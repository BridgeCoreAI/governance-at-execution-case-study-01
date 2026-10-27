# H2 Local Decision-Level Test Report

**Researcher:** Grace Adjeli | BridgeCore AI LLC  
**Status:** Local harness observation; uncommitted review package  
**System under test:** New H2 synthetic deterministic policy, reconciliation, decision and binding logic  
**Not tested:** Frozen architecture implementation, real AI behavior, network isolation, mock-tool execution, prevented mutations

## Results

- H1 schema / cross-record baseline: PASSED (local invocation)
- H2 decision-level unit tests: **14 passed, 0 failed**
- Positive authorization case: passed
- Revoked authority, unauthorized target, restricted data, and unauthorized deletion: yielded REFUSE_PAUSE as specified
- Environmental divergence and stale ESA: yielded REVALIDATE as specified
- Missing authority reference: yielded REFUSE_PAUSE
- Combined prohibited target plus divergence: yielded REFUSE_PAUSE and recorded divergent condition
- Binding mismatch when request or ESA version changes: rejected
- Valid unchanged ALLOW binding: accepted as eligible (no executor)
- Removed authority permission after decision: binding rejected

## Scope and limitations

Results apply only to the local deterministic harness using synthetic JSON fixtures, and demonstrate decisions and binding checks, **not actual enforcement of tool execution**. Escalation and mitigation logic are not implemented beyond the disposition vocabulary. The tested environmental conditions are simulated inputs, not externally verified telemetry. Evidence output is a local test-run file, not tamper-evident audit evidence. No formal AT-001 through AT-004 effectiveness outcome is assigned.

## Execution

From review bundle root:

```bash
python -m unittest discover -s harness/tests -v
python harness/validate_h1.py
```

See `h2-local-test-output.txt` for individual checks.
