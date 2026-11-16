# Open Science Network

**One journal for all**: a federated, non-profit publishing platform run by universities and public research institutes, as an alternative to commercial academic publishers.

- Researchers write their papers directly in the portal, in a rich-text editor or a restricted LaTeX editor, so every paper has the same clean layout.
- Editors from network-wide subject boards handle submissions, and reviewers from the network's pool review them. Topics follow the OpenAlex taxonomy, and papers can belong to several topics.
- The portal is multilingual: the interface starts in English, German and French, and papers in other languages and scripts follow after the first release. AI assistance follows in a later release.
- Accepted papers get a DOI and are open access immediately, together with their **complete, public review history**.
- Any university or public research institute can run a node. New nodes are admitted by existing nodes, and there is no master node.
- Every publication is stored on several independent nodes and can be verified against its signed, content-addressed package.

## Status

The project is in the **specification phase** (draft v0.1, November 2026). No code for the new version exists yet.

## Documentation

The technical specification is in [`docs/spec/`](docs/spec/README.md):

| # | Document |
|---|---|
| — | [Index, decisions, assumptions, glossary](docs/spec/README.md) |
| 01 | [Overview and scope](docs/spec/01-overview-and-scope.md) |
| 02 | [Architecture and tech stack](docs/spec/02-architecture-and-tech-stack.md) |
| 03 | [Federation and governance](docs/spec/03-federation-and-governance.md) |
| 04 | [Publications, replication and DOI](docs/spec/04-publications-replication-doi.md) |
| 05 | [Editorial workflow](docs/spec/05-editorial-workflow.md) |
| 06 | [Authoring and document model](docs/spec/06-authoring-and-document-model.md) |
| 07 | [Use cases](docs/spec/07-use-cases.md) |
| 08 | [Data model and APIs](docs/spec/08-data-model-and-apis.md) |
| 09 | [Security, privacy and operations](docs/spec/09-security-privacy-operations.md) |
| 10 | [Roadmap and open questions](docs/spec/10-roadmap-and-open-questions.md) |
| 11 | [Languages and localisation](docs/spec/11-languages-and-localisation.md) |
| 12 | [Topics and publication types](docs/spec/12-topics-and-publication-types.md) |

## Repository layout

| Path | Content |
|---|---|
| `docs/spec/` | Technical specification of the new version |
| `Backend/`, `frontend/`, `.github/workflows/` | **Archived** 2024 student prototype (Flask backend, FastAPI/HTMX frontend). Archived on 15.11.2026. It is not part of the new version and will not be developed further. |

## License

The software license is still to be decided. The specification proposes AGPL-3.0 for the software and CC BY 4.0 for published content (see assumptions A-02 and A-03 in the [spec index](docs/spec/README.md)).
