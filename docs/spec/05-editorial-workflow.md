# 05 — Editorial Workflow

The workflow follows the usual journal process, with three differences: editors come from network-wide boards, AI assistance plugs in at defined points, and the full history of accepted papers is published.

## 1. Where the workflow runs

All workflow data for a manuscript lives on its **handling node**, which is the node where the corresponding author created it. Editors, reviewers and co-authors from other nodes sign in there with ORCID (03 §10). Notifications reach them through their account nodes (03 §9). If the handling node is unavailable, the manuscript waits and its deadlines are extended afterwards (03 §11.5).

## 2. Topics, boards and publication types

### 2.1 Taxonomy and topics

- Topics come from the OpenAlex taxonomy (domain › field › subfield › topic), as specified in 12 §1.
- A manuscript has **one primary topic** and up to 4 additional topics. The primary topic's subfield decides the **responsible board** (12 §2–3).
- Each manuscript has one **publication type** (12 §6). The type decides the required sections and declarations, formal-check items, review questions and default minimum reviews.

### 2.2 Board roles

| Role | Appointed by | Responsibilities |
|---|---|---|
| Board chair (1–3 per board) | Bootstrap: the Foundation's designated chairs. Later: the other chairs of the board. | Appoint and remove editors, handle appeals and integrity cases, reassign manuscripts, set board policies (minimum reviews, citation style, deadlines, enabled publication types), define sub-topics, split or merge board scopes (12 §3.1). |
| Editor | A board chair, or 2 existing editors of the board | Handle manuscripts as handling editor, or as co-editor for another board (12 §4). |

- Researchers can apply to become editors of a board. They declare the topics and languages they can handle (12 §3.2). The application shows their ORCID record and publications to the chairs.
- Appointment and removal are `EditorAppointed` / `EditorRemoved` events in the feed of the approver's account node. Each event names the approving chair or editors. Every node checks the event: the approvers must have held the required role at the time, according to earlier events.
- Board membership, policies and editor load are public.

## 3. Manuscript states

```mermaid
stateDiagram-v2
    [*] --> Draft
    Draft --> Submitted: Corresponding author submits (all co-authors confirmed)
    Submitted --> EditorAssignment
    EditorAssignment --> FormalCheck: Editor accepts assignment
    FormalCheck --> ReturnedForFormalFixes: Issues found
    ReturnedForFormalFixes --> FormalCheck: Author resubmits
    FormalCheck --> Rejected: Desk reject (out of scope / not scholarly)
    FormalCheck --> ReviewerInvitation: Passes
    ReviewerInvitation --> UnderReview: Enough reviewers accepted
    UnderReview --> AwaitingDecision: Enough reviews completed
    AwaitingDecision --> RevisionRequested: Minor or major revision
    AwaitingDecision --> Rejected
    AwaitingDecision --> Accepted
    RevisionRequested --> RevisionSubmitted: Author submits new version + responses
    RevisionSubmitted --> ReviewerInvitation: New round (major, or minor with re-review)
    RevisionSubmitted --> AwaitingDecision: Minor, editor decides alone
    Accepted --> Production
    Production --> Published: Author approves proofs, DOI registered
    Published --> [*]
    Rejected --> Appealed: Author appeals (once)
    Appealed --> AwaitingDecision: Appeal upheld (new editor)
    Appealed --> Rejected: Appeal dismissed
    Rejected --> [*]
    Draft --> Withdrawn
    Submitted --> Withdrawn
    ReviewerInvitation --> Withdrawn
    UnderReview --> Withdrawn
    RevisionRequested --> Withdrawn
    Withdrawn --> [*]
```

Every transition is recorded in the manuscript's timeline with actor, time and reason. After publication the timeline becomes part of the package (`history/timeline.json`), with reviewer identities revealed (D-04).

## 4. Submission

Before a manuscript can be submitted, the system checks that:

- every co-author has confirmed their authorship and contributor roles (by signing in with ORCID and confirming);
- required metadata is complete: English title, abstract and keywords (11 §5.1), primary and additional topics, publication type, licence (A-02), funding, competing interests, data availability statement and ethics statement where applicable;
- the **type-specific requirements** are met (12 §6.2): for example the target DOI of a commentary, the consent statement of a case report, or the dataset or software DOI of a data or software paper, which must resolve;
- the paper's language is **English** (V1, D-17);
- the publication type is enabled by the responsible board;
- the document passes **structural validation**: required sections for the type, every figure and table has a caption and alt text, every citation resolves to a reference, cross-references resolve, and the renderer produces HTML and PDF without errors;
- the author has accepted the transparency terms, which state that the review history will be published if the paper is accepted.

On submission, the current document is frozen as **version 1**. The authors can keep editing a working copy, but the editor and reviewers only see frozen versions.

## 5. Editor assignment

