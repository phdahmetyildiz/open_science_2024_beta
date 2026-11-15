# 07 — Use Cases

Each use case lists actors, preconditions, the main flow, alternatives and exceptions, the result, and the release. References such as "03 §5" point to the specification documents.

## Overview

| ID | Use case | Primary actor | Release |
|---|---|---|---|
| **Network and nodes** | | | |
| UC-N1 | Create the network (genesis) | Node admin (first node) | V1 |
| UC-N2 | Install a node and apply to join | Node admin (applicant) | V1 |
| UC-N3 | Review and vote on an application | Node admin (member) | V1 |
| UC-N4 | Become a member and start operating | Node (system) | V1 |
| UC-N5 | Rotate or recover the node key | Node admin | V1 |
| UC-N6 | Retire a node | Node admin | V1 |
| UC-N7 | Mark another node as distrusted | Node admin | V1 |
| UC-N8 | Upgrade, back up and monitor a node | Node admin | V1 |
| **Researchers** | | | |
| UC-U1 | Sign in with ORCID and create an account | Researcher | V1 |
| UC-U2 | Maintain profile and join the reviewer pool | Researcher | V1 |
| UC-U3 | Report a user | Researcher | V1 |
| UC-U4 | Handle a user report | Node admin / board chair | V1 |
| UC-U5 | Apply to become an editor | Researcher | V1 |
| **Authoring and submission** | | | |
| UC-A1 | Create a manuscript and invite co-authors | Corresponding author | V1 |
| UC-A2 | Write the manuscript together | Authors | V1 |
| UC-A3 | Submit the manuscript | Corresponding author | V1 |
| UC-A4 | Revise and respond to reviews | Corresponding author | V1 |
| UC-A5 | Approve proofs | Corresponding author | V1 |
| UC-A6 | Withdraw a manuscript | Corresponding author | V1 |
| UC-A7 | Appeal a rejection | Corresponding author | V1 |
| UC-A8 | Publish the history of a rejected paper | Corresponding author | V1 |
| UC-A9 | Import a Word or LaTeX file | Author | V2 |
| **Editorial** | | | |
| UC-E1 | Accept an editor assignment | Editor | V1 |
| UC-E2 | Perform the formal check | Editor (V2: AI-assisted) | V1 |
| UC-E3 | Find and invite reviewers | Editor | V1 |
| UC-E4 | Make a decision | Editor | V1 |
| UC-E5 | Manage a board | Board chair | V1 |
| **Review** | | | |
| UC-R1 | Respond to a review invitation | Reviewer | V1 |
| UC-R2 | Write a review with AI suggestions | Reviewer | V1 (stub) |
| **Publication and reading** | | | |
| UC-P1 | Publish an accepted paper | Node (system) | V1 |
| UC-P2 | Replicate and audit publications | Node (system) | V1 |
| UC-P3 | Find, read and cite a publication | Visitor | V1 |
| UC-P4 | Read the review history | Visitor | V1 |
| UC-P5 | Correct or retract a publication | Board chair / editor | V1 |
| UC-P6 | Recover the DOI resolution of a lost node | Node (system) | V1 |

---

## Network and nodes

### UC-N1 Create the network (genesis)

