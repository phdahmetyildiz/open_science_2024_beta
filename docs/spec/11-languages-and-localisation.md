# 11 — Languages and Localisation

The network serves researchers worldwide. Two things are kept apart in this document:

- **UI language**: the language of the portal's interface, emails and legal texts. It's chosen by each user.
- **Content language**: the language of a paper. It's chosen by the authors and recorded in the paper's metadata.

A German-speaking reviewer can use the German UI to review an English paper. The PDF of that English paper still says "Figure 1" and "References", whatever language the UI is in.

## 1. Scope by release

| Area | V1 | V2 | Later |
|---|---|---|---|
| UI languages | **English, German, French** | More languages, including the first right-to-left UI (Arabic) | Community-driven: any language with enough translation coverage |
| Full text of papers | **English only** | Other languages, starting with a list agreed by the editorial council (for example Spanish, Portuguese, Chinese, Arabic, Hindi, French, German) | Any language |
| Text in other scripts *inside* English papers | **Supported**: names, quotations, terms, place names, in any script | — | — |
| Author names in native script | **Supported** (next to the Latin-script name) | — | — |
| Translated titles and abstracts | Data model ready, not offered in the UI | Optional, in any number of languages | — |
| Search | English full text, plus titles and names in any script | Language-aware search for every supported content language | Cross-language search |

The rule for V1: **papers are limited to English, the system isn't.** Every layer handles every script from the start: storage, editors, rendering, fonts, search indexing of names and titles, and metadata. Enabling a new content language in V2 is then a configuration step, not a redesign.

## 2. Language identification

- Languages are identified by **BCP 47 tags**: `en`, `de`, `fr`, `zh-Hans`, `zh-Hant`, `ar`, `hi`, `ja`, `ru`, `he` and so on.
- Every user-visible text field that can be in a language carries a tag: the document, title, abstract, keywords, taxonomy labels, review texts and notification templates.
- The SDM (06 §2) carries `lang` at document level, and optionally on any block or inline span. For example, a Chinese quotation in an English paper is a span with `lang="zh-Hans"`.

## 3. UI localisation

| Requirement | Specification |
|---|---|
| Framework | ICU MessageFormat via **FormatJS** (react-intl) in the frontend, and the same message catalogues on the server for emails and server-rendered pages. Plurals, gender and select rules follow ICU. |
| Source language | English. Every UI string has a key and lives in the message catalogue. No hard-coded text. |
| Language choice | Order: the user's saved setting, then the browser's `Accept-Language`, then English. A language switcher on every page. |
| Public pages | The language is in the URL (`/de/p/{doi}`, `/fr/search`). Pages carry `hreflang` links for search engines. |
| Formatting | Dates, numbers, lists and relative times through the `Intl` API in the user's locale. Sorting through `Intl.Collator` and PostgreSQL ICU collations. |
| Emails and notifications | Sent in the **recipient's** UI language, not the sender's. |
| Legal texts | Terms, privacy notice and transparency terms exist in every enabled UI language, with legal review. If a translation is missing, the binding version (English) is shown with a notice. |
| Translation workflow | Message catalogues are managed in **Weblate** (open source, hosted by the project). V1 languages get professional review. Other languages are contributed by the community. |
| Enabling a language | A UI language can be enabled when at least 95% of strings are translated and reviewed, and the legal texts are available. Missing strings fall back to English. |
| Right-to-left readiness | From V1, all CSS uses **logical properties** (`margin-inline-start` instead of `margin-left`). Layout direction comes from `dir` on `<html>`. Icons that imply direction are mirrored. V1 ships no RTL UI, but every release is tested with an RTL pseudo-locale. |
| Quality gates in CI | A pseudo-locale with accented, 40% longer strings detects hard-coded text and truncation. An RTL pseudo-locale detects layout errors. Missing keys fail the build. |
| UI fonts | System UI fonts, with **Noto** fonts as fallback for every script, so names in any script display correctly in V1. |

## 4. Text handling requirements (all releases)

These apply to every component that stores, edits, renders or searches text:

1. **Unicode, UTF-8 everywhere.** Input is normalised to NFC. Identifiers (ORCID iDs, DOIs, keys) are compared after normalisation.
2. **Bidirectional text** follows the Unicode Bidirectional Algorithm. Inline spans of the opposite direction are isolated (`<bdi>`, `dir="auto"`), so a Hebrew name in an English sentence, or an English term in an Arabic sentence, doesn't break the layout.
3. **Complex-script shaping** for Arabic, Hebrew, Devanagari (Hindi, Marathi, Sanskrit), Bengali, Tamil, Thai and other scripts, in the browser and in the PDF engine.
4. **Line breaking** by the Unicode line-breaking rules, including scripts without spaces: CJK, and Thai, Lao and Khmer with dictionary-based segmentation.
5. **Hyphenation** per content language, where hyphenation patterns exist.
6. **Math is always left-to-right**, also inside right-to-left text.
7. **Language-specific typography** for the content language: quotation marks, number formatting in the text, and spacing rules (for example French spaces before `:` and `;`).

