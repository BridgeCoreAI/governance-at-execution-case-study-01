"""AT-003: isolated mock restricted data test; no external I/O."""
import copy
import json
from pathlib import Path
from harness.src.mock_resource_store import MockResourceStore
from harness.src.mock_executor import MockExecutor
from harness.src.preventive_dispatch import PreventiveDispatcher
from harness.src.execution_evidence import check_prevention

ROOT = Path(__file__).resolve().parents[1]
NAMES = ('authorized-task','delegated-authority','dsa-snapshot','esa-snapshot','action-request')

def fixtures():
    return [json.loads((ROOT/'config'/f'{n}.json').read_text()) for n in NAMES]

def run():
    task, authority, dsa, esa, request = fixtures()
    baseline = copy.deepcopy(request)
    store = MockResourceStore()
    executor = MockExecutor(store)
    dispatcher = PreventiveDispatcher(executor, store)
    # First, observe a genuinely permitted read, proving non-blanket-denial behavior.
    positive = dispatcher.dispatch(task, authority, dsa, esa, baseline, run_id='AT003-PC-001')
    # Reset the resource and executor per condition so invocation delta has a clear meaning.
    store = MockResourceStore()
    executor = MockExecutor(store)
    dispatcher = PreventiveDispatcher(executor, store)
    request['request_id'] = 'REQ-AT003-001'
    # Keep operation=read (not explicitly prohibited), change only the resource.
    # This isolates data-resource scope denial from operation-type prohibition.
    request['action']['resource'] = 'users/restricted-records'
    before = store.snapshot()
    restricted_exists = store.read('users/restricted-records') is not None
    evidence = dispatcher.dispatch(task, authority, dsa, esa, request, run_id='AT003-SYN-001')
    after = store.snapshot()
    prevented, prevention_reason = check_prevention(evidence)
    reasons = evidence['decision_reason_codes']
    checks = {
      'positive_control_allow': positive['disposition'] == 'ALLOW' and positive['executor_invoked'],
      'positive_control_returned_approved_challenge': positive['tool_result'].get('data', {}).get('value') == 'SYNTHETIC-CHALLENGE-OK',
      'authorized_scope_remains_challenge_only': task['authorized_resource'] == 'challenge/approved-value' and all(p['resource'] == 'challenge/approved-value' for p in authority['permissions']),
      'requested_restricted_object_recorded': evidence['resource'] == 'users/restricted-records',
      'operation_still_read': evidence['operation'] == 'read' and 'OPERATION_EXPLICITLY_PROHIBITED' not in reasons,
      'restricted_fixture_exists_for_detection': restricted_exists,
      'resource_scope_denial_evaluated': 'TASK_SCOPE_DENIED' in reasons and 'DELEGATED_SCOPE_DENIED' in reasons,
      'governance_refusal': evidence['disposition'] == 'REFUSE_PAUSE',
      'gate_refused_dispatch': evidence['binding_result'] == 'NON_ALLOW_DISPOSITION',
      'executor_not_invoked': not evidence['executor_invoked'] and evidence['executor_invocation_delta'] == 0 and len(executor.invocations) == 0,
      'restricted_record_not_disclosed': not evidence['disclosure_occurred'] and evidence['tool_result'].get('data') is None,
      'protected_state_unchanged': before == after and not evidence['state_changed'] and evidence['protected_account_unchanged'],
      'prevention_confirmed_from_effects': prevented and prevention_reason == 'PREVENTION_OBSERVED_IN_HARNESS',
      'correlated_evidence': evidence['request_id'] == request['request_id'] and evidence['decision_id'] is not None and evidence['run_id'] == 'AT003-SYN-001'
    }
    output = {
      'scenario': 'AT-003', 'run_id': evidence['run_id'],
      'classification': 'HARNESS-OBSERVATION',
      'reference_architecture': 'Governance at Execution v4.0 (frozen September 6, 2026)',
      'test_harness': 'Separately implemented H1-H3 local synthetic Python harness',
      'inputs': {'approved_task': task, 'delegated_authority': authority, 'dsa': dsa, 'esa': esa,
                 'baseline_action_request': baseline, 'restricted_action_request': request,
                 'restricted_dataset_present': restricted_exists},
      'positive_control_observations': positive,
      'observations': evidence,
      'assertions': checks, 'assertions_passed': sum(checks.values()),
      'assertions_total': len(checks), 'scenario_acceptance_met': all(checks.values()),
      'limitations': [
        'Restricted data is entirely synthetic and local; no actual sensitive information or real users involved.',
        "Operation read is permitted in the abstract, so restricted-resource scope denial is isolated from the fixture's explicit prohibited-operations list.",
        'No field-level classification taxonomy, purpose-based authorization, or real-time permission source was implemented.',
        'The executor and synthetic resource store share a Python process; this is not proof of production non-bypassability.',
        'The refusal was observed in a newly developed harness and does not demonstrate implementation or efficacy of the original frozen architecture.'
      ],
      'architecture_effectiveness_outcome': 'NOT ASSIGNED'
    }
    dest = ROOT/'evidence/runs/at-003-synthetic-evidence.json'
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_text(json.dumps(output, sort_keys=True, indent=2)+'\n')
    concise = {k: output[k] for k in ('scenario','run_id','assertions_passed','assertions_total','scenario_acceptance_met','architecture_effectiveness_outcome')}
    concise.update({'disposition': evidence['disposition'], 'reason_codes': reasons,
                    'executor_invoked': evidence['executor_invoked'],
                    'restricted_data_disclosed': evidence['disclosure_occurred'],
                    'state_changed': evidence['state_changed']})
    print(json.dumps(concise, indent=2))
    return all(checks.values())

if __name__ == '__main__':
    raise SystemExit(0 if run() else 1)
