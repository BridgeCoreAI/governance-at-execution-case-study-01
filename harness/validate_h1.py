"""Validate the H1 synthetic baseline. No external access, no execution-gate claims."""
from pathlib import Path
import json
import sys
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parent
NAMES = ['authorized-task','delegated-authority','dsa-snapshot','esa-snapshot','action-request']

def validate():
    records = {}
    problems = []
    for name in NAMES:
        try:
            doc = json.loads((ROOT/'config'/f'{name}.json').read_text())
            schema = json.loads((ROOT/'schema'/f'{name}.schema.json').read_text())
            Draft202012Validator.check_schema(schema)
            for error in Draft202012Validator(schema).iter_errors(doc):
                problems.append(f'{name}: {error.message}')
            records[name] = doc
        except (OSError, ValueError) as exc:
            problems.append(f'{name}: {exc}')
    if len(records) != len(NAMES):
        return problems
    t,a,d,e,q = [records[n] for n in NAMES]
    def require(condition,label):
        if not condition: problems.append(label)
    require(t['agent_id']==a['principal']==d['agent_id']==q['agent_id'],'agent identity mismatch')
    require(t['task_id']==a['task_id']==d['task_id']==q['task_id'],'task identity mismatch')
    require(t['approval_id']==a['approval_id']==d['approval_id']==q['approval_id'],'approval mismatch')
    require(t['authority_ref']==a['authority_id']==d['authority_ref']==q['authority_ref'],'authority mismatch')
    require(t['dsa_ref']==d['dsa_id']==q['dsa_ref'],'DSA reference mismatch')
    require(t['policy_version']==d['policy_version']==e['policy_version'],'policy version mismatch')
    require(t['approved_intent']==d['approved_intent'],'approved intent mismatch')
    require(t['authorized_target']==d['assumptions']['target'],'approved target mismatch')
    require(t['expected_network_state']==d['assumptions']['network_state'],'network assumption mismatch')
    require(t['approval_status']=='approved','task not approved')
    require(a['status']=='active' and e['authority_status']=='active','authority not active')
    require(e['evidence_freshness']=='current','ESA evidence not current')
    require(e['observed_network_state']==d['assumptions']['network_state'],'material network divergence: revalidation required')
    require(e['current_target']==t['authorized_target'],'current environmental target mismatch')
    require(t['authorized_target'].endswith('.test') and e['current_target'].endswith('.test') and q['action']['target'].endswith('.test'),'non-synthetic target detected')
    request=q['action']
    require(request['operation'] not in a['prohibited_operations'],'explicitly prohibited operation')
    require(request['target']==t['authorized_target'] and request['resource']==t['authorized_resource'] and request['operation'] in t['authorized_operations'],'request outside task scope')
    require(any(request['target']==p['target'] and request['resource']==p['resource'] and request['operation'] in p['operations'] for p in a['permissions']),'request outside delegated authority')
    return problems

if __name__ == '__main__':
    errors=validate()
    if errors:
        print('H1 BASELINE VALIDATION FAILED')
        for err in errors: print(' -',err)
        sys.exit(1)
    print('H1 BASELINE VALIDATION PASSED: 5 schemas and cross-record checks')
    print('NOTE: fixture validation only; no gate enforcement or AT-001–AT-004 test executed.')