## 5. Content language

### 5.1 Metadata rules

| Item | Rule |
|---|---|
| Paper language | One per paper (`language` in the manuscript and the manifest). **V1: must be `en`**, enforced when the paper is submitted. |
| English title, abstract and keywords | **Always required**, whatever the paper's language. This makes every paper findable and assessable by an international editor (D-17). |
| Original-language title, abstract and keywords | Required when the paper isn't in English (V2). |
| Translated abstracts | Optional, in further languages (V2). Each is labelled with its language and its translator, which can be the authors or a named translator. |
| Author names | Latin-script name as on ORCID, plus an optional native-script name. Displayed as "Zhang Wei (张伟)". Both are searchable and both are written to JATS and Crossref. |
| Affiliations | Name as in ROR. ROR's names in other languages are shown when the UI is in that language. |

### 5.2 House-style labels

Labels the renderer generates ("Abstract", "Figure", "Table", "References", "Received", "Accepted", "Corresponding author") are localised in the **paper's language**, not the UI language. Each enabled content language needs a reviewed label set before papers in that language can be accepted. Citation formatting uses the CSL locale of the paper's language ("et al.", "and", date formats).

## 6. Editors

| Requirement | Specification |
|---|---|
| Input methods | Full support for input method editors (IME) used for Chinese, Japanese and Korean, in Tiptap/ProseMirror and in CodeMirror, including in collaborative editing. *Tested in spike S6.* |
| Bidirectional editing | Cursor movement and selection work correctly in mixed-direction text in both editors. |
| Marking another language | Rich text: select text, then *Mark language*. LaTeX: `\foreignlanguage{lang}{…}`, the `otherlanguage` environment, and direct Unicode input (as with XeLaTeX/LuaLaTeX). `babel` and `polyglossia` aren't allowed as packages (06 §4.2). The document language comes from the metadata. |
| Spell checking | Browser spell checking, driven by the `lang` attribute of the document and of spans. |
| Search and replace | Unicode-aware and normalisation-aware. |

## 7. Rendering

| Output | Requirements |
|---|---|
| HTML | `lang` and `dir` on the document and on spans. Web fonts are subsetted per page, from the Noto families. |
| PDF | The engine MUST support shaping, bidirectional text, CJK line breaking and font fallback across scripts. Typst has a shaping engine and handles RTL text and CJK; this is *verified in spike S1* together with the alternative engine. Fonts are embedded and subsetted. |
| Fonts | The renderer bundles Noto Serif and Noto Sans in the house style, plus the Noto families for CJK, Arabic, Hebrew, Devanagari and other scripts. CJK fonts are large (hundreds of MB), so font packs are a separate container layer that is downloaded once. |
| JATS | `xml:lang` on the article and on elements, `<trans-title-group>`, `<trans-abstract>`, `<name-alternatives>` for native-script names. |
| Crossref | `language` attribute, original-language title, and native-script names where Crossref's schema allows them. |

## 8. Search

| Release | Approach |
|---|---|
| V1 | PostgreSQL full-text search with the English configuration for full text and abstracts. A `simple` configuration plus trigram indexes (`pg_trgm`) for titles, names and keywords in any script, so "张伟" or "Ελλάδα" can be found. |
| V2 | Non-English full texts need language-aware analysis: CJK segmentation, Arabic and Indic normalisation, stemming for European languages. PostgreSQL doesn't cover this well. V2 adds an external search engine as a node component (OpenSearch with ICU analysis, or Meilisearch). *Choice in V2 design.* |
| All releases | The mandatory English title, abstract and keywords mean that every paper can be found with an English query. |

## 9. Editorial work on non-English papers (V2)

- The handling editor must read the paper's language. Otherwise the editor adds a **co-editor** who does (12 §4). The editor-assignment proposal takes editors' languages into account.
- Reviewers are matched on the languages in their reviewer profile (03 §8). At least one reviewer per round must read the paper's language. All reviewers must if the board's policy requires it.
- The board's policy decides whether reviews and decision letters may be written in the paper's language, or must be in English. Each review is tagged with its language.
- The AI assistance in V2 declares which languages it supports. For other languages it returns no suggestions, and the panel says why.

## 10. Testing

- A **multilingual test corpus**: English papers containing Chinese, Japanese, Korean, Arabic, Hebrew, Hindi, Greek, Russian and Thai text. Mixed-direction paragraphs. Native-script author names. In V2, complete papers in each enabled content language.
- Rendering tests compare HTML and PDF output against reference images for the corpus.
- Editor tests cover IME input and bidirectional cursor movement, with two users editing at the same time.
- UI tests run in every enabled locale, plus the two pseudo-locales.
