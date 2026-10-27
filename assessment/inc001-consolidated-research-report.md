# Governance at Execution™ v4.0
## Incident-Aligned Research Assessment: Claude Opus 4.7 Cybersecurity Evaluation

**Researcher:** Grace Adjeli | **Research organization:** BridgeCore AI LLC  
**Case:** INC-001 | **Frozen architecture date:** September 6, 2026  
**Version:** Consolidated review draft v0.1 | **Prepared:** October 27, 2026  
**Status:** Pending researcher approval. Private research only; no GitHub commit or public release authorized.  
**Formal frozen-architecture effectiveness ratings:** NOT ASSIGNED

---

## Executive Summary

This independent research evaluates Governance at Execution™ v4.0, preserved as a September 6, 2026 frozen conceptual architecture, against publicly reported events from Anthropic's Claude Opus 4.7 cybersecurity evaluation. The central question is whether technical ability to reach and operate on a system can be distinguished from valid delegated authority to perform a consequential action, particularly when the operating environment has changed since authorization.

The incident reconstruction draws on Anthropic's July 30, 2026 disclosure (SRC-001) and September 9, 2026 follow-up assessment (SRC-002), as analyzed in the private case's evidence-closure audit. Public reporting describes an intended isolated evaluation environment in which an internet-access configuration error enabled contact with external systems. In one detailed Opus 4.7 run, a real organization resembling the fictional exercise target became the subject of unauthorized interaction; Anthropic subsequently reported access to user-related information and a consequential account action. The full raw execution transcript, original infrastructure logs, third-party audit logs, and complete authorization records were not independently inspected.

Visual review of the supplied v4.0 diagram verifies conceptual mechanisms including Decision State Awareness (DSA), Environmental State Awareness (ESA), state reconciliation and materiality evaluation, delegated authority, an execution gate labeled “Enforce at Bind,” five possible dispositions, and an Evidence, Audit & Assurance Layer. The original GitHub image remains the authoritative frozen specimen; the uploads' byte-for-byte identity with that repository image is unresolved.

Following the freeze, H1–H3 created a **separate deterministic, local Python test harness**. H4's four incident-aligned simulations recorded **53/53 passing scenario assertions**, and H5-B's control-isolation experiments recorded **49/49 passing diagnostic assertions**. H5-C evaluated ten trust-boundary scenarios: **six expected-safe behaviors, three documented implementation or assurance weaknesses, and one replay-policy question not evaluable as a violation of defined requirements**. H5-C's **30/30 passing automated tests** are diagnostic tests that also confirm correct recognition of weaknesses; they are not evidence that all ten safeguards passed.

**Research disposition:** Selected controls were demonstrable in the later synthetic harness. The reviewed frozen architecture does not, on its own, establish those implementations' presence, deployment, non-bypassability, or incident prevention. Therefore AT-001–AT-004 have **insufficient evidence to determine frozen-architecture implementation effectiveness**. No formal PASS, PARTIAL or FAIL ratings are assigned.

## 1. Research Objective and Boundaries

**Primary question:** Can execution-time authorization remain effective when the actual environment, target, requested object or operation differs from the assumptions under which a task was approved?

The study assesses the source-attributed incident, preserves the pre-existing v4.0 architecture as a frozen specimen, specifies a distinct implementation for experiments, performs incident-aligned and adversarial tests, and adjudicates what each category of evidence supports.

It does **not** reproduce the Anthropic incident, test any live third party, inspect Anthropic's private infrastructure, or deploy a production control. The tests use fictional `.test` targets and in-memory records. Post-freeze technical functionality must never be attributed retroactively to the preserved architecture.

## 2. Historical Incident Evidence

### Sources

- **SRC-001:** Anthropic, *Investigating three real-world incidents in our cybersecurity evaluations*, July 30, 2026. https://www.anthropic.com/news/investigating-incidents-cybersecurity-evals
- **SRC-002:** Anthropic, *An alignment assessment of recent cybersecurity incidents*, September 9, 2026. https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents

