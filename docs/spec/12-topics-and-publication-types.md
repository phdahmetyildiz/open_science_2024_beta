# 12 — Topics and Publication Types

The network is one journal for all subjects. Internally it needs two kinds of structure:

- **Topics**: what a paper is about. They decide which editorial board is responsible, help match editors and reviewers, and make the catalog browsable.
- **Publication types**: what kind of publication it is (research article, review, commentary …). They decide the required sections, declarations, checks and review questions.

## 1. Subject taxonomy

### 1.1 Basis: OpenAlex Topics

The taxonomy is **OpenAlex Topics** (D-18). It has four levels:

| Level | Name | Approx. count | Example |
|---|---|---|---|
| 1 | Domain | 4 | Physical Sciences |
| 2 | Field | 26 | Computer Science |
| 3 | Subfield | about 250 | Artificial Intelligence |
| 4 | Topic | about 4,500 | Topic Modeling and Natural Language Processing |

Reasons for the choice:

- It covers all disciplines, including the humanities and social sciences, with enough depth for editors at level 4.
- It is published under CC0, so the network can copy it and keep a fixed version.
- OpenAlex has already classified most of its catalogue of existing works with these topics. That gives two practical benefits. Reviewers' expertise can be prefilled from their earlier publications (§5). Topics can be suggested for new manuscripts by the same open classifier (V2).

### 1.2 How the network uses it

