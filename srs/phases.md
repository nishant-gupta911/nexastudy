# NexaStudy Phases and Flows

## Contents
- [Likely product evolution](#likely-product-evolution)
- [Runtime user flow](#runtime-user-flow)
- [Rebuild order](#rebuild-order)
- [Final study notes](#final-study-notes)

## Likely product evolution
This sequence is supported by Git history and current files, but exact dates and ownership are not stated.

### Phase 1: retrieval proof of concept
The project appears to have started with simpler chatbot experiments. `chat_buddy/simple.py` performs embedding-based retrieval with SentenceTransformers and Chroma, with no LLM. `chat_buddy/ollam_bot.py` adds local Ollama generation, LangChain loaders, and conversational memory. `chat_buddy/chat_buddyAPI.py` explores a Groq-hosted general chatbot. These are evidence of experimentation rather than the supported product path.

### Phase 2: primary Gemini RAG engine
`rag.py` consolidates format-specific extraction, OCR, Gemini embeddings/generation, Chroma persistence, hybrid retrieval, cross-encoder reranking, feedback memory, and conversation memory. This is the functional MVP: upload a supported document and ask grounded questions.

### Phase 3: interfaces and productization
`api.py` exposes the engine as a REST service. `app.py` provides a direct Streamlit UI. The `frontend/` directory adds a React/Vite workspace with chat, library, overview, uploads, deletion, and video controls. The product is branded as NexaStudy.

### Phase 4: multimodal resilience and video
The current engine adds Tesseract/Gemini OCR fallback for scanned material. `video_gen.py` turns answers into narrated videos. The latest README commit documents the video feature. These later features add user value but also more external dependencies and longer synchronous operations.

## MVP assumptions
The likely MVP assumed one local operator, one shared document store, an available Gemini key, moderate documents, and interactive usage rather than high concurrency. It prioritized breadth of supported formats and retrieval quality over identity, tenant isolation, asynchronous jobs, automated evaluation, and production operations.

## Runtime user flow

### Start-up
1. A developer activates Python, loads `.env`, and starts Uvicorn or Streamlit.
2. The RAG singleton/cache initializes Chroma collections, verifies Gemini embeddings, loads the optional cross-encoder, builds model fallbacks, and configures the splitter.
3. React starts Vite, creates a browser session UUID, and requests `/api/files` and `/api/stats`.

### Upload and initialization of knowledge
1. User selects, drags, or pastes files in the chat input.
2. React uploads files to `/api/upload`; the pasted-text state is currently not transmitted.
3. The server parses by extension, OCRs images when needed, chunks content, batches embeddings, and upserts records.
4. The client refreshes files and stats and keeps the user in chat.

### Main question flow
1. User submits a question; if files are attached, upload completes first.
2. `/api/chat` rejects the request if no document exists.
3. Retrieval gathers dense, keyword, and feedback candidates.
4. Reranking selects up to `TOP_K_RERANKED` chunks.
5. Gemini generates a cited answer from context, memory, and corrections.
6. Memory saves both question and answer. The UI appends the response.

### Save/update and feedback flow
Document deletion verifies the filename is known, deletes matching document chunks, and refreshes UI state. Feedback is fully wired in Streamlit and API, but not in the React UI. Feedback is embedded in a dedicated collection and may influence future retrieval.

### Video and failure flow
A user requests a video with the last answer or an explicit query. The API extracts answer text, generates slides/audio/MP4, and returns a static URL. Failures are returned as HTTP 4xx/5xx and displayed by React. Long-running calls are synchronous, so timeouts are possible. Streamlit's video consumer expects a different response key and is likely broken.

## If rebuilding from scratch
1. Define supported user journeys and security boundaries.
2. Implement a small parser contract and one text format.
3. Add document metadata, Chroma abstraction, and deterministic ingestion tests.
4. Add query retrieval and answer generation with citation contracts.
5. Add session memory and feedback as separate opt-in capabilities.
6. Expose a versioned API with request limits and auth.
7. Build one UI against that API, then add Streamlit only if needed.
8. Move OCR, ingestion, and video to background jobs.
9. Add observability, evaluation datasets, CI, deployment, backups, and retention controls.

This order reduces the risk of building UI features around an unstable retrieval contract. An alternative is to start with the polished React screen, but current code shows that some controls became cosmetic because the backend contract did not evolve with them.

## Why this phased approach makes sense
The current repository demonstrates a natural progression from retrieval experimentation to a reusable engine, API, UI, and media output. The recommended rebuild puts contracts, security, and evaluation earlier because those are the current weak points. A microservice-first order would be worse for the present scale: it would increase operational complexity before the core answer quality and product requirements are measured.

## Final study notes
### What to say in an interview
Describe the project as an incremental RAG build: first prove retrieval, then add generation and memory, then expose it through interfaces, then add OCR and video. Mention that a production rebuild would move authentication, async jobs, evaluation, and tests earlier.

### What to study next
Study vertical-slice delivery, RAG evaluation sets, async task queues, API-first frontend development, and migration strategies for changing chunking or embedding models.

### Open questions / uncertainties
The exact chronology before the visible Git commits, the intended MVP acceptance criteria, and whether video was a core requirement or an exploratory feature are not explicitly documented.
