# Open Science Network — Technical Specification

| | |
|---|---|
| Status | Draft v0.1 — for discussion |
| Date | 2026-11-15 |
| Owner | Ahmet Yildiz |
| Supersedes | The 2024 student prototype in this repository (`Backend/`, `frontend/`), which will not be reused |

## Documents

| # | Document | Content |
|---|---|---|
| 01 | [Overview and scope](01-overview-and-scope.md) | Vision, principles, roles, release scope, non-functional requirements |
| 02 | [Architecture and tech stack](02-architecture-and-tech-stack.md) | Node architecture, data placement, tech stack, deployment |
| 03 | [Federation and governance](03-federation-and-governance.md) | Node identity, signed feeds, admission voting, key management |
| 04 | [Publications, replication and DOI](04-publications-replication-doi.md) | Publication packages, replica placement, audits, DOI registration, indexing |
| 05 | [Editorial workflow](05-editorial-workflow.md) | Fields and boards, manuscript state machine, review, decisions, public record |
| 06 | [Authoring and document model](06-authoring-and-document-model.md) | Rich-text and LaTeX editors, document model, rendering pipeline, import |
| 07 | [Use cases](07-use-cases.md) | Use cases for all actors |
| 08 | [Data model and APIs](08-data-model-and-apis.md) | Entities, event and manifest formats, API surface |
| 09 | [Security, privacy and operations](09-security-privacy-operations.md) | Threat model, permissions, GDPR, anonymity, operations |
| 10 | [Roadmap and open questions](10-roadmap-and-open-questions.md) | Phases, risks, decisions still needed |

Requirement keywords **MUST**, **SHOULD** and **MAY** are used as in RFC 2119. Release tags: **[V1]** first production release, **[V2]**, **[V3]** later releases.

## Confirmed decisions

| ID | Decision |
|---|---|
| D-01 | The 2024 prototype code is not reused. |
| D-02 | The network acts as **one journal for all fields**. There is no master node. |
| D-03 | Accepted papers are published **open access immediately**, with a DOI and their **complete review history** (all versions, reviews, responses, decision letters). Rejected papers stay private unless the author opts in to publishing them. |
| D-04 | Reviewers are **anonymous during review**. Their names become public when the record is published. |
| D-05 | Researcher identity is the **ORCID iD**. No institutional verification in V1. Users can report a person they believe is misrepresenting themselves. |
| D-06 | Editors come from **network-wide editorial boards per subject field**. An editor is never from the author's institution. |
| D-07 | Each publication is stored on **at least R nodes** (default R = 5), placed automatically. Any node may mirror more. When a copy is added anywhere, every node's replica list is updated. |
| D-08 | A non-profit **Open Science Foundation** (working name) is the legal entity that holds the DOI prefix. Every node operator is a member of the Foundation. |
| D-09 | A node joins after **min(N, Q) approvals** from existing nodes, where N is the number of active member nodes and Q is the quorum cap (default 10). Only approvals count; rejection votes are informational. There is no network-level expulsion. |
| D-10 | The LaTeX editor accepts a **restricted LaTeX subset** that maps onto the portal's layout, so every paper renders identically. |
| D-11 | V1 has a **human editor** and a review assistant **stub that returns zero suggestions**. The AI interfaces and feedback data model exist from V1. |
| D-12 | Word and LaTeX file import come in **V2**. |
| D-13 | Node installation and operation must be **easy for a university IT department**. |
| D-14 | Tech stack: **TypeScript throughout** (NestJS backend, React frontend, Tiptap/CodeMirror/Yjs editors, PostgreSQL), delivered as a Docker Compose stack of three containers. The PDF engine (Typst or HTML-to-PDF) is chosen after Phase-0 spike S1 (see 02 §4.3). |

## Assumptions to confirm

These were made by the spec authors to fill gaps. Each one is referenced where it is used.

| ID | Assumption |
|---|---|
| A-01 | Crossref is the DOI registration agency (standard for journal articles; supports peer-review DOIs, reference linking and Cited-by). |
| A-02 | Published content is licensed **CC BY 4.0** by default; CC0 is optional. |
| A-03 | The software is licensed **AGPL-3.0**, so commercial forks must stay open. |
| A-04 | The Foundation obtains one **ISSN** for the network journal. |
| A-05 | The subject taxonomy is the **OECD Fields of Research and Development (FORD)**, two levels, extendable by boards. |
| A-06 | A decision needs at least **2 completed reviews** (configurable per board). |
| A-07 | Title, abstract and keywords are required in English. Full text may be in any language. The UI ships in English and German. |
| A-08 | Publishing and reading are free (no article processing charges). |
| A-09 | Unpublished manuscripts live only on the author's node (and its backups); they are never replicated across the network. |
| A-10 | Reviewers may leave confidential comments for the editor, limited to ethics and conflict issues. These are never published. |
| A-11 | One house citation style per field family (numeric or author–year), chosen by the board. |
| A-12 | Authors can appeal a rejection once, to the board chair of the field. |

## Glossary

| Term | Meaning |
|---|---|
| Network | All admitted nodes together. |
| Node | One installation of the software, run by a member institution. |
| Foundation | The legal non-profit entity behind the network (DOI prefix, ISSN, contracts). |
| Account node | The node where a researcher created their account. Their profile is owned there. |
| Handling node | The node where a manuscript was created. All unpublished data for it lives there. |
| Feed | A node's signed, append-only log of public events, replicated to all nodes. |
| Catalog | Metadata and full text of all publications, held on every node for search. |
| Publication package | Immutable, content-addressed bundle of one published version and its review history. |
| Replica | A complete copy of a publication package on a node. |
| R | Target replication factor (default 5). |
| Q | Admission quorum cap (default 10). |
| Field | A subject area from the taxonomy. Each field has an editorial board. |
| Handling editor | The editor responsible for one manuscript. |
| Reviewer pool | Researchers who opted in to review, with their fields and keywords. |
| Round | One review cycle on one manuscript version. |
| Version of record | The final accepted and published version. |
| SDM | Scholarly Document Model, the canonical internal document format (see 06). |
