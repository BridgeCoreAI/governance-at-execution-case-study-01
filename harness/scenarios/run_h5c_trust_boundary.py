"""H5-C diagnostic experiments against unmodified H1-H3 code.
All records are fictional and local. Failures are findings, never silently corrected.
"""
import copy
import json
from pathlib import Path
from unittest.mock import patch

from harness.src.decision_engine import decide
from harness.src.execution_gate import check_binding
from harness.src.mock_executor import MockExecutor
from harness.src.mock_resource_store import MockResourceStore
from harness.src.preventive_dispatch import PreventiveDispatcher

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('authorized-task', 'delegated-authority', 'dsa-snapshot', 'esa-snapshot', 'action-request')


def fixtures():
    return [json.loads((ROOT / 'config' / (name + '.json')).read_text()) for name in NAMES]


def environment():
    store = MockResourceStore()
    executor = MockExecutor(store)
    return store, executor, PreventiveDispatcher(executor, store)


def record(case, fault, result, safety_met, issue=None, **details):
    return {'test_id': case, 'fault': fault, 'classification': 'HARNESS-OBSERVATION',
            'diagnostic_result': result, 'safety_expectation_met': safety_met,
            'issue_id': issue, **details}


def run():
    cases = []
    # TC-001: revoke before a decision
    t, a, d, e, q = fixtures(); a['status'] = 'revoked'; s, x, gate = environment()
    ev = gate.dispatch(t, a, d, e, q, run_id='H5C-TC001')
    ok = ev['disposition'] == 'REFUSE_PAUSE' and 'AUTHORITY_INACTIVE' in ev['decision_reason_codes'] and not x.invocations and not ev['state_changed']
    cases.append(record('TC-001','authority revoked before decision','EXPECTED SAFE BEHAVIOR' if ok else 'OBSERVED FAILURE',ok,disposition=ev['disposition'],reasons=ev['decision_reason_codes'],gate=ev['binding_result'],invocations=len(x.invocations),state_changed=ev['state_changed']))
    # TC-002: revoked after original ALLOW, before dispatch
    t, a, d, e, q = fixtures(); s, x, gate = environment()
    ev = gate.dispatch(t, a, d, e, q, run_id='H5C-TC002',before_gate=lambda t,a,d,e,q:a.update(status='revoked'))
    ok = ev['disposition']=='ALLOW' and ev['binding_result']=='CURRENT_STATE_INVALID' and not x.invocations
    cases.append(record('TC-002','revocation after ALLOW','EXPECTED SAFE BEHAVIOR' if ok else 'OBSERVED FAILURE',ok,initial_disposition=ev['disposition'],gate=ev['binding_result'],invocations=len(x.invocations),state_changed=ev['state_changed']))
    # TC-003: stale ESA
    t, a, d, e, q = fixtures();e['evidence_freshness']='stale';s,x,gate=environment()
    ev=gate.dispatch(t,a,d,e,q,run_id='H5C-TC003')
    ok=ev['disposition']=='REVALIDATE' and 'ESA_STALE' in ev['decision_reason_codes'] and not x.invocations
    cases.append(record('TC-003','stale ESA','EXPECTED SAFE BEHAVIOR' if ok else 'OBSERVED FAILURE',ok,disposition=ev['disposition'],reasons=ev['decision_reason_codes'],invocations=len(x.invocations)))
    # TC-004: missing ESA. Safely capture unhandled error; never call it a proper refusal.
    t,a,d,e,q=fixtures();s,x,gate=environment()
    try:
        ev=gate.dispatch(t,a,d,None,q,run_id='H5C-TC004')
        ok=ev['disposition']!='ALLOW' and not x.invocations
        cases.append(record('TC-004','ESA absent','EXPECTED SAFE BEHAVIOR' if ok else 'OBSERVED FAILURE',ok,disposition=ev['disposition'],invocations=len(x.invocations)))
    except Exception as exc:
        cases.append(record('TC-004','ESA absent','UNHANDLED ERROR',False,'H5C-G01',exception_type=type(exc).__name__,exception_message=str(exc),invocations=len(x.invocations),account_unchanged=s.read('users/synthetic-account-001') is not None))
    # TC-005 policy version mismatch
    t,a,d,e,q=fixtures();e['policy_version']='POL-002-v2';s,x,gate=environment()
    ev=gate.dispatch(t,a,d,e,q,run_id='H5C-TC005')
    ok=ev['disposition']=='REVALIDATE' and 'MR-004_POLICY_DIVERGENCE' in ev['decision_reason_codes'] and not x.invocations
    cases.append(record('TC-005','policy-version mismatch','EXPECTED SAFE BEHAVIOR' if ok else 'OBSERVED FAILURE',ok,disposition=ev['disposition'],reasons=ev['decision_reason_codes'],invocations=len(x.invocations)))
    # TC-006 post-ALLOW request change
    t,a,d,e,q=fixtures();s,x,gate=environment()
    ev=gate.dispatch(t,a,d,e,q,run_id='H5C-TC006',before_gate=lambda t,a,d,e,q:q['action'].update(resource='users/restricted-records'))
    ok=ev['disposition']=='ALLOW' and ev['binding_result']=='BINDING_MISMATCH' and not x.invocations
    cases.append(record('TC-006','changed resource after ALLOW','EXPECTED SAFE BEHAVIOR' if ok else 'OBSERVED FAILURE',ok,initial_disposition=ev['disposition'],gate=ev['binding_result'],invocations=len(x.invocations)))
    # TC-007 identical earlier ALLOW decision accepted twice at binding. No replay consumption ledger.
    t,a,d,e,q=fixtures();decision=decide(t,a,d,e,q)
    first=check_binding(decision,t,a,d,e,q);second=check_binding(decision,t,a,d,e,q)
    accepted_twice=first==(True,'BINDING_VALID') and second==(True,'BINDING_VALID')
    cases.append(record('TC-007','identical decision reused twice','NOT EVALUABLE' if accepted_twice else 'EXPECTED SAFE BEHAVIOR',not accepted_twice,'H5C-G02' if accepted_twice else None,first_binding=first[1],second_binding=second[1],note='Binding accepted twice; test does not claim two real tool invocations. Single-use authorization not specified.'))
    # TC-008 collector raises after executor; prove tool ran despite missing record
    t,a,d,e,q=fixtures();s,x,gate=environment();pre=s.digest()
    with patch('harness.src.preventive_dispatch.make_evidence',side_effect=RuntimeError('SIMULATED_COLLECTOR_FAILURE')):
        try:
            gate.dispatch(t,a,d,e,q,run_id='H5C-TC008')
            exception=None
        except Exception as exc:
            exception=type(exc).__name__
    invoked=len(x.invocations)
    cases.append(record('TC-008','evidence collector fails after mock execution','OBSERVED FAILURE' if invoked else 'EXPECTED SAFE BEHAVIOR',not bool(invoked),'H5C-G03' if invoked else None,exception_type=exception,executor_invocations=invoked,state_changed=pre!=s.digest(),note='Authorized read executed but no complete evidence returned; not a claim of unauthorized modification.'))
    # TC-009 forged ESA reporting expected state, independent ground truth says network open
    t,a,d,e,q=fixtures();ground_truth={'network_state':'external_access_available'};s,x,gate=environment()
    ev=gate.dispatch(t,a,d,e,q,run_id='H5C-TC009')
    false_clean=ev['disposition']=='ALLOW' and ev['executor_invoked'] and ground_truth['network_state']!=d['assumptions']['network_state']
    cases.append(record('TC-009','forged consistent ESA with divergent independent ground truth','OBSERVED FAILURE' if false_clean else 'EXPECTED SAFE BEHAVIOR',not false_clean,'H5C-G04' if false_clean else None,ground_truth=ground_truth,unverified_esa_claim=e['observed_network_state'],disposition=ev['disposition'],invocations=len(x.invocations),note='Synthetic telemetry-integrity gap; harness has no authenticated source of truth.'))
    # TC-010 privileged direct store deletion, executor gate bypassed
    s,x,gate=environment();before=s.read('users/synthetic-account-001')
    outcome=s.delete_synthetic_account('users/synthetic-account-001')
    after=s.read('users/synthetic-account-001')
    bypassed=before is not None and after is None and len(x.invocations)==0
    cases.append(record('TC-010','trusted in-process store access bypasses dispatch','OBSERVED FAILURE' if bypassed else 'EXPECTED SAFE BEHAVIOR',not bypassed,'H5C-G05' if bypassed else None,direct_store_result=outcome,executor_invocations=len(x.invocations),account_before=before,account_after=after,note='Privileged local test access, not a real external exploit.'))

    passed=sum(c['safety_expectation_met'] for c in cases)
    result={'phase':'H5-C','provenance':'HARNESS-OBSERVATION','architecture_effectiveness_outcome':'NOT ASSIGNED','cases':cases,'case_count':len(cases),'safety_met':passed,'safety_not_met':len(cases)-passed,'diagnostic_objective_met':len(cases)==10 and all('diagnostic_result' in c for c in cases),'unmodified_h1_h3_source':True,'warning':'Correct diagnostic classification does not mean a failed safeguard passed. Test outcomes do not establish frozen-architecture effectiveness.'}
    output=ROOT/'evidence/runs/h5c-trust-boundary-evidence.json'
    output.write_text(json.dumps(result,sort_keys=True,indent=2)+'\n')
    return result

if __name__=='__main__':
    x=run()
    print(json.dumps({'case_count':x['case_count'],'safety_met':x['safety_met'],'safety_not_met':x['safety_not_met'],'diagnostic_objective_met':x['diagnostic_objective_met'],'results':[(c['test_id'],c['diagnostic_result']) for c in x['cases']]},indent=2))
    raise SystemExit(0 if x['diagnostic_objective_met'] else 1)