1. The system proposes an editor from the **responsible board** (the board of the primary topic's subfield):
   - excluding conflicts (§7);
   - ranked by topic match (editors who declared the primary topic, then the same subfield, then the rest of the board, 12 §3.2), then keyword overlap, then lowest current load, then randomly;
   - [V2] for non-English papers, only editors who read the paper's language, unless a co-editor covers it (11 §9).
2. The proposed editor receives an inbox invitation with title, abstract, type and topics. The editor accepts within 3 days, or declines with a reason.
3. If they decline or don't answer in time, the next candidate is asked. After 3 failed attempts, the board chairs are notified and assign someone manually.
4. Board chairs can reassign a manuscript at any time, with a recorded reason.
5. For interdisciplinary papers, the handling editor can add up to 2 **co-editors** from the boards of the additional topics (12 §4).

[V2] The AI editor proposes the editor and the reviewers. The editor remains a human who confirms.

## 6. Formal check

The handling editor works through a checklist. In V2 the AI formal check pre-fills it with findings.

| Check | Example findings |
|---|---|
| Scope | Fits the responsible board, is scholarly work. |
| Classification | Publication type and topics are correct. The editor can change them, with a reason (12 §2). |
| Structure | Required sections present for the publication type. Abstract within the word limit. |
| Type-specific items | For example the PRISMA checklist for systematic reviews, consent for case reports, repository checks for data and software papers (12 §6.4). |
| Language | Readable enough for review. |
| References | Plausible, resolvable DOIs, no obvious citation manipulation. |
| Figures and tables | Legible, captioned, alt text present, licensed. |
| Declarations | Ethics approval, consent, funding, competing interests, data availability. |
| Integrity | [V2] Similarity check, image manipulation screening. |

Possible outcomes are *passes*, *returned for formal fixes* (with a list of findings, and the author resubmits without starting a new review round) or *desk rejection* (with a written reason). The formal check result is part of the public history for accepted papers.

## 7. Conflicts of interest

A person may not act as editor or reviewer for a manuscript if they:

- are an author;
- share a current affiliation with any author (from ORCID affiliations and the manuscript's metadata);
- co-authored a publication with any author in the last 5 years (from ORCID works and Crossref, where available);
- declare a conflict themselves (the invitation always asks).

Detected conflicts block the invitation. Self-declared conflicts lead to an automatic decline. The editor sees the reason for every excluded candidate.

## 8. Reviewers

### 8.1 Pool and eligibility

- Researchers opt in to the pool on their profile, choosing topics (prefilled from OpenAlex, 12 §5), keywords, languages and availability (`ReviewerProfile`).
- Because identity is ORCID only (D-05), each board sets an **eligibility rule**. The default: the ORCID record lists at least one work with a DOI whose source is a trusted organisation (for example Crossref auto-update), and the ORCID account is older than 6 months. The editor can override the rule for a specific invitation, with a reason.
- The editor sees eligibility signals for each candidate: account age, works, verified affiliations, past reviews in the network, and any open reports.
- Author-suggested reviewers are allowed and are marked as such. At least one reviewer per round MUST NOT be author-suggested.

### 8.2 Invitation

1. The editor searches the pool. A recommendation list is shown, ranked by topic match across the primary and additional topics (12 §5), then keyword overlap, languages, reviewing history and current load (`ReviewerRecommender`). This is a simple non-AI algorithm in V1 and AI-based in V2.
2. The editor invites at least as many reviewers as the minimum for the publication type (12 §6.2), which the board can raise. Typically that means 3 invitations.
3. The invitation shows the title, abstract, type, topics, deadline (default 21 days) and the transparency terms. It explains that the reviewer's name and report will be published if the paper is accepted.
4. The reviewer **accepts** or **declines**. A decline asks for a reason (no time, out of expertise, conflict, other) and optionally suggests an alternative reviewer.
5. Without an answer within 5 days, the invitation expires and the editor is notified.
6. Reminders go out 7 days and 2 days before the deadline. Reviewers can ask for an extension, which the editor approves or rejects.

### 8.3 Review form

| Section | Content | Visible to author | Public after acceptance |
|---|---|---|---|
| Summary | The reviewer's summary of the paper and its contribution | Yes | Yes |
| Points | Numbered points, each with a category (major, minor, typo/language), a text, and optionally an anchor to a location in the manuscript | Yes | Yes |
| AI suggestions | Suggestions from `ReviewAssistant` with the reviewer's verdict and explanation (§8.4) | Accepted ones appear as points | Yes, all with verdicts |
| Type-specific questions | Questions defined for the publication type (12 §6.5) | Yes | Yes |
| Recommendation | Accept, minor revision, major revision, reject | Yes | Yes |
| Confidential comments | Ethics and conflict concerns for the editor only (A-10) | No | No |

The reviewer reads the frozen version in an HTML viewer, with the PDF available, and can place points directly on passages of the text.

### 8.4 AI review assistant

- Interface: `ReviewAssistant.suggest(manuscriptVersion, publicationType, topics, language, reviewerContext) → Suggestion[]`. A suggestion has an anchor, a category, a text, a rationale and a model version.
- **V1: the stub returns an empty list.** The UI panel exists and shows "No suggestions", so V2 needs no UI change.
- For each suggestion the reviewer MUST choose **accept** or **reject**, and MUST write a short explanation (at least 10 characters). Accepted suggestions become review points, which the reviewer can edit.
- The verdict and explanation are stored as `SuggestionFeedback` and used as training data in V2. For accepted papers, the feedback is published with the review history. For rejected papers, it stays private and is used for training only if the reviewer consented.

## 9. Decisions

1. When the minimum number of reviews is complete, the manuscript moves to *awaiting decision*. The editor can also wait for further reviews.
2. The editor chooses **accept**, **minor revision**, **major revision** or **reject**, and writes a decision letter. The letter is prefilled with all reviews. If co-editors are involved, their recommendations are collected first (12 §4).
3. If the decision goes against the majority of reviewer recommendations, the editor MUST write a justification. It is part of the public record.
4. The author receives the decision letter and all reviews, without reviewer names (D-04).

## 10. Revisions

1. The author edits the working copy, then submits it as a new frozen version (v2, v3 …). The deadline is 30 days for minor and 90 days for major revisions; authors can request an extension.
2. The author MUST respond to **every** review point: *addressed* (with an explanation and links to changed passages), *partially addressed*, or *not addressed* (with a reason). They can add a general response letter.
3. The system generates a **diff** between the versions, shown to editor and reviewers.
4. After a **major revision**, a new round starts. The same reviewers are invited again by default, and the editor can add new ones.
5. After a **minor revision**, the editor decides alone, or opens a new round.
6. A board can set a maximum number of rounds (default 4). After that, the editor must accept or reject.

## 11. Appeal

An author can appeal a rejection **once**, within 30 days, with a written statement (A-12). The board chair either dismisses the appeal with a reason, or upholds it and assigns a new editor, who starts from *awaiting decision*.

## 12. Production and publication

1. **Accepted** puts the manuscript into *production*. The final version is rendered to HTML, PDF and JATS with the house style.
2. The corresponding author reviews the **proofs**. Only corrections of typos and errors are allowed; content changes need the editor's approval. Co-authors are notified.
3. Once the author approves, the handling node:
   1. reserves the DOI suffix;
   2. builds the package (04 §3), including the complete history with reviewer names revealed and signed reports;
   3. registers the DOI with Crossref (04 §7);
   4. stores and signs the package, and appends `PublicationPublished` and `ReplicaAdded`;
   5. notifies authors, editor and reviewers.
4. The publication is immediately readable on the handling node and, within minutes, findable through every node's catalog. Replication to R nodes follows automatically.

## 13. What becomes public

| Item | Accepted papers | Rejected papers (default) | Rejected papers (author opted in) |
|---|---|---|---|
| All submitted versions and diffs | Yes | No | Yes |
| Formal check result | Yes | No | Yes |
| Review reports, points, recommendations | Yes | No | Yes |
| Reviewer names | Yes | No | Yes (reviewers were told at invitation) |
| AI suggestions and verdicts | Yes | No | Yes |
| Author responses | Yes | No | Yes |
| Decision letters, justifications | Yes | No | Yes |
| Editor and co-editor names, co-editor recommendations | Yes | No | Yes |
| Timeline (dates of all steps) | Yes | No | Yes |
| Declined invitations | Only counts | No | Only counts |
| Confidential comments | Never | Never | Never |

A rejected paper whose author opts in is published as a **rejected record**: it has a landing page and the full history, gets no article DOI, and is clearly labelled as not accepted. It is replicated like a publication. *Whether rejected records should get a DOI is an open question (see 10).*

**Withdrawn** manuscripts are never public. Unpublished data is deleted according to the retention policy (09 §5).

## 14. Deadlines and defaults

| Step | Default | Configurable by |
|---|---|---|
| Editor accepts assignment | 3 days | Board |
| Formal check | 7 days | Board |
| Reviewer answers invitation | 5 days | Board |
| Review completed | 21 days | Board, extendable by the editor |
| Editor decision after reviews | 7 days | Board |
| Minor / major revision | 30 / 90 days | Board, extendable by the editor |
| Appeal | 30 days | Network policy |
| Maximum rounds | 4 | Board |

Overdue steps escalate: first to the actor, then to the editor, then to the board chairs.

If the handling node was unavailable, every running deadline is extended by the length of the outage, rounded up to full days, and everyone affected is notified (03 §11.5).

## 15. Notifications

Notifications go through the in-app dashboard and email. Researchers choose immediate or daily-digest emails for non-urgent items. Notifications that carry deadlines (invitations, decisions, revision requests) are always sent immediately.
