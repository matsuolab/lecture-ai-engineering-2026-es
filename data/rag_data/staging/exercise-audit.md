# Spanish exercise corpus audit

## Scope and source

Prepared **49 full pages**, with no summary-only replacements:

| Document | Canonical Japanese pages | Prepared Spanish pages | Sections |
|---|---:|---:|---:|
| `lec03-exercise` | 26 | 26 | 1 |
| `lec04-exercise` | 23 | 23 | 1 |

The authority is `source-documents.json`, copied from Japanese `data/rag_data/lectures.json` at commit `1ce722c2816b70ef62891a6378b2478af555e3fd`. Its SHA-256 is recorded in `exercise-validation.json`. The corresponding uploaded Japanese PPTX files have 26 and 23 slides respectively. Every canonical page ID, page number, section boundary, and JSON key is preserved; the section label `全体` is translated as `Contenido completo`.

No Spanish exercise slide decks were present in the supplied archives. All 49 pages are therefore explicitly recorded as `new_translation_from_japanese`. `uploaded_translation` and `uploaded_translation_slide` are `null` on every page. Page numbers identify the Japanese source, **not a Spanish PDF or PPTX**. Each provenance entry records the Japanese file, actual Japanese slide number, file hash, source-page hash, and source commit.

The English Lecture 04 exercise deck has 21 pages, unlike the Japanese 23-page source. It was not used to replace, omit, or reorder Japanese content. The English Lecture 03 deck confirms the author romanization **Yoshiaki Sato** on page 1; the Japanese source remains authoritative for the body.

## Meaning and technical fidelity

- Lecture 03 retains the complete review of Lecture 02; all six exercise steps; basic, implementation and both advanced homework options; deadlines; submission requirements; and troubleshooting.
- Lecture 03 page 3 retains `format_rate` 0.095 → 1.0, `content_rate` 0 → 0.905, 19/21, no regressions, two remaining failures, and the seed/GPU reproducibility caveat. These are explicitly the instructor's source results, not a new experiment.
- Lecture 03 pages 4–6 retain all three failure types; `false` versus the incorrect string `"false"`; 14 training examples, including four without evidence; and splitting paraphrases by template across `train / valid / test`.
- Literal function names, file paths, flags, JSON keys, branch/tag names, environment names, model identifiers, versions and technical output are preserved. Human-facing prompts, comments, docstrings, commit messages and explanatory text are translated.
- Lecture 03 page 16 follows the existing reviewed Spanish `INSTRUCTIONS` and equivalent tool docstring wording. The code is intentionally an excerpt, like its source, rather than an invented complete implementation. The expected session marker is `Lecture NN`, matching the Spanish program.
- Tool approval content retains `requires_approval=True`, `DeferredToolRequests`, `output_type`, waiting before execution, and passing `message_history` when resuming. No claim is made that a pending tool has already executed.
- `make_quiz` retains its incomplete student implementation and missing-term test case `lecture=0`; no homework solution was added.
- ADK and Pi content retains the exact model/package/command identifiers, ADK 2.0 caveat, `--ignore-scripts`, Pi's no-confirmation warning, and the source scope of the homework.
- Lecture 04 retains four LLM criteria, the separately coded session marker, and human labeling of all five. Source pages 10–11 describe four criteria, while pages 8 and 14 explicitly describe five human criteria; that distinction has not been silently rewritten.
- Lecture 04 page 5 keeps the source's **M of N** measurement placeholder without inventing measurements, and distinguishes `tool_calls` 2 → 1 from unchanged `requests=2`.
- Lecture 04 page 15 retains every example fraction/count, `coverage 90%`, `#05`, `#09`, `#10`, missed failures versus false alarms, and the explicit `--model test` / not-a-real-evaluation qualification. The source's illustrative output and interpretation are preserved rather than represented as this work's validation results.
- Lecture 04 page 16 retains the entire before/after rubric example, the undecided-policy case, both permissible pass/fail choices, and the source's illustrative 1 → 0 change. No actual rubric or evaluator was modified or executed.
- Independent review caught an operational formatting issue on Lecture 04 page 16: the added policy had a visual line break between `explicación general` and `(pass)`, whereas the existing Spanish rule-based test grader matches them on one line. The full pass policy is now on one line, and the alternative fail policy explicitly retains `explicación general` and `(fail)` on one line. This preserves the source policy while making the excerpt compatible with the existing localized code.
- The benchmark homework retains 500 / 93 / 3 for SWE-bench Verified; 198 / 4 / 2 and `2311.12022` for GPQA Diamond; 2,500 / 2 and `2501.14249` for Humanity's Last Exam; and the source description of τ²-bench. Source dataset terms-of-use and summary-only submission instructions remain teaching content, not instructions executed by the translation process.

## Intentional localization and normalization

1. Operational course repository URLs on Lecture 03 page 13 and Lecture 04 page 13 target `https://github.com/matsuolab/lecture-ai-engineering-2026-es.git`, as directed by the parent and consistent with the existing Spanish course. Japanese source provenance remains unchanged. Scholarly and third-party documentation URLs are preserved.
2. User prompts and output-marker examples are in Spanish. Lecture 04 page 12 uses `¿Qué es un arnés?` and the orthographic variant `¿Qué es lorá?`, matching existing `data/eval/lec04_cases.jsonl`; the category and exercise purpose are unchanged.
3. Lecture 04 UI references use the actual existing labels `Tengo dudas` and `Guardar y continuar` from Spanish `tools/annotate.py`. The source screenshot transcription is translated as source text; it is not presented as a new Spanish screenshot.
4. Visual line wraps are repaired while preserving table/list relationships and code indentation. Lecture 03 `git fetch` retains its explicit backslash continuation. The visually wrapped Lecture 04 `git fetch` is joined into one executable line. The visually split `sierra-research/tau2-bench` reference is rejoined.
5. Repeated copyright footers are omitted from retrieval bodies after the title pages; Lecture 04's logo-only final page retains its source logo/copyright. Explicit logo/screenshot transcriptions from the canonical source are retained in translated form.

## Checks and limits

`python build_exercises.py` regenerates the two corpus files, separate per-page provenance files, and `exercise-validation.json`. It checks exact page ID/order coverage, cardinality, section counts, schema keys, nonempty titles/content, presence and slide counts of the Japanese input decks, and absence of untranslated Japanese in retrieval content. It records artifact hashes and confirms zero fabricated uploaded-Spanish slide mappings. A source-to-target pass reviewed all 49 pages, with focused comparison of numbers, commands, warnings, evaluation criteria, and homework requirements.

No unresolved omission or translation ambiguity remains after the page 16 review correction described above. Numeric strings written as Spanish words (for example, `una semana`, `dos lugares`, `décimo ejemplo`) preserve their original meaning. The English-language agent completed an independent review of all 49 pages and provenance, rechecked both page 16 regex-compatible examples, and returned **PASS** in `../en/independent-review-es-exercises.md`.

These are prepared, auditable retrieval-source artifacts. No course-repository files, APIs, model evaluations, embeddings or databases were modified or executed. No runtime/UI or retrieval-quality result is claimed. Integration and retrieval validation belong to the parent task; missing materials for other lecture documents remain outside this artifact scope.

## Files

- `lec03-exercise.json`
- `lec03-exercise-provenance.json`
- `lec04-exercise.json`
- `lec04-exercise-provenance.json`
- `build_exercises.py`
- `exercise-validation.json`
- `exercise-audit.md`
