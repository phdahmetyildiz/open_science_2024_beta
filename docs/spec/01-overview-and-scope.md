# 01 — Overview and Scope

## 1. Problem

Academic publishing is dominated by a few commercial publishers. Researchers write, review and edit for free. Publishers then charge universities for subscriptions or authors for article processing charges, and earn large margins on publicly funded work. Peer review stays mostly closed, so its quality cannot be checked from outside.

## 2. Vision

The **Open Science Network** is "one journal for all". It is a single scholarly journal, run on infrastructure owned by universities and public research institutes:

- Researchers write papers directly in the portal, so every paper has the same clean layout.
- Editors from network-wide subject boards handle submissions. In later releases an AI editor runs formal checks and proposes reviewers.
- Reviewers from the network's pool review the paper, optionally helped by AI suggestions (V2).
- Accepted papers get a DOI and are open access immediately, with their full review history.
- Any university or public institute can run a node. New nodes are admitted by existing nodes, and no node is in charge.

## 3. Principles

| # | Principle | Consequence for the design |
|---|---|---|
| P1 | **No master node** | All shared state lives in signed per-node feeds that every node verifies on its own. No node's database is authoritative for the network. |
| P2 | **Transparency by default** | The whole editorial history of an accepted paper is public and permanent. |
| P3 | **Write in the portal** | Content is structured (not free-form PDF), so it can be rendered uniformly as HTML, PDF and JATS XML. |
| P4 | **Standards over invention** | ORCID for identity, Crossref DOIs, JATS XML, OAI-PMH, CC licences, HTTP Message Signatures. |
| P5 | **Easy to run** | One installer, one container stack, automatic TLS, few moving parts. |
| P6 | **Durability** | Every publication exists on several independent institutions' servers, and can additionally be deposited in external archives. |
| P7 | **AI as an assistant** | AI only makes suggestions. Humans make every decision and must justify accepting or rejecting a suggestion. |

## 4. Roles

| Role | Who | Main capabilities |
|---|---|---|
| Visitor | Anyone, not logged in | Read, search, download and cite publications and their review histories. |
| Researcher | Anyone logged in with ORCID | Profile, reading list, write manuscripts, opt in to the reviewer pool, report a user. |
| Corresponding author | Researcher who owns a manuscript | Invite co-authors, submit, respond to reviews, approve proofs, withdraw. |
| Co-author | Researcher invited to a manuscript | Edit, comment, confirm authorship before submission. |
| Reviewer | Researcher in the reviewer pool | Accept or decline invitations, write reviews, rate AI suggestions. |
| Handling editor | Board member assigned to a manuscript | Formal check, invite reviewers, make decisions. |
| Board chair | Lead of a field board | Appoint editors, handle appeals, reassign manuscripts, oversee integrity cases. |
| Node administrator | Staff of the institution running a node | Install and operate the node, vote on admissions, handle user reports. |
| Node | The software installation (system actor) | Sign events, replicate feeds and publications, serve content. |
| Foundation | Legal entity | Holds the DOI prefix, ISSN and Crossref account; issues credentials to nodes; signs contracts with archives. |

One person can hold several roles. Roles are always scoped: for example, an editor role applies to a field, and an author role to a manuscript.

## 5. Scope by release

### V1 — first production release

- Node installation, genesis of the network, and admission voting.
- The front door: the network's generic URL, served by several nodes, with routing of signed-in users to their account node (D-15).
- Encrypted, restore-only partner copies of every node's private data, and deadlines that pause during handling-node outages (D-16).
- Signed feeds and gossip replication of public data.
- ORCID login. Profiles. Reviewer pool opt-in. Reporting a user.
- Rich-text editor and restricted-LaTeX editor on one document model. Math, figures, tables, references and cross-references.
- Real-time collaboration between co-authors.
- The full editorial workflow with a human editor: formal check, reviewer invitation, review, decision, revisions, appeal.
- Review assistant interface with a stub that returns zero suggestions, plus the feedback data model.
- Simple, non-AI reviewer recommendation based on fields and keyword overlap.
- Production: rendering to HTML, PDF and JATS; author proofs; DOI registration through the Foundation's Crossref account.
- Publication packages, replication with R copies, storage audits and repair.
- A public reading site on every node: landing pages, search across the whole catalog, full review history, citation export.
- OAI-PMH endpoint, Google Scholar meta tags, sitemaps.

