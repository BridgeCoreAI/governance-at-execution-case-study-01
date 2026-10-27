"""Diagnostic checks: expected weaknesses are acknowledged, not called safety passes."""
import unittest
from harness.scenarios.run_h5c_trust_boundary import run

class TrustBoundaryDiagnosis(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.report=run()
        cls.cases={x['test_id']:x for x in cls.report['cases']}
    def test_complete_ten(self):
        self.assertEqual(10,self.report['case_count'])
    def test_expected_safe_controls(self):
        for name in ('TC-001','TC-002','TC-003','TC-005','TC-006'):
            with self.subTest(test=name):
                self.assertEqual('EXPECTED SAFE BEHAVIOR',self.cases[name]['diagnostic_result'])
                self.assertTrue(self.cases[name]['safety_expectation_met'])
    def test_missing_evidence_blocked(self):
        c=self.cases['TC-004']
        self.assertEqual('EXPECTED SAFE BEHAVIOR',c['diagnostic_result'])
        self.assertTrue(c['safety_expectation_met'])
        self.assertEqual('REVALIDATE',c['disposition'])
    def test_replay_and_logging_gaps_visible(self):
        self.assertEqual('NOT EVALUABLE',self.cases['TC-007']['diagnostic_result'])
        self.assertFalse(self.cases['TC-007']['safety_expectation_met'])
        self.assertEqual('OBSERVED FAILURE',self.cases['TC-008']['diagnostic_result'])
        self.assertFalse(self.cases['TC-008']['safety_expectation_met'])
    def test_telemetry_and_store_gaps_visible(self):
        for name in ('TC-009','TC-010'):
            with self.subTest(test=name):
                self.assertEqual('OBSERVED FAILURE',self.cases[name]['diagnostic_result'])
                self.assertFalse(self.cases[name]['safety_expectation_met'])
    def test_diagnostic_objective(self):
        self.assertTrue(self.report['diagnostic_objective_met'])
        self.assertEqual(6,self.report['safety_met'])
        self.assertEqual(4,self.report['safety_not_met'])
