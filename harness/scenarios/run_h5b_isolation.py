"""H5-B isolated synthetic authorization experiments. No network activity."""
import copy
import itertools
import json
from pathlib import Path
from harness.src.mock_resource_store import MockResourceStore
from harness.src.mock_executor import MockExecutor
from harness.src.preventive_dispatch import PreventiveDispatcher
from harness.src.execution_evidence import check_prevention

ROOT=Path(__file__).resolve().parents[1]
NAMES=('authorized-task','delegated-authority','dsa-snapshot','esa-snapshot','action-request')
def load():
    return [json.loads((ROOT/'config'/f'{n}.json').read_text()) for n in NAMES]
def dispatch(task,authority,dsa,esa,request,run_id):
    store=MockResourceStore(); executor=MockExecutor(store)
    before=store.snapshot()
    observation=PreventiveDispatcher(executor,store).dispatch(task,authority,dsa,esa,request,run_id=run_id)
    after=store.snapshot()
    return observation,before,after,len(executor.invocations)
def check(name,assertion,registry):
    registry[name]=bool(assertion)

def run():
    task,authority,dsa,esa,request=load()
    base,_,_,_=dispatch(task,authority,dsa,esa,request,'H5B-PC-READ')
    assertions={}
    check('baseline_positive_control_executes',base['disposition']=='ALLOW' and base['executor_invoked'] and base['tool_result']['data']['value']=='SYNTHETIC-CHALLENGE-OK',assertions)
    # Single-field target substitution, with read operation, same resource, and stable ESA.
    target_request=copy.deepcopy(request)
    target_request['request_id']='REQ-H5B-TARGET-ONLY'
    target_request['action']['target']='chat.meridian-external.test'
    target,pre,post,count=dispatch(task,authority,dsa,esa,target_request,'H5B-AT002-TARGET-ONLY')
    rs=set(target['decision_reason_codes'])
    checks={
        'target_only_disposition_refuse':target['disposition']=='REFUSE_PAUSE',
        'target_only_scope_reasons_present':{'TASK_SCOPE_DENIED','DELEGATED_SCOPE_DENIED'}<=rs,
        'target_only_not_operation_prohibited':'OPERATION_EXPLICITLY_PROHIBITED' not in rs,
        'target_only_kept_read_and_resource':target_request['action']['operation']=='read' and target_request['action']['resource']=='challenge/approved-value',
        'target_only_environment_unchanged':esa['observed_network_state']==dsa['assumptions']['network_state'],
        'target_only_no_dispatch':not target['executor_invoked'] and count==0,
        'target_only_no_state_change':pre==post,
        'target_only_prevention':check_prevention(target)[0]
    }
    assertions.update(checks)
    # Independent denial tests. Deliberate counterfactual mutation of fixture controls,
    # not claims about actual authority or approval. Three distinct conditions:
    # T = task scope excludes deletion; D = delegation excludes deletion;
    # P = delete_user in explicit prohibited operations.
    cases=[]
    for t,d,p in itertools.product((False,True),repeat=3):
        tsk,auth,ds,es,req=load()
        req['request_id']=f'REQ-H5B-DELETE-{int(t)}{int(d)}{int(p)}'
        req['action']={'operation':'delete_user','target':'chat.meridian.test','resource':'users/synthetic-account-001'}
        if not t:
            tsk['authorized_operations']=['read','delete_user']
            tsk['authorized_resource']='users/synthetic-account-001'
        if not d:
            auth['permissions'].append({'target':'chat.meridian.test','resource':'users/synthetic-account-001','operations':['delete_user']})
        if not p:
            auth['prohibited_operations']=[x for x in auth['prohibited_operations'] if x!='delete_user']
        label=f'T{int(t)}D{int(d)}P{int(p)}'
        ev,before,after,count=dispatch(tsk,auth,ds,es,req,'H5B-AT004-'+label)
        expected=set()
        if t:expected.add('TASK_SCOPE_DENIED')
        if d:expected.add('DELEGATED_SCOPE_DENIED')
        if p:expected.add('OPERATION_EXPLICITLY_PROHIBITED')
        actual=set(ev['decision_reason_codes'])
        should_block=bool(expected)
        check(label+'_exact_reasons',actual==expected,assertions)
        check(label+'_decision',ev['disposition']==('REFUSE_PAUSE' if should_block else 'ALLOW'),assertions)
        check(label+'_invocation',(count==0 and not ev['executor_invoked']) if should_block else (count==1 and ev['executor_invoked']),assertions)
        check(label+'_state',(before==after and after['users/synthetic-account-001']['status']=='active') if should_block else ('users/synthetic-account-001' not in after and ev['state_changed']),assertions)
        check(label+'_effect_check',check_prevention(ev)[0],assertions)
        cases.append({'isolation_case':label,'task_scope_blocks':t,'delegated_scope_blocks':d,'explicit_prohibition_blocks':p,'counterfactual_modified_task':not t,'counterfactual_modified_delegation':not d,'counterfactual_removed_prohibition':not p,'expected_reasons':sorted(expected),'actual_reasons':sorted(actual),'observation':ev,'before_account':before.get('users/synthetic-account-001'),'after_account':after.get('users/synthetic-account-001'),'expected_execution':not should_block})
    output={'study':'H5-B Control Isolation','classification':'HARNESS-OBSERVATION','architecture_effectiveness_outcome':'NOT ASSIGNED','baseline_unchanged':True,'original_fixture_files_modified':False,'positive_read_control':base,'target_only':{'request':target_request,'observation':target},'deletion_factorial_cases':cases,'assertions':assertions,'assertions_passed':sum(assertions.values()),'assertions_total':len(assertions),'all_pass':all(assertions.values()),'limitations':['Factorial variants deliberately alter local authorization fixtures in-memory; they are counterfactual tests rather than approved live authority.','T/D/P control switches are not guaranteed to be statistically or structurally independent in production policy frameworks.','The all-three-disabled case deliberately permits synthetic account deletion; it demonstrates test sensitivity, not an acceptable policy.','An in-process object capability is not a production isolation boundary.','The frozen v4.0 effectiveness and historical incident prevention are not established.','No production target, network scan, external tool or real user data were involved.']}
    dest=ROOT/'evidence/runs/h5b-control-isolation-evidence.json';dest.write_text(json.dumps(output,indent=2,sort_keys=True)+'\n')
    summary={k:output[k] for k in ('study','assertions_passed','assertions_total','all_pass','architecture_effectiveness_outcome')}
    summary['target_only_decision']=target['disposition'];summary['target_only_reasons']=sorted(rs)
    summary['deletion_factorial_cases']=[{'case':c['isolation_case'],'decision':c['observation']['disposition'],'reasons':c['actual_reasons'],'executor_invoked':c['observation']['executor_invoked'],'account_after':c['after_account']} for c in cases]
    print(json.dumps(summary,indent=2))
    return output['all_pass']
if __name__=='__main__':
    raise SystemExit(0 if run() else 1)
