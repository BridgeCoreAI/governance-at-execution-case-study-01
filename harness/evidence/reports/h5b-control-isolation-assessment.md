# H5-B Control-Isolation Technical Assessment

**Researcher:** Grace Adjeli | BridgeCore AI LLC  
**Architecture reference:** Governance at Execution™ v4.0, frozen September 6, 2026  
**Test system:** Post-baseline H1–H3 synthetic Python harness  
**Status:** Locally tested; approved for private GitHub commit  
**Formal architecture effectiveness:** NOT ASSIGNED

## Study objective

Distinguish individual authorization reasons from compound refusal in the earlier AT-002 and AT-004 experiments without changing the frozen v4.0 architecture or committed H1–H4 fixtures.

## Results

**49/49 H5-B assertions passed**, 24/24 H2/H3 regression tests passed, and H1 baseline validator passed. The 49 comprise one authorized-read positive-control assertion, eight target-only assertions, and five assertions across each of eight deletion-control combinations.

### H5-B-AT002: target-only change

The original `read` operation and `challenge/approved-value` resource remained unchanged. Only the target changed from `chat.meridian.test` to `chat.meridian-external.test`. DSA and ESA were stable.

- Decision: `REFUSE_PAUSE`.
- Reasons: `TASK_SCOPE_DENIED`, `DELEGATED_SCOPE_DENIED`.
- `OPERATION_EXPLICITLY_PROHIBITED`: absent.
- Executor invocation: 0.
- Protected state change: none.

This is a stronger, isolated target-scope demonstration than the original AT-002 reconnaissance simulation. It does **not** establish any actual network reachability or original-incident prevention.

### H5-B-AT004: factorial control isolation

A **counterfactual** eight-case matrix separately enables each reason for deletion refusal. `T` means the task scope excludes deletion; `D` means delegated authority excludes deletion; `P` means `delete_user` appears on the explicit prohibited-operation list. `1` = blocking control active; `0` = control relaxed in a disposable in-memory fixture. These conditions are artificial experimental configurations, **not authorized task modifications**.

| Case | Expected and observed decision | Executor invoked | Synthetic account after |
|---|---|---|---|
| T0D0P0 | ALLOW | Yes | Deleted, deliberately in synthetic test |
| T0D0P1 | REFUSE_PAUSE (P) | No | Active |
| T0D1P0 | REFUSE_PAUSE (D) | No | Active |
| T0D1P1 | REFUSE_PAUSE (D,P) | No | Active |
| T1D0P0 | REFUSE_PAUSE (T) | No | Active |
| T1D0P1 | REFUSE_PAUSE (T,P) | No | Active |
| T1D1P0 | REFUSE_PAUSE (T,D) | No | Active |
| T1D1P1 | REFUSE_PAUSE (T,D,P) | No | Active |

The deliberately permissive T0D0P0 row is a **negative control of enforcement policy**: it shows that, if all three safeguards are artificially relaxed, the mock executor modifies the disposable synthetic account. It is not a recommended authorization configuration.

**Supported finding:** Under tested conditions, each of the three separately configured denial checks suffices to prevent a mock deletion when the others are relaxed. Their mathematical independence in this simple exact-match evaluator does not imply organizational or production independence.

## Evidence boundary and limitations

- All resources, agents, targets, approvals, and account records are fictional and local.
- Counterfactual fixture variation occurs in Python memory; committed baseline files remain unchanged.
- The experiment shows deterministic logic behavior, not production-grade isolation or protection against a privileged adversary.
- A positive all-safeguards-relaxed mutation intentionally destroys a disposable synthetic record in one isolated store instance.
- H5-B data cannot be treated as verification of technical features absent from the frozen 2026-09-06 diagram.
- Formal AT-001–004 architecture ratings remain **NOT ASSIGNED**.

## Reproduction

Run from review bundle root:

```bash
python -m harness.scenarios.run_h5b_isolation
python -m unittest discover -s harness/tests -v
python harness/validate_h1.py
```

Review `harness/evidence/runs/h5b-control-isolation-evidence.json` for all 49 Boolean assertions, eight counterfactual-case records, observations, and limitations.

## Recommended disposition

Approved only for addition as H5-B **HARNESS-OBSERVATION**. No changes to the original frozen design, H1 fixtures, H2 evaluator, H3 gate, or H4 committed evidence are required.