### V2

- Word (DOCX) and LaTeX file import.
- AI formal check, AI reviewer recommendation, AI review suggestions.
- DOIs for individual peer-review reports.
- Writing publications to authors' ORCID records (needs ORCID membership).
- Similarity and plagiarism check (Crossref Similarity Check).
- Automatic takeover of a failed node's users and manuscripts by a partner node, so an outage doesn't stall reviews (D-16, 03 §11.6).
- Changing network parameters by vote. Optionally, network-level node suspension (see 10).
- Track changes in the editors.

### V3

- Datasets and software as publication types.
- Post-publication commentary and community review.
- Indexing applications (DOAJ, Scopus, PubMed Central) and usage metrics (COUNTER).
- Federated or central training of the AI models.

### Non-goals

- Uploading a finished PDF as the publication. Content must be written or imported into the document model.
- Paid access of any kind.
- Blockchain or tokens. The trust model is institutional and is enforced with ordinary signatures (see 03).
- Arbitrary LaTeX with custom layouts.

## 6. Non-functional requirements

| ID | Area | Requirement |
|---|---|---|
| NFR-01 | Installability | A new node MUST be installable by one IT administrator in under 2 hours, on one Linux VM, with a documented installer. |
| NFR-02 | Hardware | One node MUST run on 4 vCPU, 8 GB RAM and 250 GB disk for a network of 100k publications. Storage scales with the replica share (see 04 §9). |
| NFR-03 | Availability | The network MUST keep serving every publication while up to R − 1 of its replica nodes are offline. A single node's target is 99.5% availability. |
| NFR-04 | Durability | A publication MUST never fall below R verified replicas for longer than 7 days while at least R nodes are active. |
| NFR-05 | Performance | Landing pages MUST render in under 1 s (p95) from any node holding a replica, and in under 2.5 s from a node that has to fetch from a peer. Search MUST answer in under 1 s (p95) for 1M publications. |
| NFR-06 | Consistency | Public network state (membership, catalog, replica lists) MUST converge on all reachable nodes within 15 minutes under normal conditions. |
| NFR-07 | Security | All node-to-node traffic MUST be TLS-encrypted and signed by the sending node. All public records MUST be verifiable against node signatures. |
| NFR-08 | Privacy | Unpublished manuscripts, reviewer identities during review, and confidential comments MUST never leave the handling node in readable form. Encrypted backups and partner copies are allowed, as long as the holder can't decrypt them (03 §11). |
| NFR-14 | Recoverability | If a node is lost completely, its private data MUST be restorable from a partner copy with at most 15 minutes of data loss. |
| NFR-15 | Front door | The generic URL MUST stay reachable as long as at least one front-door node is healthy. Unhealthy nodes MUST drop out of DNS within 5 minutes. |
| NFR-09 | Accessibility | The UI MUST meet WCAG 2.1 AA. Published HTML MUST use MathML. PDFs SHOULD be tagged. |
| NFR-10 | Internationalisation | The UI MUST be translatable; English and German ship in V1. |
| NFR-11 | Upgradability | Nodes MUST interoperate as long as they are within one major protocol version of each other. Upgrades MUST be applicable without downtime longer than 5 minutes. |
| NFR-12 | Observability | Each node MUST expose health, metrics and federation status to its administrator. |
| NFR-13 | Openness | All code MUST be open source (A-03). Protocols and formats MUST be documented, so independent implementations are possible. |

## 7. Success criteria for V1

1. At least 3 nodes run by different institutions, admitted through the voting protocol.
2. At least 20 papers published end to end with a registered DOI, their full review history, and at least 3 replicas each.
3. Any single node can be switched off without any publication becoming unavailable.
4. A new node can be installed and admitted without help from the core team.
