# H5-C Trust Boundary and Failure Analysis: Local Evidence Report

**Researcher:** Grace Adjeli | BridgeCore AI LLC  
**Frozen architecture:** Governance at Execution™ v4.0, September 6, 2026  
**Provenance:** HARNESS-OBSERVATION (H1–H3 Python test harness)  
**Status:** Executed locally; awaiting approval for GitHub commit  
**Architecture effectiveness disposition:** NOT ASSIGNED

## Question and method

The study evaluates how the post-baseline synthetic H1–H3 governance harness behaves when authorization, environment, decision binding, or evidence is compromised. It does **not** test the frozen architecture implementation or Anthropic infrastructure. All records are in-memory fictional objects. No H1–H3 source files were modified. Faults were injected through disposable copies and test-only hooks.

## Ten diagnostic results

| ID | Fault | Outcome | Observed behavior |
|---|---|---|---|
| TC-001 | Delegation revoked before decision | Expected safe behavior | REFUSE_PAUSE, inactive authority reason, no invocation |
| TC-002 | Delegation revoked after ALLOW, before dispatch | Expected safe behavior | CURRENT_STATE_INVALID, no invocation |
| TC-003 | ESA stale | Expected safe behavior | REVALIDATE, no invocation |
| TC-004 | ESA absent | Expected safe behavior | REVALIDATE and non-execution; a predicted unhandled error did not occur |
| TC-005 | Policy version mismatch | Expected safe behavior | REVALIDATE, no invocation |
| TC-006 | Request resource changed after ALLOW | Expected safe behavior | BINDING_MISMATCH, no invocation |
| TC-007 | Repeat a previously valid binding check | Not evaluable against undefined replay policy | Identical decision accepted twice by binding check; no second executor operation attempted |
| TC-008 | Evidence collector raises | Observed assurance failure | Authorized mock read executed before evidence collector failure; complete evidence not returned |
| TC-009 | False but consistent ESA | Observed trust-boundary failure | Mock execution allowed based on false simulated telemetry, contrary to independent synthetic ground truth |
| TC-010 | Privileged direct resource-store modification | Observed boundary limitation | Synthetic account deleted through in-process store API, without invoking gated executor |

**Summary:** 6 expected-safe outcomes, 3 observed implementation/assurance weaknesses, 1 replay-policy question not evaluable without a specification. The 10 diagnostic records were produced successfully, which is not the same as ten safeguards passing.

## Reproducibility and regression

- Local diagnostic suite: ten cases captured; six additional unittest diagnostic assertions passed.
- Combined H2/H3/H5-C automated suite: **30 tests passed, 0 failed**. Tests verify that weaknesses are *reported*, rather than interpreted as successful security controls.
- H1 baseline schema validation: passed.
- Full scenario observations: `harness/evidence/runs/h5c-trust-boundary-evidence.json`.
- Defects and gaps: `harness/evidence/reports/h5c-defect-and-gap-register.md`.

## Control evidence vs frozen design

**FROZEN-DESIGN:** The September 6, 2026 diagram depicts decision state, environmental state, reconciliation, delegated authority, execution gate, and evidence layer.

**HARNESS-SPECIFICATION:** The JSON fields, Python comparison rules, and in-process authorization model were introduced after the freeze.

**HARNESS-OBSERVATION:** The existing harness protected six tested conditions, left replay semantics unspecified, and showed three meaningful implementation/assurance limitations.

**INFERENCE:** Successful nominal decisions are insufficient to establish reliable operational governance without trusted telemetry, evidence continuity, complete mediation, and defined authorization reuse policy. These are recommendations to examine, not proofs that the frozen design contained or lacked executable implementations.

## Significant limitations

1. TC-007 tests repeated binding validation, **not** repeated dispatch of a real capability.
2. TC-008 concerns an authorized read and missing evidence, **not** an unauthorized operation.
3. TC-009 uses an independent synthetic ground-truth variable. It does not verify real telemetry collection, signatures, or compromise.
4. TC-010 bypass comes from privileged trusted-process code, not remote access.
5. The object-identity capability and in-memory store have no secure process boundary or independent immutable audit log.
6. No original Anthropic system, model, or incident transcript was executed.
7. Formal AT-001–004 frozen architecture effectiveness determinations remain **NOT ASSIGNED**.

## Reproduction

```bash
python -m harness.scenarios.run_h5c_trust_boundary
python -m unittest discover -s harness/tests -v
python harness/validate_h1.py
```

## Review disposition

Proposed for user approval as a diagnostic experimental finding. Do not modify frozen architecture, retroactively change H4 results, claim all controls passed, or commit without explicit approval.
