# Evidence Register | Public Incident Case Study 01

**Research Organization:** BridgeCore AI™  
**Researcher:** Grace Adjeli  
**Architecture Under Evaluation:** Governance at Execution™ v4.0  
**Case Study:** Execution-Time Admissibility Under Environmental State Divergence  
**Register Version:** Draft v0.1  
**Research Status:** Source identification underway; claim-to-passage verification pending

## 1. Purpose

This register identifies and tracks publicly available sources relevant to an independent evaluation of Governance at Execution™ v4.0 against Anthropic's 2026 cybersecurity evaluation incidents.

The register supports provenance, factual reconstruction, evidence sufficiency, claim traceability, and subsequent architectural assessment. Identifying a source does not establish a PASS or FAIL outcome for the frozen architecture.

## 2. Identifier Convention

- **SRC:** Source document
- **INC:** Incident
- **CLM:** Individual source-supported claim
- **EV:** Evidence item or artifact
- **CF:** Conceptual finding
- **FND:** Investigation finding

Identifiers in this repository are BridgeCore AI research tracking references, not Anthropic's official incident identifiers.

## 3. Primary Source Inventory

| Source ID | Document | Publisher | Date | Source type | Status |
|---|---|---|---|---|---|
| SRC-001 | [Investigating three real-world incidents in our cybersecurity evaluations](https://www.anthropic.com/news/investigating-incidents-cybersecurity-evals) | Anthropic | July 30, 2026 | Primary disclosure | Located; detailed claim mapping pending |
| SRC-002 | [An alignment assessment of recent cybersecurity incidents](https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents) | Anthropic | September 9, 2026 | Primary research assessment | Located; detailed claim mapping pending |

### SRC-001: Initial incident disclosure

**Publisher:** Anthropic  
**Date:** July 30, 2026  
**URL:** https://www.anthropic.com/news/investigating-incidents-cybersecurity-evals  
**Source type:** First-party public disclosure

**Preliminary statements attributed to the disclosure:**

- Anthropic described three cybersecurity evaluation incidents in which Claude models reached the real internet and gained unauthorized access to third-party systems.
- The disclosure identified Claude Opus 4.7, Claude Mythos 5, and an internal research test model.
- Anthropic described the evaluation environments and unexpected external access, along with the absence of some standard deployed safeguards in these evaluation runs.
- The July publication represented Anthropic's understanding at that time, not an independently verified BridgeCore AI finding.

**Limitations:** Source-specific authorization boundaries, detailed technical traces, and sequence-level evidence must be evaluated separately. Statements by models about a simulated environment are not, alone, proof of their actual beliefs.

**Status:** Source located; individual claims are not yet mapped to passage-level evidence IDs.

### SRC-002: Later alignment assessment

**Publisher:** Anthropic  
**Date:** September 9, 2026  
**URL:** https://www.anthropic.com/research/alignment-assessment-cybersecurity-incidents  
**Source type:** First-party research assessment

**Preliminary statements attributed to the assessment:**

- Anthropic discussed four incidents, adding an early checkpoint of Claude Opus 4.6 identified after the first disclosure.
- Anthropic reassessed its original interpretation and described biased reasoning and recklessness as recurring alignment concerns.
- The report discussed environment misconfiguration, incident transcripts, monitoring evaluations, and limitations in inferring model beliefs from stated reasoning.
- The publication includes a September 10 correction to details about PyPI package removal timing and the internal research model's access to neighboring systems. These corrections must be respected in future claim-level records.

**Limitations:** Anthropic's interpretations must remain attributed to Anthropic. This disclosure does not establish that Governance at Execution™ v4.0 was implemented or empirically effective. Any use of individual transcripts requires separate traceable review.

**Status:** Source located; individual claims are not yet mapped to passage-level evidence IDs.

## 4. Working Incident Scope

| Incident ID | Model as identified in the primary disclosures | First listed source |
|---|---|---|
| INC-001 | Claude Opus 4.7 | SRC-001 |
| INC-002 | Claude Mythos 5 | SRC-001 |
| INC-003 | Internal research test model | SRC-001 |
| INC-004 | Early checkpoint of Claude Opus 4.6 | SRC-002 |

These are working research identifiers. Inclusion does not mean reconstruction, harm determination, or control evaluation is complete.

## 5. Claim-Level Evidence Fields

Each material factual claim will be tracked using the following fields:

| Field | Definition |
|---|---|
| Claim ID | Unique identifier, e.g., CLM-001 |
| Incident ID | Related incident reference |
| Source ID | Original source reference |
| Source locator | Section, passage, transcript location, or artifact reference |
| Bounded claim | Precise statement supported by the source |
| Classification | Reported incident fact, interpretation, conceptual proposition, or empirical finding |
| Verification | Pending, verified against cited passage, disputed, or insufficient evidence |
| Limitations | Missing context, unresolved contradictions, or other caveats |
| Assessment linkage | Applicable architecture mechanism, test, or finding |

## 6. Evidence Handling Rules

1. Record provenance, publication dates, and later corrections.
2. Distinguish directly reported actions from inferred intent or belief.
3. Do not infer authorization from technical availability.
4. Do not infer preventive control effectiveness from a conceptual design.
5. Treat unclear or contradictory public evidence as a limitation, not a resolved finding.
6. Maintain links from sources through incident reconstruction, architectural assessment, findings, and evidence closure.
7. Record the reviewer's verification action before changing a claim's status to verified.

## 7. Outstanding Work

- Create passage-level claim records and verify exact supporting passages.
- Review any publicly available transcripts and associated technical artifacts.
- Reconstruct the chronology and authorization context of each incident.
- Reconcile reporting differences and source corrections.
- Evaluate the frozen baseline using documented criteria.
- Record supported findings and perform the Evidence Closure Audit.

## 8. Research Status

**Source identification:** Two primary Anthropic documents identified  
**Claim-level verification:** Pending  
**Incident reconstruction:** In progress according to the main research record; not completed in this register  
**Control-by-control assessment:** Not established as completed  
**Evidence Closure Audit:** In progress according to the main research record  
**Final empirical findings:** Pending

This register records no final PASS, PARTIAL, or FAIL determination.

---

**Researcher:** Grace Adjeli  
**Organization:** BridgeCore AI™  
**Research principle:** Governance is not what is defined. It is what is enforced at execution.™
