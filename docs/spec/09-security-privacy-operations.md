# 09 — Security, Privacy and Operations

## 1. Threat model

| Threat | Example | Mitigation |
|---|---|---|
| Fake node joins | Someone sets up a node to inject content | Admission quorum (03 §5). Foundation membership checked by voters. Every approval is public. |
| Collusion of Q members | Colluding nodes admit more fake nodes | Foundation membership requirement. Local distrust (03 §7). Transparency. Network-level suspension is an open question (10). |
| Forged events | Changing a replica list or a vote | Ed25519 signatures, hash-chained feeds, verification of every event. |
| Tampered copies | A node serves a modified PDF | Content addressing: every file is checked against the signed manifest. Landing pages verify before serving fetched content. |
| Lost or withheld copies | A node silently deletes packages | Storage challenges, repair, R ≥ 5, external archives. |
| Stolen node key | Attacker signs events as a node | Encrypted key storage, rotation, `KeyRecovery` with a cut-off, fork detection. |
| Fake researcher identities | Review rings: an author creates ORCID accounts to review their own paper | Eligibility rule (05 §8.1), conflict checks, at least one reviewer not suggested by the author, editor oversight, reporting, published review histories. |
| Reviewer de-anonymisation during review | Author identifies a reviewer through metadata | Reviewer identity is stored only on the handling node and never sent to author views or across nodes before publication. Uploaded review files are stripped of metadata. Invitations sent to account nodes contain no author-visible data. |
| Leak of unpublished manuscripts | A node in the middle reads drafts | Unpublished data never leaves the handling node (A-09). Guests only see what their manuscript role allows. |
| Malicious uploads | Scripts in SVG, malware in supplementary files | SVG sanitising, malware scan, separate download domain or `Content-Disposition: attachment`, strict Content Security Policy. |
| LaTeX code execution | `\write18` | LaTeX is parsed into the SDM, never executed (06 §4.2). Renderers run sandboxed with no network access. |
| Common web attacks | XSS, CSRF, injection, account takeover | Framework defaults, CSRF tokens, parameterised queries, CSP, ORCID-only sign-in (no passwords stored), rate limiting, security headers. |
| Denial of service | Flooding federation endpoints | Per-peer rate limits, signed requests, caching of public content, optional CDN in front of public pages. |
| Malicious software release | Compromised update | Releases signed with the project key and verified by `osn upgrade`. Reproducible builds as a goal. |

## 2. Authentication

- **Researchers**: ORCID OpenID Connect (authorisation code flow with PKCE). No local passwords. Session cookies are `HttpOnly`, `Secure` and `SameSite=Lax`, with a 12-hour idle timeout and 30 days with "remember me".
- **Node administrators**: researchers with an admin role on that node, plus a required second factor (TOTP or WebAuthn) for admin actions.
- **Nodes**: RFC 9421 HTTP Message Signatures with the node key (08 §6).

## 3. Permissions

| Action | Visitor | Researcher | Author (of M) | Editor (of M) | Reviewer (of M) | Board chair | Node admin |
|---|---|---|---|---|---|---|---|
| Read publications and histories | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ | ✓ |
| Edit manuscript M | | | ✓ (before submission and during revisions) | | | | |
| See frozen versions of M | | | ✓ | ✓ | ✓ (from invitation acceptance) | ✓ (field) | |
| See reviewer identities of M | | | | ✓ | Own only | ✓ (field) | |
| See confidential comments | | | | ✓ | Own only | ✓ (field) | |
| Invite reviewers / decide | | | | ✓ | | ✓ (reassign, appeals) | |
| Write review | | | | | ✓ | | |
| Manage board | | | | | | ✓ | |
| Vote on admissions, distrust nodes | | | | | | | ✓ |
| Handle user reports | | | | | | ✓ (editorial) | ✓ (accounts) |

Node admins have **no** access to manuscript content or reviewer identities through the UI. Database access is a technical fact on every node, so it is covered by the operator agreement with the Foundation (§5) and logged where possible.

## 4. Anonymity of reviewers

- In the author's view, reviewers are "Reviewer 1", "Reviewer 2" and so on, consistently across rounds.
- Notifications to authors never contain reviewer names or account nodes.
- Inbox messages to reviewers' account nodes don't reveal anything to the author.
- Review texts are checked on submission for the reviewer's name, and the reviewer is warned if it appears.
- At publication, the names are revealed (D-04). Reviewers agree to this when they accept the invitation, and they see it again before submitting.

## 5. Privacy (GDPR)

This section is to be confirmed by legal counsel.

| Topic | Specification |
|---|---|
| Controllers | Each node operator is the controller for the accounts and manuscripts it hosts. The Foundation and the node operators sign a **joint controllership and operator agreement** that covers the network-wide public data (reviewer pool, catalog, published records). |
| Lawful basis | Accounts and the workflow: contract (terms of use). Published records, including the names of authors, reviewers and editors: consent given at submission or invitation, plus the public interest in a permanent scholarly record (Art. 6(1)(e), Art. 89 GDPR). |
| Data minimisation | Only ORCID iD, name, email, affiliations and the profile data the user enters. No date of birth, address or phone number. The email address is never replicated. |
| Erasure | Account data, drafts and unpublished manuscripts can be deleted on request. **Published records can't be erased.** They are part of the scholarly record (Art. 17(3)(d), archiving in the public interest), and the terms state this clearly. A person's profile can be anonymised, but their names on published records remain. |
| Retention | Withdrawn and rejected manuscripts (not published by the author): kept for 2 years for integrity investigations, then deleted. Guest sessions: 30 days. Audit logs: 2 years. Report cases: 5 years after closure. |
| Transparency | Privacy notice on every node, using a template provided by the Foundation. The terms and the invitation emails explain the transparency principle (D-03, D-04). |
| Transfers | Nodes outside the EU/EEA receive only public data through feeds. Unpublished data stays on the handling node. Guest access by reviewers from abroad is access to the handling node, not a data transfer to another node. |
| AI | [V2] Unpublished manuscripts may be sent to AI services only if they run on the handling node or on a processor under a data processing agreement, never to services that train on the input without consent. |

## 6. Operations

| Area | Requirement |
|---|---|
| Backups | Nightly encrypted backups of PostgreSQL, the package store and the node key, kept for 30 days. Restore tested monthly by an automated job that reports to the console. |
| Disaster recovery | Public data is recoverable from the network (feeds and replicas). Private data comes only from backups. Target: restore within 24 hours, lose at most 24 hours of private data. |
| Monitoring | Health endpoint and Prometheus metrics. Console alerts for feed lag over 1 hour, replication deficits, failed challenges, disk over 80%, certificate expiry within 14 days, failed backups, and fork proofs. |
| Logging | Structured logs without manuscript content. Personal data in logs is pseudonymised after 30 days. |
| Updates | Signed releases, `osn upgrade`, release notes with protocol compatibility. Security releases are announced on a mailing list for node admins. |
| Support | Administrator documentation, a runbook, and a community forum for operators. The Foundation coordinates incident response across nodes. |
| Testing | A federation test harness that runs a simulated network of 10+ nodes in CI. It covers admissions, partitions, dormancy, key rotation, forks, replication and repair. |