- **Actor:** administrator of the first node (Ahmet Yildiz's node).
- **Preconditions:** node installed (02 §5). The Foundation exists, and its Crossref prefix and credentials are available.
- **Main flow:**
  1. The admin chooses *Create a new network* in the console.
  2. The admin enters the network name, the parameters (Q = 10, R = 5, and the others in 03 §5.1), the initial field taxonomy (OECD FORD) and the initial board chairs (ORCID iDs) designated by the Foundation.
  3. The node appends `Genesis`, `FieldDefined` and `EditorAppointed` (chairs) events to its feed.
  4. The node is the network's only member and is fully operational.
- **Result:** a network with one member. Its ID is the hash of the genesis event.
- **Exceptions:** genesis can only be done once per installation. A node that has joined a network can't create another.

### UC-N2 Install a node and apply to join

- **Actor:** administrator of an applicant institution.
- **Preconditions:** the institution is a Foundation member. It has a domain, a VM, SMTP and an ORCID client.
- **Main flow:**
  1. The admin runs the installer (02 §5.2). A node key is generated.
  2. In the console the admin chooses *Join a network* and enters the URL of any member node.
  3. The node fetches and verifies the network's genesis and feeds, then syncs read-only (pending mode).
  4. The admin fills in the application: institution, country, type, node code, contacts, Foundation membership number and a statement.
  5. The node signs the application and sends it to the member node (the sponsor).
  6. The sponsor validates it (domain control, key proof, unique node code) and appends `AdmissionApplication` with its snapshot of active members.
  7. The console shows the application status: required approvals, approvals so far, informational rejections and their reasons, and the expiry date.
- **Alternatives:** 6a. Validation fails (for example the node code is taken). The sponsor returns the error and the admin corrects the application.
- **Result:** a pending application, visible to all members.

### UC-N3 Review and vote on an application

- **Actor:** administrator of a member node.
- **Preconditions:** an open application whose snapshot includes this node.
- **Main flow:**
  1. The admin receives a console notification and an email.
  2. The admin reviews the details: the institution and its web presence, the Foundation membership, the node's reachability and software version (checked automatically), and the other votes and comments.
  3. The admin chooses *Approve* (with an optional comment) or *Object* (with a required reason).
  4. The node appends `AdmissionApproval` or `AdmissionRejection`.
- **Alternatives:** 3a. The console detects a stale snapshot (03 §5.3). Approving is disabled and the admin is asked to request a re-issue from the sponsor.
- **Result:** a signed vote. Objections are informational only (D-09).

### UC-N4 Become a member and start operating

- **Actor:** node (system).
- **Trigger:** the number of valid approvals reaches `required`.
- **Main flow:**
  1. Every node, including the applicant, finds that the admission rule is satisfied (03 §5.3).
  2. The applicant leaves pending mode and appends its first `Heartbeat` with its storage capacity.
  3. The applicant's admin enters the Foundation-issued Crossref credentials (or has already done so).
  4. Replica placement now includes the new node. It starts fetching the packages it is responsible for (04 §5).
  5. Researchers can now create accounts on the node.
- **Result:** an active member node.

### UC-N5 Rotate or recover the node key

- **Rotation:** the admin starts a rotation. The node generates a new key and appends `KeyRotation`, signed with the old key. Peers switch to the new key from that `seq` on.
- **Recovery:** the key is lost or compromised. The admin generates a new key and applies for `KeyRecovery` through a sponsor, which needs the admission quorum. After approval, events signed with the old key after the declared cut-off are invalid. Alerts are shown on all consoles.

### UC-N6 Retire a node

- **Main flow:** the admin chooses *Retire*. The console shows the publications for which this node holds one of too few copies, and the DOIs it stewards. The node announces `NodeRetired` only after the repair processes have placed enough other copies, or the admin forces retirement after a warning. Stewardship moves to other nodes (UC-P6). Researchers with accounts on the node are asked to move to another node (V2) or are informed that their account will be closed.

### UC-N7 Mark another node as distrusted

- **Main flow:** the admin selects a node and chooses *Distrust* with a reason. Locally, the node stops accepting the distrusted node's new catalog entries and replicas, and leaves it out of placement and quorum counts. An informational event lets other admins see the decision. It can be reversed.

### UC-N8 Upgrade, back up and monitor a node

- Covered in 02 §5.3 and 09 §6. The console shows the available upgrades, the backup status (last success, restore test date), feed lag per peer, replication health and certificate expiry.

## Researchers

### UC-U1 Sign in with ORCID and create an account

- **Actor:** researcher.
- **Main flow:**
  1. The researcher clicks *Sign in with ORCID* on any node.
  2. They are redirected to ORCID, authenticate and authorise. The node receives the ORCID iD and name (OpenID Connect).
  3. If the iD is new to the whole network (not in any account node's directory), the node creates an account and becomes the researcher's **account node**.
  4. The researcher enters and verifies an email address (ORCID often doesn't share it), and accepts the terms and the privacy notice.
  5. The profile is prefilled from the public ORCID record: affiliations, works, education.
- **Alternatives:**
  - 3a. The iD already has an account on another node. The node creates a **guest session** and links to the account node for profile changes (03 §10).
  - 3b. The researcher only wants to read. No account is needed.
- **Result:** a researcher account on the node.

### UC-U2 Maintain profile and join the reviewer pool

- **Main flow:** the researcher edits their profile (bio, fields, keywords, languages, links). They enable *Available as reviewer* and set a capacity (for example 2 reviews per quarter). The account node publishes `ReviewerProfile` (public data only). The researcher can pause their availability or withdraw from the pool at any time (`ReviewerProfileWithdrawn`).
- **Result:** the researcher appears in reviewer search on every node.

### UC-U3 Report a user

- **Actor:** any signed-in researcher.
- **Main flow:** on a profile, review or manuscript page, the researcher chooses *Report*, picks a category (false identity or affiliation, misconduct, harassment, other), and adds a description and evidence. The report goes to the reported person's account node, through the inbox if that's another node. If it relates to a manuscript, it also goes to the board chairs of the field.
- **Result:** an open report case. The reporter receives an acknowledgement. The reported person is not told who reported them.

### UC-U4 Handle a user report

- **Actors:** node admins of the account node (identity and conduct). Board chairs (editorial integrity).
- **Main flow:** the case is assessed, and the reported person can be asked to respond. Possible outcomes: no action, warning, a **reviewer-pool suspension** (published as an event, so editors everywhere see it), suspension of the account, or referral to the institution or the Foundation. Every outcome is documented in the case.
- **Exceptions:** cases affecting published records follow UC-P5.

### UC-U5 Apply to become an editor

- **Main flow:** the researcher selects a field and submits a statement. The board chairs see the ORCID record, publications and review history in the network. A chair (or 2 editors) approves, and `EditorAppointed` is published. Otherwise the application is declined with a reason.

## Authoring and submission

### UC-A1 Create a manuscript and invite co-authors

- **Actor:** researcher, who becomes the corresponding author.
- **Main flow:**
  1. *New manuscript*: choose the article type (research article, review, short communication …), the authoring mode (rich text or LaTeX), and the primary field.
  2. The manuscript is created on the researcher's account node, which becomes its **handling node**.
  3. The author invites co-authors by ORCID iD or email. They receive an invitation and sign in with ORCID on the handling node to accept it.
- **Result:** a draft shared with the co-authors.

### UC-A2 Write the manuscript together

- **Actors:** corresponding author and co-authors.
- **Main flow:** the authors write in the chosen editor (06 §3–4) with live preview, add references by DOI or BibTeX, upload figures with alt text, add cross-references, comment and resolve comments, and take snapshots. The validation panel shows problems continuously.
- **Alternatives:** switch the authoring mode (06 §4.3).
- **Result:** a draft that is ready for submission.

### UC-A3 Submit the manuscript

- **Main flow:**
  1. The corresponding author clicks *Submit*.
  2. The system checks completeness (05 §4) and lists any problems.
  3. All co-authors are asked to confirm their authorship and contributor roles. Submission continues once all have confirmed.
  4. The author accepts the transparency terms. Version 1 is frozen and the state becomes *Submitted*.
  5. Editor assignment starts (UC-E1).
- **Exceptions:** a co-author doesn't confirm within 14 days. The corresponding author can remove them (they are notified) or wait.

### UC-A4 Revise and respond to reviews

- **Precondition:** decision *minor revision* or *major revision*.
- **Main flow:** the author reads the decision letter and the anonymous reviews. They edit the working copy and answer **each** review point (addressed, partially, or not addressed, with an explanation and links to changes). They submit the new version. The system creates the diff, and the editor is notified (05 §10).
- **Exceptions:** deadline missed. Reminders go out, then the editor can extend the deadline or close the manuscript as withdrawn.

### UC-A5 Approve proofs

- **Precondition:** state *Production*.
- **Main flow:** the author checks the rendered HTML and PDF, marks small corrections, and approves. Publication follows (UC-P1).

### UC-A6 Withdraw a manuscript

- Possible in any state before *Accepted*. The author gives a reason. The editor and reviewers with active tasks are notified, and their tasks are cancelled. Nothing is published.

### UC-A7 Appeal a rejection

- Within 30 days of the rejection, the author submits one appeal with a statement. A board chair decides (05 §11).

### UC-A8 Publish the history of a rejected paper

- **Main flow:** after a final rejection (appeal decided or appeal period over), the author can choose *Publish this record*. A preview shows exactly what will become public (05 §13). On confirmation, a **rejected record** package is built, signed and replicated. It has no article DOI (open question, see 10).

### UC-A9 Import a Word or LaTeX file [V2]

- The author uploads a DOCX file or a LaTeX zip. The system converts it (06 §9), creates a draft and shows the import report. The author fixes the reported problems in the editor.

## Editorial

### UC-E1 Accept an editor assignment

- **Actor:** an editor of the manuscript's primary field.
- **Main flow:** the editor receives an invitation (title, abstract, fields, and the reason they were chosen). They sign in to the handling node, confirm they have no conflict, and accept. The state becomes *Formal check*.
- **Alternatives:** the editor declines with a reason, and the next candidate is asked (05 §5). After 3 declines, the board chairs assign someone.

### UC-E2 Perform the formal check

- **Main flow:** the editor goes through the checklist (05 §6). In V2 it is prefilled by the AI formal check. The editor chooses *Passes*, *Return for formal fixes* (with findings) or *Desk reject* (with a reason).
- **Result:** the manuscript moves to reviewer invitation, goes back to the author, or is rejected.

### UC-E3 Find and invite reviewers

- **Main flow:**
  1. The editor opens the reviewer search: a recommendation list, filters for field, keyword, language, availability and eligibility, and author-suggested reviewers marked as such.
  2. Conflicts are excluded automatically, with the reason shown (05 §7).
  3. The editor selects reviewers (at least the board minimum), adjusts the deadline and sends invitations.
  4. The invitations reach the reviewers' account nodes through the inbox (03 §9).
- **Alternatives:** an invitation is declined or expires. The editor is notified and invites a replacement, possibly someone the declining reviewer suggested.

### UC-E4 Make a decision

- **Precondition:** the minimum number of reviews is complete.
- **Main flow:** the editor reads the reviews (including the confidential comments) and the author's responses in later rounds. They choose a decision and write the letter, adding a justification if it goes against the majority of recommendations. The author is notified (05 §9).

### UC-E5 Manage a board

- **Actor:** board chair.
- **Main flow:** appoint and remove editors (UC-U5), reassign stuck manuscripts, set board policies (minimum reviews, deadlines, eligibility rule, citation style), define sub-fields, decide appeals and integrity cases, and view board statistics (load, turnaround, overdue steps).

## Review

### UC-R1 Respond to a review invitation

- **Actor:** researcher in the reviewer pool.
- **Main flow:** the reviewer gets the invitation on their account node's dashboard and by email. They open it on the handling node (signing in with ORCID), read the title, abstract, deadline and transparency terms, declare whether they have a conflict, and accept.
- **Alternatives:** they decline with a reason and optionally suggest someone else. Or they don't answer and the invitation expires after 5 days.
- **Result:** the review task is active, with a deadline.

### UC-R2 Write a review with AI suggestions

- **Main flow:**
  1. The reviewer opens the frozen version in the review workspace: the HTML text with an anchor tool, the PDF, the supplementary files, and in later rounds the diff and the author's responses.
  2. The AI suggestion panel loads. **In V1 the stub returns no suggestions** and the panel says so.
  3. [V2] For each suggestion, the reviewer chooses accept or reject and writes a short explanation (required). Accepted suggestions become editable review points.
  4. The reviewer writes a summary and their own numbered points (major, minor, typo), anchored to passages where useful.
  5. The reviewer chooses a recommendation and optionally adds confidential comments (ethics and conflict issues only).
  6. The reviewer submits. The review is locked, and the editor is notified.
- **Alternatives:** save a draft and continue later, or request an extension.
- **Result:** a completed review, anonymous to the authors and public with the reviewer's name if the paper is accepted.

## Publication and reading

### UC-P1 Publish an accepted paper

- **Actor:** handling node (system), triggered by proof approval.
- **Main flow:** reserve the DOI suffix, build the package with the full history, register the DOI with Crossref, store and sign the package, and append `PublicationPublished` and `ReplicaAdded`. Then notify everyone involved (05 §12).
- **Exceptions:** the Crossref deposit fails. Retry with backoff and notify the node admin. The publication becomes visible only after registration succeeds, so a DOI never points nowhere. If the failure is permanent (for example revoked credentials), the admin and the Foundation are notified.

### UC-P2 Replicate and audit publications

- **Actor:** every node (system).
- **Main flow:** compute responsibility for new packages, fetch, verify, store and announce `ReplicaAdded` (04 §5). Run daily storage challenges and repair packages that are under-replicated (04 §6).
- **Result:** every package keeps at least `r` verified copies. Every node's replica lists stay current.

### UC-P3 Find, read and cite a publication

- **Actor:** visitor.
- **Main flow:** the visitor searches on any node (full text, filters for field, date, author and status), or arrives through a DOI or search engine. They read the HTML version, download the PDF or JATS, and export a citation.
- **Alternatives:** the node has no local copy. It fetches the package from a replica and caches it, which is invisible to the reader apart from slightly longer loading.

### UC-P4 Read the review history

- **Main flow:** on the landing page, the visitor opens *Peer review history*. It shows a timeline of the rounds: for each round, the version (with diff), the signed reviews, the AI suggestions with verdicts, the author's responses point by point, and the decision letter. The visitor can go from any review point to the passage it refers to in that version.

### UC-P5 Correct or retract a publication

- **Correction:** the authors request it, and the editor or board chair approves. A new version package is published (04 §10). Earlier versions stay available, with a banner pointing to the current one.
- **Retraction / expression of concern:** after an integrity investigation (following COPE), the board chair decides. The handling node publishes `PublicationStatusChanged` with the notice. The content stays available with a banner. The Crossref metadata is updated.

### UC-P6 Recover the DOI resolution of a lost node

- **Trigger:** the resolution steward of a DOI has been dormant for 30 days, or has retired.
- **Main flow:** every node computes the next steward deterministically (04 §7.3). That node appends `ResolutionStewardChanged` and updates the URL at Crossref with its own credentials.
- **Result:** the DOI resolves to a live landing page again.