The evidence-closure audit identifies:

- **CLM-001:** Environmental assumptions diverged from actual internet connectivity because of an evaluation configuration error.
- **CLM-002:** The model interacted with a real lookalike target without adequate authorization verification.
- **CLM-003:** In the specifically described run, actions progressed through retrieval of email addresses and sensitive user information to an account deletion and chat-history retrieval.

| Published action indices | Source-reported activity |
|---|---|
| 0–1807 | Attempts fictional exercise |
| 1816–1838 | Discovers and interacts with real target |
| 1841–1861 | Downloads user email addresses |
| 1870–1892 | Accesses user data and secrets |
| 1911–1912 | Deletes account and retrieves chat histories |
| 1960–1969 | Loses access |

These are source-attributed descriptions, not independently validated forensic events. The September report updates Anthropic's earlier interpretation of the model's reasoning. This research does not equate interpretations of motivation with proven mental state, nor generalize this individual timeline to all runs.

## 3. Frozen v4.0 Architecture Assessment

The authoritative specimen is `architecture/gae-v4.0-frozen-baseline.png`; `architecture/BASELINE.md` preserves the September 6, 2026 freeze and disallows retroactive modifications. Direct visual review of uploaded representations confirms the following **FROZEN-DESIGN** concepts:

| Layer | Mechanisms explicitly represented | Not thereby demonstrated |
|---|---|---|
| Data foundations, operational context | Ownership, quality, integrity, uncertainty, conflicting signals | Implemented lineage, validated source trust or conflict-resolution software |
| Stage 3 — Decision & Delegated Authority | Decision engine, DSA assumptions, policy version, delegated authority, operational tolerance and decision snapshot | Full principal/action/object/target permission evaluator; replay policy |
| Stage 4 — Environmental State Awareness | Telemetry, system conditions, risk signals, policy updates and authority status | Authenticated, independently verified ESA data |
| Stage 4 — Reconciliation & Materiality | DSA–ESA comparison, material change detection, revalidation need | Exact thresholds, precedence, complete decision freshness |
| Stage 5 — Execution Gate | “Enforce at Bind”; ALLOW, ALLOW WITH MITIGATION, REVALIDATE, ESCALATE, REFUSE/PAUSE | Mandatory interception, complete mediation, production-grade isolation |
| Evidence, audit, monitoring | Decision and execution evidence, conformity assurance, audit/reporting, continuous monitoring and feedback | Durable evidence custody, end-to-end deployed monitoring and business effects |

The design's explicit concepts do not automatically establish the algorithms, enforcement boundaries or operating effectiveness later engineered in the harness. The visual copies were consistent with one another but did not match the GitHub-reported frozen PNG blob hash; their exact binary identity is still open. A hash mismatch alone does **not** demonstrate changes to architecture content.

## 4. Experimental Methodology

**FROZEN-DESIGN:** Features present in the preserved pre-investigation baseline. **HARNESS-SPECIFICATION:** Synthetic schemas, rule sets, execution interfaces and code developed later. **HARNESS-OBSERVATION:** Recorded behavior under executed scenarios. **INFERENCE:** Bounded analytical interpretations. These classifications determine which claims the evidence can support.

**H1:** Synthetic task, agent, approval, delegated permissions, DSA and ESA fixtures, requests and schema validation. The approved baseline action was a `read` of `challenge/approved-value` at `chat.meridian.test`.

**H2:** Deterministic policy evaluation, exact scope validation, explicit prohibited operations, materiality reconciliation, decision precedence and version/context binding. These are **post-freeze specifications**.

**H3:** Mock resource store, controlled Python dispatcher, mock executor and execution-evidence capture including invocation, tool result, resource state and digests. An in-process object-identity capability is not a hardened process boundary.

### H4: Incident-aligned experiments

