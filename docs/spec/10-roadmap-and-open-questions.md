# 10 — Roadmap and Open Questions

## 1. Phases

### Phase 0 — Foundations and spikes (about 2–3 months)

These prototypes reduce the biggest technical risks before V1 development starts:

| Spike | Question it answers | Exit criterion |
|---|---|---|
| S1 Rendering | Typst or HTML-to-PDF? Can the SDM express papers from 5 different fields? | 10 difficult test papers render correctly to HTML, PDF and JATS. Decision documented. |
| S2 LaTeX subset | Is the subset usable for real papers? | 20 real arXiv papers from different fields: measure how much needs changing to fit the subset. Fewer than 30 minutes of manual work per paper. |
| S3 Federation | Do feeds, gossip and the admission rule work under partitions? | A 10-node simulation in CI with admissions, dormancy, a fork and key rotation. All nodes converge. |
| S4 Replication | Do placement, audits and repair work? | Simulation with 1,000 packages and nodes failing: R copies restored within the target time. |
| S5 Crossref | Can DOIs be deposited with per-node credentials? | Test deposits in the Crossref sandbox under the Foundation's account. |
| S6 Collaboration | Do Yjs, Tiptap and CodeMirror work for both modes? | Two authors editing a 30-page paper in real time without problems. |

Organisational work in parallel: found the Foundation, join Crossref, apply for an ISSN, draft the operator agreement and terms, recruit the founding board chairs.

### V1 (about 9–12 months after Phase 0)

The scope is in 01 §5. Suggested order:

1. Node core: installation, ORCID sign-in, accounts, admin console.
2. Federation: feeds, gossip, genesis, admission, directories.
3. Authoring: SDM, both editors, collaboration, references, figures, rendering.
4. Editorial workflow: boards, submission through decisions, revisions, appeal.
5. Production, packages, DOI, replication, public reading site, search, OAI-PMH.
6. Hardening: security review, accessibility audit, load tests, a pilot with 3 nodes.

### V2 and V3

The scope is in 01 §5. AI work in V2 starts by collecting the reviewer feedback that V1 already records.

## 2. Main risks

| Risk | Impact | Mitigation |
|---|---|---|
| Researchers don't adopt "write in the portal" | No submissions | An excellent editor, import in V2 (consider pulling it forward), LaTeX mode for LaTeX users, a pilot with friendly communities. |
| Recognition (indexing, impact) is missing at the start | Researchers avoid publishing | Get DOAJ, Scopus and Web of Science criteria right from the start. Recruit prominent board chairs. Peer-review DOIs as an incentive for reviewers. |
| Not enough reviewers | Slow turnaround | Public credit for reviews (signed reports, review DOIs). Profile statistics. AI assistance in V2. |
| Governance attack (collusion, D-09) | Fake nodes, loss of trust | Foundation membership requirement and the Crossref credential lever. Revisit network suspension (§3 Q1). |
| Operational burden for institutions | Few nodes | One-command installer, low resource needs, a strong admin console, Foundation support. |
| The restricted LaTeX subset is too narrow for some fields | Lost authors | Spike S2. Board-defined extensions. The SVG route for TikZ. |
| A handling node fails during review | Workflow stalls | Backups in V1, encrypted standby copies in V2. |

## 3. Open questions

| # | Question | Why it matters | Proposal |
|---|---|---|---|
| Q1 | **Should the network be able to suspend or expel a node?** D-09 says no. | Without it, a rogue or compromised node stays a member forever. The only levers are legal (Foundation, Crossref credentials) and local distrust. | Add a network-level *suspension* in V2, with a higher quorum (for example 2Q approvals) and an appeal period. |
| Q2 | Can independent researchers (no institution) or private research organisations run nodes? | Who can join, and Foundation membership rules. | V1: universities and public research institutes only, as stated. Revisit later. |
| Q3 | Do rejected records that authors publish (UC-A8) get a DOI? | Citability vs. diluting the journal's DOI space. | Yes, with a separate content type and a clear "not accepted" label. Decide with the Foundation. |
| Q4 | Can the review history be published while a paper is under review, as a preprint, if the author wants? | Speed and openness vs. reviewer anonymity during review. | Not in V1. Possibly V3. |
| Q5 | Should confidential comments to the editor exist at all (A-10)? | Full transparency vs. reporting ethics concerns safely. | Keep them, limited to ethics and conflict issues, never published. |
| Q6 | Article types and length limits per field? | Formal check rules, house style. | Board-defined, with network defaults. |
| Q7 | Who runs the AI models in V2, and where? Per node, Foundation-hosted, or an external provider? | Privacy of unpublished manuscripts, cost, model quality. | A Foundation-hosted service under a data processing agreement, with the option to run it on a node. Decide during V2 design. |
| Q8 | How do the AI models learn from reviewer feedback? Central training on all feedback, or federated? | Privacy of feedback on rejected papers. | Central training on the feedback of published records, plus consented feedback. |
| Q9 | How is the Foundation funded (Crossref fees, legal, coordination)? | Sustainability. | Membership fees by institution size. Grants from research funders. |
| Q10 | Should the house style, taxonomy and network parameters be governed by node votes, by the Foundation, or by an editorial council? | Network parameter changes need a defined process (V2). | Technical parameters: node vote (2Q quorum). Editorial style and policies: an editorial council of board chairs. |
| Q11 | Is English required for title, abstract and keywords (A-07)? | Indexing vs. support for other languages. | Yes, required, alongside the original language. |
| Q12 | Do researchers need to verify an institutional affiliation to become editors or board chairs? | Trust in editorial roles, given ORCID-only identity. | Yes, for editors: an ORCID affiliation verified by an institution, or confirmation by a chair. Optional for reviewers. |
