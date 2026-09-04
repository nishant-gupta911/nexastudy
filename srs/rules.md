# NexaStudy Rules and Conventions

## Contents
- [Observed rules](#observed-rules)
- [Operational and security rules](#operational-and-security-rules)
- [What not to do](#what-not-to-do)
- [Developer checklist](#new-developer-checklist)
- [Final study notes](#final-study-notes)

## Observed rules

### Coding and module organization
Python modules use type hints, `from __future__ import annotations`, descriptive functions, and a central `NexaStudyRAG` class in `rag.py`. API transport concerns belong in `api.py`; parsing, retrieval, persistence, and model orchestration belong in `rag.py`; video rendering belongs in `video_gen.py`; UI orchestration belongs in `app.py` or `frontend/src/App.tsx`. The frontend uses functional React components, TypeScript types, hooks, and Tailwind utility classes.

Names are descriptive and snake_case in Python (`generate_answer`, `session_id`, `chunk_overlap`) and camelCase in TypeScript (`handleSendMessage`, `statsData`). Constants are uppercase. Metadata keys are stable snake_case names such as `page_or_slide` and `document_id`.

### Input and API rules
Requests are validated with Pydantic fields requiring non-empty strings. Uploads use multipart fields named `files`. Chat requires a client-provided `session_id`. API responses are JSON objects, not raw strings. File deletion uses a path parameter and URL decoding. The frontend expects `/api` as its default API base and sends uploads before chat.

The supported extensions are `.pdf`, `.pptx`, `.docx`, `.txt`, `.md`, `.csv`, `.png`, `.jpg`, `.jpeg`, `.bmp`, and `.webp`. New formats should be added in `_extract_content`, with a clear section label and metadata behavior.

### Data and consistency rules
Document chunks must carry `source`, `chunk_id`, `document_id`, `file_type`, `chunk_index`, `total_chunks`, `page_or_slide`, and `ingested_at`. The content hash combines filename and bytes, so renaming a file changes the identity. New document records should be upserted in batches and preserve the collection's cosine metric.

Memory records require session, role, timestamp, and turn index. Feedback records contain the original question, bad answer, correction, session, timestamp, and query hash. Deleting a file removes all chunks where `source` matches; it does not delete memory or feedback.

### Retrieval and generation rules
Retrieval is intentionally hybrid: dense search plus keyword search plus relevant feedback. Candidate chunks are reranked, limited by `TOP_K_RERANKED`, and inserted into a grounded prompt. Generated answers should cite source filename and page/slide. The prompt tells the model to admit when context does not contain the answer and not expose local paths.

### Error handling rules
Errors should be surfaced with meaningful context. Upload treats each file independently. Model initialization tries candidate model names. The API converts expected operational failures into HTTP errors, while the UI displays a user-facing message. Do not silently discard parsing or model failures when adding new behavior.

### State, security, and environment
The React browser owns the active view, messages, loading/error state, document list, stats, and one generated session ID. Streamlit owns equivalent values in `st.session_state`. The server does not own authenticated identity. Environment secrets belong in `.env`, never source or committed docs. `.env.example` is the configuration contract.

At present, security is a gap rather than a complete rule set: there is no auth, authorization, tenant filtering, file-size validation, rate limiting, MIME verification, or restrictive CORS. These should be mandatory rules before deployment.

### Testing and release
No test framework, lint script, CI workflow, Dockerfile, or release process is visible. The frontend has `build`, but no test command. Until tests are added, a minimum manual check is: start backend, confirm health, upload one supported file, ask a question, list/delete the file, and generate a video.

## What not to do
- Do not expose `.env` or API keys in issue text, demos, logs, or docs.
- Do not assume `session_id` provides security.
- Do not add a parser without handling empty extraction and preserving source metadata.
- Do not block a production request on long OCR, embedding, or video work.
- Do not change collection names or chunk metadata without a migration plan.
- Do not claim the React model selector, thinking toggle, pasted text, or feedback UI is functional; current code does not send/use all of them.
- Do not rely on `run.sh` until the `.venv` versus `.venv312` mismatch is corrected.
- Do not treat `chat_buddy/` as the primary supported implementation.

## Why these rules matter
Stable metadata is what makes citations, deletion, deduplication, and file statistics possible. Separation between API and engine prevents UI-specific behavior from leaking into retrieval. Hybrid retrieval exists because semantic similarity alone can miss exact terms, while keyword matching alone misses paraphrases. Explicit uncertainty matters because the repository has strong prototype capabilities but limited operational controls.

The style favors a single understandable engine over a repository pattern with separate controllers/services/repositories. That is reasonable for a small learning project, but it creates a large class and makes testing and independent scaling harder.

## New developer checklist
1. Read `README.md`, `.env.example`, `api.py`, `rag.py`, and the relevant UI.
2. Confirm the active Python environment and API key without printing secrets.
3. Decide whether the change affects document, feedback, or memory collections.
4. Preserve metadata and source/page lineage.
5. Add or update API validation and frontend response handling together.
6. Handle empty extraction, duplicate uploads, external API failure, and no-document chat.
7. Run frontend build and a focused Python import/smoke check.
8. Update docs when endpoint or configuration behavior changes.

## Common mistakes for newcomers
The most likely mistakes are confusing chunk count with file count, assuming Chroma is a relational schema, treating retrieval distances as reranker scores, forgetting that OCR may call Gemini, believing UI model choices change backend models, and using `video_path` instead of the API's `video_url`.

## Final study notes
### What to say in an interview
Explain that the repository has clear practical conventions around metadata, parsing, retrieval, and UI state, while also honestly identifying missing production rules such as auth, tests, limits, and CI.

### What to study next
Study API versioning, schema migration, secure upload handling, CORS, testing seams for external models, and configuration validation.

### Open questions / uncertainties
There is no formal style guide, owner map, code review policy, or release checklist. Some conventions are inferred from the implementation rather than guaranteed project policy.