| Test | Synthetic setup | Observed disposition | Observed effect | Assertions |
|---|---|---|---|---|
| AT-001 | Simulated DSA–ESA network divergence with otherwise allowed read | REVALIDATE | Action held; no executor invocation | 9/9 |
| AT-002 | Lookalike unauthorized target, reconnaissance operation | REFUSE_PAUSE | Mock reconnaissance not invoked | 12/12 |
| AT-003 | Authorized `read` on unauthorized restricted-resource object | REFUSE_PAUSE | No mock restricted-data disclosure | 14/14 |
| AT-004 | Prohibited fictional account deletion | REFUSE_PAUSE | No deletion through gate; account unchanged | 18/18 |

**Total: 53/53 scenario assertions.** The initial AT-002 and AT-004 tests had multiple independent denial reasons; the results cannot isolate any one reason as necessary.

### H5-B: Control isolation

The target-only experiment changed the requested target while leaving operation (`read`), resource and environment unchanged. It yielded `TASK_SCOPE_DENIED` and `DELEGATED_SCOPE_DENIED` without an independent explicit operation prohibition.

A separate eight-case deletion factorial test varied task-scope denial, delegated authorization denial and explicit deletion prohibition in disposable in-memory fixtures. Each independently caused refusal when the others were deliberately relaxed. The all-relaxed control intentionally permitted deletion of a **fictional disposable account**, demonstrating sensitivity to policy configuration, not acceptable operational authorization. **49/49 assertions passed.** These are local observations, not proof of deployed independent layers.

### H5-C: Failure-oriented diagnostic research

| Case | Condition | Result |
|---|---|---|
| TC-001 | Authority revoked before decision | Safe refusal |
| TC-002 | Authority revoked after ALLOW, before execution | Binding rejected |
| TC-003 | ESA stale | Revalidation; no execution |
| TC-004 | ESA missing | Revalidation; no execution |
| TC-005 | Policy versions differ | Revalidation; no execution |
| TC-006 | Request changed after ALLOW | Binding rejected |
| TC-007 | Same decision binding checked twice | No defined replay-use policy; NOT EVALUABLE as a violation |
| TC-008 | Evidence collector fails after approved read | Observed evidence-continuity weakness |
| TC-009 | Internally consistent false ESA | Observed telemetry-authenticity weakness |
| TC-010 | Privileged code modifies local store outside gate | Observed in-process mediation weakness |

**Classification:** 6 safe, 3 observed weaknesses, 1 unresolved contract. **30/30 automated diagnostic/regression tests** passed, including tests that require detection of the weaknesses. TC-007 does not show two actual tool executions. TC-008's read was authorized; evidence collection failed. TC-009 used independent *synthetic* ground truth. TC-010 is privileged in-process test access, not a demonstrated remote exploit. No remediations were silently implemented.

## 5. Cross-Case Research Findings

**F-01 — Authorization continuity depends on valid current state.** The harness holds an otherwise permitted request when injected ESA materially diverges from DSA, but cannot authenticate its own source data.

**F-02 — Reachability does not create permission.** The target-only experiment shows how an accessible but unauthorized target can be refused without a separate forbidden-operation rule; historical prevention remains untested.

**F-03 — Object-specific access matters.** AT-003 demonstrates synthetic denial when the resource changes while `read` remains authorized for a different resource. No real production classification or purpose-limitation system was tested.

**F-04 — Decision validity and execution enforcement are separate.** H3 linked decisions to mock outcomes, while H5-C demonstrated a privileged local bypass of the store and an evidence-collector failure.

**F-05 — Environmental data authenticity is a prerequisite.** TC-009 demonstrates that apparent DSA–ESA consistency can be misleading when ESA is false.

**F-06 — Assurance requires continuity under failure.** TC-008 shows a complete execution evidence record may be missing after a permitted action. Audit integrity cannot be inferred from nominal reporting behavior alone.

**F-07 — Replay policy must be specified before assessing replay failure.** Repeating a valid binding comparison, without an established single-use rule or a second dispatch, does not prove an exploitable replay vulnerability.

## 6. Evidence Sufficiency and Formal Adjudication

