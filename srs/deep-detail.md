# NexaStudy Deep Implementation Detail

## Contents
- [Folder and file map](#folder-and-file-map)
- [Critical code path](#critical-code-path)
- [Contracts and edge cases](#contracts-and-edge-cases)
- [Risks and interview walk-through](#risks-and-interview-walk-through)
- [Final study notes](#final-study-notes)

## Folder and file map
- Root `rag.py`: `NexaStudyRAG`; all core RAG behavior.
- Root `api.py`: FastAPI app, Pydantic request models, cached engine, routes, CORS, video static mount.
- Root `app.py`: Streamlit state, upload/sidebar/chat/feedback/video UI.
- Root `video_gen.py`: `Slide` dataclass and `VideoGenerator` pipeline.
- `frontend/src/main.tsx`: React mount point.
- `frontend/src/App.tsx`: browser state, API calls, views, message rendering.
- `frontend/src/components/ui/claude-style-chat-input.tsx`: attachment/paste/control surface.
- `frontend/src/index.css`: fonts, colors, Tailwind theme, animation.
- `.env.example`: configuration keys and defaults.
- `run.sh`, `run.bat`: two-process local startup.
- `README.md`, `PROJECT_DOCUMENTATION.md`: product and setup narrative.
- `chat_buddy/`: historical alternatives; current root `.gitignore` excludes it.
- `chroma_db/`: persistent generated vector state; `videos/`: generated MP4s.

## Important functions and algorithms
`NexaStudyRAG.__init__` loads configuration, validates the Gemini key, initializes Chroma, tests embedding connectivity, tries the cross-encoder, prepares model candidates, and creates the recursive splitter. `_extract_content` dispatches by extension. `_extract_pdf` combines native text, embedded-image OCR, and rendered-page OCR when text is below `OCR_MIN_TEXT_THRESHOLD`. `_batch_embed_documents` limits embedding batches to 50 and sleeps between batches.

`ingest_file` computes an MD5 of filename plus bytes, skips an existing document ID, creates metadata per chunk, embeds, and upserts. `_dense_retrieve` uses query embeddings and Chroma distances. `_keyword_retrieve` extracts up to ten terms longer than two characters and uses Chroma `$contains`. `retrieve` merges candidates by chunk ID and prepends feedback records. `rerank` uses `CrossEncoder.predict` and descending scores; if unavailable it returns candidates in retrieval order.

`save_memory_turn` assigns a turn index, embeds content, and deletes oldest records beyond `MAX_MEMORY_TURNS`. `build_prompt` formats source/page/relevance, memory, feedback, and strict citation/grounding instructions. `generate_answer` tries generation model candidates, stores both turns, and returns answer, sources, chunks, model, and scores.

`VideoGenerator._split_into_sections` uses numbered sections and a 600-character slide limit. `_draw_slide` renders fixed 1280x720 frames. `_build_slides` calls gTTS in a thread with a 15-second join timeout and estimates duration. `_stitch_video` then combines frames and audio; exact MoviePy stitching is in the remainder of `video_gen.py`.

## API contracts
`ChatRequest`: non-empty `query`, non-empty `session_id`. `FeedbackRequest`: non-empty `query`, `bad_answer`, `correction`, `session_id`. `VideoRequest`: non-empty `session_id`, optional query. Upload accepts one or more multipart fields called `files`.

Responses include upload results per file, answer data, aggregate stats, file names, deletion confirmation, feedback status, or video URL. Error status codes include 400 for no-document/no-memory preconditions, 404 for unknown file, 422 for Pydantic validation, and 500 for model/processing failures.

## Important state transitions and edge cases
- No documents -> chat is rejected.
- Duplicate document hash -> zero chunks and success in upload response.
- Unsupported extension -> per-file upload error.
- Empty extraction -> zero chunks.
- Missing Tesseract -> Gemini vision fallback.
- Cross-encoder unavailable -> retrieval-order fallback.
- No feedback -> feedback retrieval is empty.
- Memory overflow -> oldest turns deleted.
- No video query -> last assistant response is extracted from memory.
- No prior assistant memory -> video request is rejected.
- Model candidate failure -> next candidate is tried.
- Chroma SQLite operational error matching `collections.topic` -> store is moved to a timestamped backup and recreated.

Potential edge cases are not fully handled: oversized uploads, malformed PDFs/CSV, duplicate filenames with changed bytes, concurrent ingestion, partial upsert after embedding failure, OCR text quality, prompt injection inside documents, and user deletion semantics for feedback/memory.

## Test strategy and hidden complexity
No test files or test runner are present. The effective test strategy is manual UI use and existing local data. High-value tests should isolate extraction per format, hash deduplication, chunk metadata, retrieval merge/deduplication, reranker fallback, memory trimming, prompt citation rules, API validation, and video response contracts. External Gemini, Tesseract, gTTS, and MoviePy should be mocked in unit tests.

The hidden complexity is external-call orchestration: one upload can trigger OCR, embeddings, Chroma writes, and sleeps; one chat can trigger multiple embedding queries, vector/keyword lookups, reranking, generation, and memory writes. These calls are all synchronous and errors can be expensive or difficult to reproduce.

## Most important 20 files
`rag.py`, `api.py`, `video_gen.py`, `app.py`, `frontend/src/App.tsx`, `frontend/src/components/ui/claude-style-chat-input.tsx`, `frontend/src/index.css`, `frontend/src/main.tsx`, `.env.example`, `requirements.txt`, `frontend/package.json`, `frontend/vite.config.ts`, `run.sh`, `run.bat`, `README.md`, `PROJECT_DOCUMENTATION.md`, `chat_buddy/README.md`, `chat_buddy/ollam_bot.py`, `chat_buddy/simple.py`, and `chat_buddy/chat_buddyAPI.py`.

## Critical path through the code
React send -> `handleSendMessage` -> POST upload (optional) -> POST chat -> `api.chat` -> cached `get_rag` -> `generate_answer` -> `retrieve` -> `rerank` -> `build_prompt` -> Gemini -> `save_memory_turn` -> JSON response -> React message state. Upload follows `api.upload` -> `ingest_file` -> `_extract_content` -> splitter -> embeddings -> Chroma.

## Five hardest parts to understand
1. PDF extraction has three text paths and page-level decisions.
2. Retrieval scores change meaning: Chroma distances versus cross-encoder scores.
3. Feedback is both stored independently and inserted into retrieval/prompt context.
4. Memory is vector storage plus ordered metadata, not a normal chat-history table.
5. Three UI paths do not have identical feature contracts.

## If interviewer asks for a code walk-through
Start at `api.py` models and routes, jump to `rag.py` initialization, then trace `ingest_file` and `generate_answer`. Explain metadata before model calls. Finish with `App.tsx` upload/chat ordering and `video_gen.py` as an optional derived output.

## Questions for original developers
What is the intended deployment target? Are uploaded documents private? Why is there no auth? What is the supported frontend versus Streamlit path? Should React display citations and feedback? What are acceptable Gemini costs and latency? Is CSV preview-only intentional? What are backup/recovery expectations for Chroma and videos? Which model names are tested? Why do startup scripts and README use different virtual environments?

## Final study notes
### What to say in an interview
Walk from endpoint to engine to collection to external model and back. Mention exact edge cases and distinguish implemented behavior from desired behavior.

### What to study next
Read the complete remaining `video_gen.py` stitch implementation, inspect the Vite proxy, and build focused tests around the critical path.

### Open questions / uncertainties
The final MoviePy implementation, local package versions actually used at runtime, and production data volume are not fully established by documentation alone.