- **Pinned version.** The network uses a fixed copy of the taxonomy, shipped with the software release as a data file. Every manuscript and publication records the taxonomy version it was classified with. The network never depends on the OpenAlex service at run time.
- **Updates.** A new taxonomy version comes with a software release that includes a **mapping file** from old to new topic IDs. Existing manuscripts and publications keep their original classification and also get the mapped topics, so browsing and search use the current version.
- **Local extensions.** Some boards need finer divisions than OpenAlex topics, for example sections of a very large topic. A board chair can define **sub-topics** below a topic (`TopicExtensionDefined`, signed by the chair's account node). Their IDs have the `osn:` prefix, so they never collide with OpenAlex IDs. Sub-topics are optional for authors.
- **Labels in other languages.** OpenAlex labels are in English. German and French labels ship with V1, translated and reviewed by the boards through the same workflow as the UI (11 §3). Missing labels fall back to English.

## 2. Topics of a paper

| Rule | Specification |
|---|---|
| Primary topic | Exactly one level-4 topic, chosen by the authors. Its subfield decides the **responsible board** (§3). |
| Additional topics | Up to 4 more topics, from any part of the taxonomy. They're used for discovery, browsing, reviewer matching and co-editors. |
| Sub-topics | Optional, for any of the chosen topics that has board-defined sub-topics. |
| Keywords | 3 to 8 free keywords, in English (11 §5.1). Separate from topics. |
| Choosing topics | A searchable picker shows the path (domain › field › subfield › topic) and the topic's description. In V1 it also suggests topics by keyword overlap with the title and abstract. [V2] The AI suggests topics using the OpenAlex classifier. The authors decide. |
| Changes during review | The handling editor can change the topics during the formal check, with a recorded reason. A change of primary topic that moves the manuscript to another board needs that board's chairs to agree. |
| Public display | Published papers show all their topics as browsable links. Topic pages list publications, the responsible board and its editors. |

## 3. Editorial boards

### 3.1 Board scope

- Each board covers a **set of subfields** (level 3). Every subfield belongs to **exactly one board** at any time, so a paper's primary topic always identifies one responsible board.
- At network start, the founding boards are formed per **field** (level 2, 26 boards), and each covers all subfields of its field. In a young network with few editors, chairs can merge several fields into one board.
- As a board grows, its chairs can split off new boards for individual subfields (`BoardDefined`, `BoardScopeChanged`, signed by the chairs' account nodes). Manuscripts already in progress stay with the board they started in.
- Board names default to the subfield or field name and can be changed.

### 3.2 Editors' expertise

- Editors are appointed to a board (05 §2.2). Within the board they declare the **topics** they can handle, in addition to their languages (11 §9).
- Editor assignment (05 §5) prefers editors whose declared topics include the manuscript's primary topic, then the same subfield, then the board in general.

## 4. Interdisciplinary papers and co-editors

When a paper's additional topics belong to other boards, the handling editor can add **co-editors** (D-19):

| Rule | Specification |
|---|---|
| Who | An editor from the board responsible for one of the paper's additional topics. At most 2 co-editors per manuscript. |
| How | The handling editor invites a co-editor through the same assignment process as for editors (05 §5). The co-editor's board receives a proposal, conflict checks apply (05 §7), and the co-editor accepts or declines. |
| When | At any point before the first decision. Typically right after the formal check, so the co-editor can help choose reviewers. |
| Rights | The same visibility as the handling editor, including reviewer identities and confidential comments. Co-editors can invite reviewers. |
| Decision | The handling editor decides. Each co-editor gives a recommendation with a short justification. If a co-editor disagrees with the decision, their note is part of the public record of accepted papers. |
| Reviewers | For papers with co-editors, the editor SHOULD invite at least one reviewer for each board involved. |
| Non-English papers (V2) | A co-editor can also be added for language reasons (11 §9). |

## 5. Reviewers and topics

- Reviewers declare topics in their reviewer profile (03 §8). The profile is **prefilled from OpenAlex**: the node looks up the researcher's OpenAlex author record by ORCID iD and suggests the topics of their works. The researcher confirms or edits them.
- Reviewer recommendation (05 §8.2) scores candidates by topic match: same topic, then same subfield, then same field. Keyword overlap and languages come next. It also covers the paper's additional topics, so interdisciplinary papers get reviewers from each side.

## 6. Publication types

### 6.1 Principles

- Every manuscript has exactly one publication type, chosen when it is created. The editor can change it during the formal check.
- Types are defined in a **type registry**, a versioned data file shipped with the software. New types can be added without code changes for most of their behaviour: required sections, declarations, checks and review questions.
- Boards can **disable** types that don't fit their subject (for example case reports outside medicine and similar fields), and can set length guidelines.
- Every **scholarly type is peer reviewed**. Editorial notices are not peer reviewed, and are labelled as such everywhere: landing page, PDF, JATS and Crossref (D-20).

### 6.2 Types in V1

| Type | Peer reviewed | Purpose | Required beyond the basics | Default minimum reviews | Length guideline |
|---|---|---|---|---|---|
| **Research article** | Yes | Original research | Data availability statement. Methods section where the board requires it. | 2 | None |
| **Review article** | Yes | Narrative or systematic review of existing work | Review subtype (narrative, systematic, meta-analysis). For systematic reviews: PRISMA checklist and search strategy. | 2 | None |
| **Commentary** | Yes | Comment on a published article | Target publication's DOI. Competing-interest statement towards the target's authors. | 1 | 2,500 words |
| **Case report** | Yes | Description of a single case (patient, animal, failure, incident) | Consent statement and de-identification confirmation where people are involved. CARE checklist for clinical cases. | 2 | 3,500 words |
| **Data paper** | Yes | Description of a dataset | Dataset in a trusted repository with a persistent identifier (DOI), its licence, and a methods description of data collection. | 2 | None |
| **Software paper** | Yes | Description of research software | Public source repository, OSI-approved licence, and an archived release with a persistent identifier (for example a Zenodo DOI or Software Heritage ID). | 2 | None |

The basics for every scholarly type are: an English title, abstract and keywords (11 §5.1), topics, authors with contributor roles, licence, funding, competing interests and the ethics statement where applicable.

### 6.3 Editorial notices (not peer reviewed)

| Type | Issued by | Purpose |
|---|---|---|
| **Editorial** | Board chairs, or the editorial council | Statements from the boards: introductions, policies, special collections. |
| **Correction** | Handling editor or board chair (UC-P5) | Notice about a corrected version. Linked to the article. |
| **Expression of concern** | Board chair | Notice about an ongoing integrity investigation. |
| **Retraction** | Board chair | Notice of retraction, with reasons (COPE guidelines). |

Notices get their own DOI and are linked to the affected publication in the network catalog and in Crossref's update metadata (Crossmark). They have a simplified workflow: written by the issuer, checked by a second editor or chair of the same board, then published. There is no review round.

### 6.4 Type-specific workflow behaviour

| Type | Behaviour |
|---|---|
| Commentary | The target can be any DOI. If the target is a network publication, its corresponding author is invited to write a **reply**: a commentary with the subtype *reply*, handled by the same editor and published linked to the commentary. The landing page of the target lists all published commentaries and replies. The responsible board is the board of the target's primary topic for network publications, and otherwise the board of the commentary's primary topic. |
| Case report | Only available in boards that enable the type. The consent statement is checked in the formal check, and the consent documents themselves are never uploaded (privacy). |
| Data paper | The system checks at submission that the dataset DOI resolves. Reviewers get a review question about accessibility, documentation and reusability (FAIR). |
| Software paper | The system checks at submission that the repository and the archived release resolve. Reviewers get review questions about installation, documentation, tests and functionality. |
| Review article | For systematic reviews, the PRISMA checklist is part of the formal check, and reviewers get a question about search strategy and bias assessment. |

### 6.5 Review questions per type

The review form (05 §8.3) gets type-specific questions in addition to summary, points and recommendation:

| Type | Additional questions |
|---|---|
| Research article | Are the methods appropriate? Do the conclusions follow from the results? Are data and code available as stated? |
| Review article | Is the coverage of the literature balanced and current? For systematic reviews: is the search reproducible and is bias assessed? |
| Commentary | Is the critique accurate and fair to the original work? |
| Case report | Is the case novel or instructive? Are consent and de-identification adequate? |
| Data paper | Is the dataset accessible, documented and reusable? Is the collection method sound? |
| Software paper | Does the software install and work as described? Is it documented and tested? Is the research purpose clear? |

### 6.6 Mapping to standards

| Type | JATS `article-type` | Crossref |
|---|---|---|
| Research article | `research-article` | `journal-article` |
| Review article | `review-article` | `journal-article` |
| Commentary (reply) | `article-commentary` (`reply`) | `journal-article`, related to the target |
| Case report | `case-report` | `journal-article` |
| Data paper | `data-paper` | `journal-article`, related to the dataset DOI |
| Software paper | `other`, with "Software paper" as a subject in the publication-type subject group | `journal-article`, related to the software DOI |
| Editorial | `editorial` | `journal-article` |
| Correction | `correction` | `journal-article`, with update metadata on the corrected article |
| Expression of concern | `expression-of-concern` | `journal-article`, with update metadata |
| Retraction | `retraction` | `journal-article`, with update metadata |

### 6.7 Planned later types

| Type | Release | Note |
|---|---|---|
| Letter / short communication | V2 | Short, rapid reports |
| Perspective / opinion | V2 | Peer reviewed, labelled as opinion |
| Methods / protocol | V2 | Including study protocols |
| Replication study | V2 | Linked to the replicated study |
| Registered report | V3 | Two-stage review: the protocol is reviewed and accepted in principle before results exist. This needs a two-stage workflow in the state machine (05 §3). |
