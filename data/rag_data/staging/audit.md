# Spanish Lecture 3 corpus review

Status: the Lecture 3 main-material corpus is ready for parent review. This is a 71-page partial corpus, not a complete search database or a claim of tested retrieval quality.

## Artifacts

- `lec03-main.json`: complete Spanish text in the authoritative corpus schema, with the same document ID, section boundaries, 71 page IDs, and canonical page numbers as Japanese commit `1ce722c2816b70ef62891a6378b2478af555e3fd`.
- `provenance.json`: one record for each page, naming the actual supplied Spanish PPTX, its SHA-256, its slide number where available, the Japanese canonical page, and every correction or newly translated addition.
- `graph-terms.json`: all 72 original term IDs/kinds, with Spanish human labels and aliases; existing technical English aliases are preserved exactly. Equivalent translated aliases are deduplicated and the localized title is included as an alias.
- `build_corpus.py` and `build_graph_terms.py`: reproducible local assembly scripts. They read the supplied extraction/source snapshots and write only this language's output directory.

## Sources and page alignment

The provided `Clase 3 - Agentes de IA_es.pptx` and matching PDF have 69 slides/pages. They correspond to the supplied Japanese `draft-1031b` revision. The final Japanese `AIE2026_第3回_AIエージェント_1102.pptx` and authoritative corpus have 71 pages.

The full 69-slide Spanish text was read and checked against the canonical Japanese source. Existing Spanish teaching content and terminology were retained. The mapping was reviewed semantically, not assumed to follow page index:

- Spanish slide 4 corresponds to final Japanese page 3 and requires updated introductory/table text.
- Spanish slide 3 corresponds to final Japanese page 4.
- Final Japanese pages 32 and 58 are newly added and have no supplied Spanish slide. Their text is explicitly marked as newly translated from the final Japanese source.
- Later slides shift by one or two pages. Every mapping is recorded in `provenance.json`.

The JSON `page` field is the canonical Japanese source page. It must not be presented as the page number of the old Spanish PDF. A retrieval/citation layer must use this provenance or identify citations as canonical Japanese source pages until corresponding updated Spanish slides exist. For pages 32 and 58 there is no uploaded Spanish-page citation.

## Corrections against the current source

| Canonical page | Change |
|---|---|
| 1 | Preserve title/author/date/copyright and translate the explicitly transcribed logo. |
| 3 | Update title and introductory explanation; preserve all seven property/agent-effect/part rows, including the expanded example of instructions in read pages/files causing tool use. |
| 4 | Reorder the uploaded agenda and restore full Part 5 and Part 9 labels. |
| 19 | Restore graph axes, ticks, legends, model names, and task-time labels omitted by native PowerPoint text extraction. All restored values come from the Japanese corpus. |
| 24 | Expand MCP in the title and retain the current Lecture 6 reference for its mechanism and use cases. |
| 26 | Add the convenience-versus-security trade-off sentence. |
| 28 | Match the final title, “Fuga de información”. |
| 29 | Add the question of detecting failed/stopped background tasks; correct the inherited Spanish resident-agent cross-reference from Part 3 to Part 2. |
| 31 | Add selection of strong/cheap subagent models, Opus/Haiku examples, cost rationale, and per-subagent model selection. |
| 32 | Translate the complete added tool-search slide: 50 definitions, approximately 55,000 tokens, lazy tool loading, Slack example, and wrong-tool-selection limitation. |
| 34 | Remove the old-draft explanatory line deleted from the final Japanese slide. |
| 36 | Match the generic decision-model title, preserving Jev examples, all probabilities, costs, latency, and limitations; join split visual JSON tokens without changing values. |
| 44 | Restore “constants” alongside evaluation in the `prepare.py` label, omitted from the existing Spanish slide. |
| 50 | Add the three source explanations of risks from cloned repository instructions, unreviewed public skills, and persisted malicious input. |
| 53 | Remove the final old-draft line deleted in the Japanese final, while retaining the source's remaining default-readable key-path labels. |
| 58 | Translate the complete new harness/RSI slide, including permitted improvement targets, questions about evaluation/approval/isolation/stopping, and the qualified Darwin Gödel Machine example. |
| 59 | Restore full Part 5 and Part 9 labels and the added summary about keeping evaluation and stopping outside harness improvement. |
| 70 | Independent review corrected the inherited Spanish inequality to “1/100 o menos”, the timing to “after the September incident”, and restored both limits and stopping in the external-control principle. |

The supplied translation already localizes the illustrative response/comment-language examples into Spanish (canonical pages 9 and 13). These are intentionally retained. Original code identifiers, paths, API names, source names, dates, and numerical examples were preserved. The source's Part 8 cross-references and other dated source assertions were retained rather than independently revised.

## Text handling and checks

- Every page has a nonempty Spanish title and body. IDs, page order, section count and per-section cardinality match the canonical source exactly.
- All 69 supplied Spanish slides are represented; two new final-source pages were translated in full. No slide was summarized away.
- Repeated copyright lines were omitted from retrieval bodies after page 1; the original extraction files and provenance preserve the uploaded originals. The title-page copyright and permission notice remain.
- The only explicit image-text supplement in the authoritative corpus is the title-page logo. Page 19 additionally contains chart text not extracted from native text shapes; that source-grounded chart text was restored. This is not a claim of OCR on every image.
- A scan found no untranslated Japanese characters in output titles, sections, bodies or graph labels/aliases. Japanese filenames in provenance are intentional evidence.
- A cross-check of source code-like identifiers and file/path strings found none omitted from the Spanish bodies.
- Graph term IDs/kinds remain unchanged and every existing technical English alias remains present.
- Numerical examples, uncertainty statements, citations and product/version caveats were reviewed against source. Source assertions have not been externally fact-checked.

## Remaining parent work

The complete configured database needs the other lecture materials. No embeddings, SQLite index, API call, repository edit, package installation, commit, push or publication were performed here. Before release, the parent must combine the remaining validated documents, preserve citation provenance, generate real embeddings with the configured model, and evaluate retrieval on the assembled corpus. Do not treat this partial JSON as the original 214-page search scope.