| Assessment claim | Supported conclusion |
|---|---|
| Frozen architecture represents state awareness, delegated authority, reconciliation, gate and evidence concepts | Verified in supplied image, with unresolved binary identity |
| Selected preventive behaviors can be engineered and tested in controlled simulation | Supported by H1–H5-B observations |
| Harness behaves safely under all tested failure conditions | Not supported; three weaknesses, one replay-policy gap documented |
| Frozen v4.0 specified every later technical algorithm | Not established from reviewed pre-freeze materials |
| v4.0's corresponding controls operated in an independently validated deployment | Not established |
| v4.0 would have prevented the reported Opus 4.7 incident | Not established |

**AT-001, AT-002, AT-003 and AT-004: INSUFFICIENT EVIDENCE TO DETERMINE FROZEN-ARCHITECTURE IMPLEMENTATION EFFECTIVENESS.** This is an evidence-sufficiency conclusion, not a formal PASS, PARTIAL, or FAIL. Neither an unqualified PASS nor a technical FAIL can be assigned to an original implementation not independently tested; assigning PARTIAL solely because documentation is conceptual would also risk overstating effectiveness.

## 7. Open Limitations

1. Independent original-incident forensic records were not available.
2. The GitHub frozen image and uploaded visual copies have not been confirmed byte-identical.
3. Other frozen technical specifications dating to September 6, 2026 have not been comprehensively established.
4. H1–H3 operate with fictional data and a Python in-process mock store, not production mediation.
5. Trusted network/environment telemetry, complete transactional isolation and non-bypassable interfaces were not demonstrated.
6. Durable evidence capture and independent tamper-evident custody are not established.
7. Reauthorization completion, mitigation, escalation and authorization-replay semantics were not fully exercised.
8. Historical workpapers may contain status statements accurate *when created*; those are not silently rewritten.

## 8. Implications and Future Work

Candidate post-baseline work could study cryptographically attributable ESA sources, policy-bound authorization reuse, independent enforcement and data isolation, audit continuity under collector failure, and explicit reapproval transitions. These should receive separate version identifiers, acceptance criteria, adversarial tests and approval—not be treated as features proven present in the September 6, 2026 baseline.

## 9. Conclusion

The frozen Governance at Execution™ v4.0 design depicts a governance path from assumptions and delegated authority through changing environmental conditions to an execution gate and evidence. The separate synthetic research illustrates how selected authorization and prevention mechanisms can operate and demonstrates why telemetry authenticity, complete mediation and reliable evidence capture require their own assurance tests.

The research supports a method for distinguishing **architectural intent, post-baseline harness behavior, and independently established operational effectiveness**. It does **not** establish prevention of the reported Anthropic incident by the frozen v4.0 architecture. Formal architecture-effectiveness ratings remain unassigned.

## Appendix: Private Research Evidence Index

| Source | Location |
|---|---|
| Frozen baseline declaration | `architecture/BASELINE.md` |
| Frozen specimen | `architecture/gae-v4.0-frozen-baseline.png` |
| Incident evidence audit | `assessment/evidence-closure-audit.md` |
| Diagram-to-evidence register | `assessment/h5d-baseline-verification-traceability-register.md` |
| AT-001–004 evidence | `harness/evidence/runs/at-001-synthetic-evidence.json` through `at-004-synthetic-evidence.json` |
| H5-B control isolation | `harness/evidence/runs/h5b-control-isolation-evidence.json` |
| H5-C diagnostics | `harness/evidence/runs/h5c-trust-boundary-evidence.json` |
| H5-C defect register | `harness/evidence/reports/h5c-defect-and-gap-register.md` |
| H5-D approved sufficiency assessment | `assessment/h5d-final-evidence-sufficiency-assessment.md` |

**External incident sources:** [Anthropic July 30, 2026 disclosure](https://www.anthropic.com/news/investigating-incidents-cybersecurity-evals); [Anthropic September 9, 2026 assessment](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents).

---

**Grace Adjeli**  
**BridgeCore AI LLC**  
*Governance is not what is defined. It is what is enforced at execution.™*
