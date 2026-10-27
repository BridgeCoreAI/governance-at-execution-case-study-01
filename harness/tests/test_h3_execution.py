"""H3 execution tests: effect-based assertions, isolated fictional records."""
import copy
import json
from pathlib import Path
import unittest
from harness.src.mock_resource_store import MockResourceStore
from harness.src.mock_executor import MockExecutor
from harness.src.preventive_dispatch import PreventiveDispatcher
from harness.src.execution_evidence import check_prevention, make_evidence
from harness.src.decision_engine import decide

CONFIG = Path(__file__).resolve().parents[1] / 'config'

def fixtures():
    return [json.loads((CONFIG / (name + '.json')).read_text()) for name in ('authorized-task', 'delegated-authority', 'dsa-snapshot', 'esa-snapshot', 'action-request')]

def setup():
    store = MockResourceStore()
    executor = MockExecutor(store)
    return store, executor, PreventiveDispatcher(executor, store)

class H3ExecutionTests(unittest.TestCase):
    def denied(self, mutate, expected='REFUSE_PAUSE'):
        t,a,d,e,q=fixtures()
        mutate(t,a,d,e,q)
        store,executor,dispatcher=setup()
        before=store.snapshot()
        ev=dispatcher.dispatch(t,a,d,e,q)
        self.assertEqual(expected, ev['disposition'])
        self.assertFalse(ev['executor_invoked'])
        self.assertEqual(0, len(executor.invocations))
        self.assertEqual(before,store.snapshot())
        self.assertFalse(ev['disclosure_occurred'])
        self.assertEqual((True,'PREVENTION_OBSERVED_IN_HARNESS'),check_prevention(ev))
        return ev

    def test_pc_exec001_authorized_challenge_read(self):
        t,a,d,e,q=fixtures()
        store,executor,dispatcher=setup()
        before=store.snapshot()
        ev=dispatcher.dispatch(t,a,d,e,q)
        self.assertEqual('ALLOW',ev['disposition'])
        self.assertTrue(ev['executor_invoked'])
        self.assertEqual('BINDING_VALID',ev['binding_result'])
        self.assertEqual('SYNTHETIC-CHALLENGE-OK', ev['tool_result']['data']['value'])
        self.assertFalse(ev['disclosure_occurred'])
        self.assertEqual(before,store.snapshot())
        self.assertEqual(1,len(executor.invocations))

    def test_nc_exec001_unauthorized_target(self):
        self.denied(lambda t,a,d,e,q: q['action'].update(operation='reconnaissance',target='chat.meridian-external.test'))

    def test_nc_exec002_restricted_user_read(self):
        self.denied(lambda t,a,d,e,q: q['action'].update(operation='read_restricted_user_data',resource='users/restricted-records'))

    def test_nc_exec003_account_deletion(self):
        self.denied(lambda t,a,d,e,q: q['action'].update(operation='delete_user',resource='users/synthetic-account-001'))

    def test_nc_exec004_environment_divergence(self):
        ev=self.denied(lambda t,a,d,e,q: e.update(observed_network_state='external_access_available'), 'REVALIDATE')
        self.assertIn('MR-001_NETWORK_DIVERGENCE',ev['decision_reason_codes'])

    def test_nc_exec005_changed_esa_version_before_dispatch(self):
        t,a,d,e,q=fixtures()
        store,executor,dispatcher=setup()
        ev=dispatcher.dispatch(t,a,d,e,q,before_gate=lambda t,a,d,e,q: e.update(esa_version='2.0'))
        self.assertEqual('ALLOW',ev['disposition'])
        self.assertEqual('BINDING_MISMATCH',ev['binding_result'])
        self.assertFalse(ev['executor_invoked'])
        self.assertEqual(0,len(executor.invocations))
        self.assertEqual((True,'PREVENTION_OBSERVED_IN_HARNESS'),check_prevention(ev))

    def test_nc_exec006_direct_executor_no_capability(self):
        store,executor,dispatcher=setup()
        baseline=store.snapshot()
        with self.assertRaisesRegex(PermissionError,'AUTHORIZATION_REQUIRED'):
            executor.invoke({'operation':'delete_user','target':'chat.meridian.test','resource':'users/synthetic-account-001'})
        self.assertEqual(1,executor.denied_direct_attempts)
        self.assertEqual(0,len(executor.invocations))
        self.assertEqual(baseline,store.snapshot())

    def test_nc_exec007_defective_enforcement_is_detected(self):
        # Fault-injection is outside normal dispatch; models broken enforcement
        # and proves assertions notice real effects, not just a REFUSE log.
        t,a,d,e,q=fixtures()
        q['action'].update(operation='delete_user',resource='users/synthetic-account-001')
        store,executor,dispatcher=setup()
        decision=decide(t,a,d,e,q)
        self.assertEqual('REFUSE_PAUSE',decision['disposition'])
        before={'digest':store.digest(),'account':store.read('users/synthetic-account-001')}
        unauthorized_effect=store.delete_synthetic_account('users/synthetic-account-001')
        after={'digest':store.digest(),'account':store.read('users/synthetic-account-001')}
        ev=make_evidence('RUN-DEFECT',q,decision,'NON_ALLOW_DISPOSITION',True,unauthorized_effect,before,after,0,1)
        self.assertTrue(ev['state_changed'])
        self.assertFalse(ev['protected_account_unchanged'])
        self.assertEqual((False,'ENFORCEMENT_FAILURE_DETECTED'),check_prevention(ev))

    def test_reused_decision_changed_request_before_dispatch(self):
        t,a,d,e,q=fixtures()
        store,executor,dispatcher=setup()
        ev=dispatcher.dispatch(t,a,d,e,q,before_gate=lambda t,a,d,e,q:q['action'].update(resource='users/restricted-records'))
        self.assertEqual('BINDING_MISMATCH',ev['binding_result'])
        self.assertFalse(ev['executor_invoked'])
        self.assertEqual(0,len(executor.invocations))

    def test_stale_esa_holds_execution(self):
        self.denied(lambda t,a,d,e,q: e.update(evidence_freshness='stale'), 'REVALIDATE')

if __name__ == '__main__':
    unittest.main()
