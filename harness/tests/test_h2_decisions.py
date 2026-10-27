"""Deterministic H2 decision tests; deliberately no mock execution."""
import copy
import json
from pathlib import Path
import unittest
from harness.src.decision_engine import decide
from harness.src.execution_gate import check_binding

CONFIG = Path(__file__).resolve().parents[1] / 'config'

def fixtures():
    names = ('authorized-task', 'delegated-authority', 'dsa-snapshot', 'esa-snapshot', 'action-request')
    return [json.loads((CONFIG / (name + '.json')).read_text()) for name in names]

class H2DecisionTests(unittest.TestCase):
    def check(self, mutate, expected):
        t,a,d,e,q = fixtures()
        mutate(t,a,d,e,q)
        decision = decide(t,a,d,e,q)
        self.assertEqual(expected, decision['disposition'], decision)
        self.assertEqual(expected == 'ALLOW', decision['execution_eligible'])
        return decision

    def test_pc001_approved_read(self):
        self.check(lambda *args: None, 'ALLOW')

    def test_nc001_revoked_authority(self):
        self.check(lambda t,a,d,e,q: a.update(status='revoked'), 'REFUSE_PAUSE')

    def test_nc002_unauthorized_target(self):
        self.check(lambda t,a,d,e,q: q['action'].update(target='chat.meridian-external.test'), 'REFUSE_PAUSE')

    def test_nc003_restricted_user_data(self):
        self.check(lambda t,a,d,e,q: q['action'].update(resource='users/restricted-records'), 'REFUSE_PAUSE')

    def test_nc004_delete_user(self):
        self.check(lambda t,a,d,e,q: q['action'].update(operation='delete_user', resource='users/synthetic-account-001'), 'REFUSE_PAUSE')

    def test_nc005_network_divergence(self):
        decision=self.check(lambda t,a,d,e,q: e.update(observed_network_state='external_access_available'), 'REVALIDATE')
        self.assertIn('MR-001_NETWORK_DIVERGENCE',decision['reason_codes'])

    def test_nc006_stale_environment(self):
        self.check(lambda t,a,d,e,q: e.update(evidence_freshness='stale'), 'REVALIDATE')

    def test_nc007_missing_authority_reference(self):
        self.check(lambda t,a,d,e,q: q.pop('authority_ref'), 'REFUSE_PAUSE')

    def test_nc008_denied_target_and_divergence(self):
        def mutate(t,a,d,e,q):
            q['action']['target']='chat.meridian-external.test'
            e['observed_network_state']='external_access_available'
        decision=self.check(mutate, 'REFUSE_PAUSE')
        self.assertIn('MR-001_NETWORK_DIVERGENCE',decision['reason_codes'])
        self.assertIn('DELEGATED_SCOPE_DENIED',decision['reason_codes'])

    def test_nc009_reused_decision_changed_action(self):
        t,a,d,e,q=fixtures()
        decision=decide(t,a,d,e,q)
        q['action']['resource']='users/restricted-records'
        self.assertEqual((False,'BINDING_MISMATCH'),check_binding(decision,t,a,d,e,q))

    def test_nc010_reused_decision_changed_esa_version(self):
        t,a,d,e,q=fixtures()
        decision=decide(t,a,d,e,q)
        e['esa_version']='2.0'
        self.assertEqual((False,'BINDING_MISMATCH'),check_binding(decision,t,a,d,e,q))

    def test_non_allow_never_valid_binding(self):
        t,a,d,e,q=fixtures()
        e['evidence_freshness']='stale'
        decision=decide(t,a,d,e,q)
        self.assertEqual((False,'NON_ALLOW_DISPOSITION'),check_binding(decision,t,a,d,e,q))

    def test_allow_valid_binding(self):
        t,a,d,e,q=fixtures()
        decision=decide(t,a,d,e,q)
        self.assertEqual((True,'BINDING_VALID'),check_binding(decision,t,a,d,e,q))

    def test_changed_auth_scope_invalidates_binding(self):
        t,a,d,e,q=fixtures()
        decision=decide(t,a,d,e,q)
        a['permissions']=[]
        self.assertEqual((False,'AUTHORITY_CHANGED'),check_binding(decision,t,a,d,e,q))

if __name__ == '__main__':
    unittest.main()
