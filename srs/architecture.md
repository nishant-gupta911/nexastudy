# NexaStudy Architecture

## Contents
- [Architecture in plain English](#architecture-in-plain-english)
- [System overview](#system-overview)
- [Components and data flow](#components-and-data-flow)
- [Runtime concerns](#runtime-concerns)
- [Tradeoffs and risks](#tradeoffs-and-risks)
- [Interview explanations](#interview-explanations)
- [Final study notes](#final-study-notes)

## Architecture in plain English
NexaStudy is a local-first student study assistant. A user uploads study files, the backend extracts text, optionally performs OCR, breaks the content into overlapping chunks, creates Gemini embeddings, and stores those chunks in ChromaDB. When the user asks a question, the service retrieves semantically and lexically related chunks, optionally includes prior corrections and recent conversation turns, reranks the candidates, and asks Gemini to produce a cited answer. The answer can also be turned into a narrated MP4.

The primary path is React/Vite -> FastAPI -> `NexaStudyRAG` -> ChromaDB and external Gemini/model services. Streamlit in `app.py` is an alternate interface that calls the same engine directly.

## System overview

```text
Browser (React/Vite)                         Streamlit UI
        | HTTP /api                                  | direct Python calls
        v                                             v
                 FastAPI (`api.py`) -----> `NexaStudyRAG` (`rag.py`)
                                                   |       |       |
                                             ChromaDB  Gemini  CrossEncoder
                                             documents  API    reranker
                                                   |
                                             local videos <- VideoGenerator
```

The repository is a single Python application plus a separate TypeScript frontend, not a distributed microservice system. The database is an embedded persistent Chroma store backed by local files. There are no queues, schedulers, workers, auth services, or external relational database layers visible in the repository.

## Components and responsibilities

| Component | Evidence | Responsibility |
|---|---|---|
| RAG engine | `rag.py` | Parsing, OCR, chunking, embeddings, retrieval, reranking, prompts, memory, feedback, file management |
| HTTP API | `api.py` | Pydantic validation, endpoint orchestration, CORS, static video delivery |
| Streamlit UI | `app.py` | Direct UI over the RAG engine; upload, chat, feedback, document deletion |
| React UI | `frontend/src/App.tsx` | Chat, library, overview, upload, deletion, video playback |
| Chat input | `frontend/src/components/ui/claude-style-chat-input.tsx` | File selection, drag/drop, pasted-text capture, model-like controls |
| Video service | `video_gen.py` | Sections -> Pillow slides -> gTTS audio -> MoviePy MP4 |
| Persistence | `chroma_db/` and `videos/` | Local vector/metadata state and generated files |

## Data flow

### Ingestion
1. The browser sends multipart `files` to `POST /api/upload`.
2. `api.py` reads each upload into memory and calls `rag.ingest_file`.
3. `rag.py` selects a parser by extension. PDF uses PyMuPDF plus embedded-image and rendered-page OCR; PPTX uses `python-pptx`; DOCX uses `python-docx`; CSV uses pandas; images use Tesseract and Gemini vision fallback.
4. Text is cleaned and split with `RecursiveCharacterTextSplitter`, default `chunk_size=800`, `chunk_overlap=150`.
5. Embeddings are generated in batches of 50 and upserted to the document collection with source, file type, page/slide, chunk, and content-hash metadata.
6. A filename plus bytes MD5 prevents duplicate ingestion for the same content.

### Question answering
1. The client sends `{query, session_id}` to `POST /api/chat`.
2. The engine reads the last configured memory turns, performs dense Chroma retrieval, keyword `$contains` retrieval, and feedback retrieval.
3. Duplicate candidates are merged; a cross-encoder reranks them when available, otherwise original candidates are truncated.
4. `build_prompt` provides memory, retrieved context, corrections, citations instructions, and the question to Gemini.
5. The answer is returned with source metadata, chunks, model name, and scores; both user and assistant turns are embedded into memory.

### Video flow
`POST /api/generate-video` obtains either a fresh answer or the last assistant answer from memory, then `VideoGenerator` splits it into sections, renders 1280x720 slides with Pillow, requests gTTS audio, and stitches an MP4 with MoviePy. FastAPI serves `/videos/{filename}` from the local `videos/` folder.

## Database and persistence architecture
Three Chroma collections are created in `NexaStudyRAG.__init__`: the document collection, feedback collection, and memory collection. All use cosine distance. Document records contain chunk text and metadata such as `document_id`, `source`, `page_or_slide`, and `ingested_at`. Feedback stores question, wrong answer, correction, session, timestamp, and query hash. Memory stores role, session, timestamp, turn index, and embedded content. `MAX_MEMORY_TURNS` limits the retained turns per session.

This is convenient for a local portfolio application because it avoids operating a database server. It also means persistence is machine-local, concurrent access is not designed, backups are manual, and there is no tenant boundary.

## Authentication, authorization, errors, and configuration
No authentication or authorization is implemented. `session_id` is a client-provided identifier rather than an identity credential. Every reachable caller can use upload, chat, deletion, feedback, statistics, and video endpoints. CORS is `allow_origins=["*"]` with credentials enabled in `api.py`.

FastAPI validates non-empty request fields through Pydantic. Upload continues processing other files after a per-file exception and reports status in the result. Chat, feedback, deletion, and video failures become HTTP errors. The RAG layer wraps ingestion and model initialization failures with runtime messages. External model calls try configured candidates and fallbacks.

Configuration is loaded from `.env` through `python-dotenv`, with defaults in `rag.py` and examples in `.env.example`. Important settings include model names, Chroma path, chunk sizes, retrieval limits, memory limit, and OCR threshold. Secrets are expected in environment variables, but the local `.env` must be treated as sensitive.

## Deployment and scalability
The visible runtime is local development: Uvicorn on port 8000, Vite on 5173, or Streamlit. `run.sh` and `run.bat` start backend and frontend processes, although they refer to `.venv` while the README uses `.venv312`. There is no Docker, CI, cloud manifest, worker process, or production reverse proxy.

The first scaling limits are synchronous file parsing, OCR, embedding calls, cross-encoder inference, Gemini latency, local Chroma storage, and unbounded in-memory upload bytes. A scalable version would queue ingestion/video jobs, use object storage, isolate users, add a hosted vector store or database, cache embeddings, rate-limit requests, and instrument latency and model failures.

## Tradeoffs and risks
The chosen monolithic engine is easy to understand and deploy locally; a service split would add operational overhead disproportionate to the current repository. Chroma is simpler than a hosted vector database but weak for multi-user production. Hybrid retrieval and reranking improve answer relevance at the cost of extra embedding/model latency. Gemini vision fallback improves scanned-document coverage but adds cost, latency, and privacy exposure. Persistent memory improves conversational continuity but increases data-retention concerns.

Concrete risks include permissive CORS, no auth, no upload limits, no automated tests, no observability, local-only persistence, model/API dependency, and inconsistent video expectations: FastAPI returns `video_url`, while `app.py` looks for `video_path` and a local file.

## Why this architecture?
Likely reasons are educational value, low setup cost, and a desire to demonstrate an end-to-end RAG pipeline. Alternatives included a purely local Ollama design, represented by `chat_buddy/ollam_bot.py`; a no-LLM semantic search design in `chat_buddy/simple.py`; and a cloud chatbot in `chat_buddy/chat_buddyAPI.py`. Gemini was likely preferred for generation, embeddings, and vision in one provider. The tradeoff is provider dependence and API-key/privacy concerns.

## Interview explanations
### 2-minute answer
“NexaStudy is a student-focused RAG system. React sends uploads and questions to FastAPI. The RAG engine extracts text from PDFs, slides, documents, CSVs, and images, uses OCR where necessary, chunks the text, embeds it, and stores it in three Chroma collections for documents, feedback, and conversation memory. For a question it combines vector retrieval, keyword retrieval, and prior corrections, reranks candidates with a cross-encoder, and sends grounded context to Gemini, which returns a cited answer. It is intentionally a local monolith with a React client, so it is easy to run, but it currently lacks authentication, background jobs, automated tests, and production deployment controls.”

### Deep technical answer
Discuss parser-specific extraction, content-hash deduplication, metadata lineage, 50-item embedding batches, hybrid candidate merging, feedback prefixing, reranker fallback, prompt constraints, memory trimming, and the synchronous request path. Then acknowledge that the design is optimized for a single-user/local workflow and identify the queue, storage, isolation, and observability changes needed for 10x scale.

## Final study notes
### What to say in an interview
Lead with the problem and the end-to-end flow. Be explicit that the implementation is a local-first RAG prototype with a strong retrieval pipeline, not a production multi-tenant platform.

### What to study next
Study RAG evaluation, retrieval metrics, prompt-injection defenses, async job architecture, vector-store tenancy, API security, and model cost/latency measurement.

### Open questions / uncertainties
The intended production hosting target, expected user count, ownership of the existing Chroma data, exact frontend proxy behavior, and whether the legacy `chat_buddy` directory is part of the supported product are not defined in code or deployment files.
