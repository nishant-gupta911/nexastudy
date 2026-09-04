# NexaStudy Interview Memory Aid

## 30-second version
NexaStudy is a student study assistant built around RAG. Users upload PDFs, slides, documents, datasets, or images. Python extracts and OCRs the content, chunks and embeds it into ChromaDB, then retrieves and reranks relevant context for Gemini to answer with citations. React is the main client, FastAPI is the API, and answers can become narrated videos. It is a capable local prototype, not yet a secured production service.

## 2-minute version
Remember the pipeline as **Parse -> Store -> Retrieve -> Rank -> Generate -> Remember**. `rag.py` parses supported files, uses Tesseract/Gemini OCR, chunks at 800/150 overlap, and stores cosine embeddings. Queries combine dense retrieval, keyword `$contains`, and feedback; a MiniLM cross-encoder reranks the candidates. Gemini receives retrieved context, recent conversation memory, and corrections, then returns a cited answer. Chroma has separate document, feedback, and memory collections. `api.py` exposes upload, chat, file, stats, feedback, health, and video routes. `App.tsx` provides chat/library/overview views. The main design tradeoff is local simplicity versus missing auth, async processing, tests, observability, and multi-user isolation.

## Core cheat sheet

| Topic | Remember |
|---|---|
| Purpose | Study questions grounded in uploaded material |
| Backend | FastAPI + Uvicorn; engine in `rag.py` |
| Frontend | React 18 + TypeScript + Vite + Tailwind |
| AI | Gemini generation and embeddings; Gemini vision OCR fallback |
| Retrieval | Dense + keyword + feedback, then cross-encoder reranking |
| Store | Persistent Chroma, cosine distance, three collections |
| Memory | Embedded turns per client `session_id`, capped by `MAX_MEMORY_TURNS` |
| Video | Pillow + gTTS + MoviePy, served from `./videos` |
| Auth | None implemented |
| Delivery | Local scripts; no CI, Docker, or production manifest |

## Files to remember
- `rag.py`: the actual system brain.
- `api.py`: REST contract and CORS/static video setup.
- `app.py`: alternate direct Streamlit product.
- `video_gen.py`: answer-to-MP4 pipeline.
- `frontend/src/App.tsx`: primary React workflow.
- `frontend/src/components/ui/claude-style-chat-input.tsx`: file and input controls.
- `.env.example`: model, Chroma, retrieval, OCR configuration.
- `run.sh` / `run.bat`: local startup, with a stale `.venv` assumption.
- `README.md`: feature and setup narrative.
- `PROJECT_DOCUMENTATION.md`: older expanded explanation.

## Key APIs
`GET /api/health`, `/api/stats`, `/api/files`; `POST /api/upload`, `/api/chat`, `/api/feedback`, `/api/generate-video`; `DELETE /api/files/{filename}`; static `GET /videos/{filename}`.

## Key entities and relationships
A document becomes many chunks. A chunk belongs to a source file and content hash. A session has many memory turns. A feedback record belongs to a query/session but is retrieved globally, not tenant-filtered. A chat response contains answer text plus top chunk metadata and scores. A video is derived from an answer and session identifier.

## Top 10 interview facts
1. It is RAG, not fine-tuning.
2. Chroma is persistent local vector storage.
3. Retrieval is hybrid and reranked.
4. OCR has local and Gemini fallback paths.
5. Source/page metadata supports citations.
6. Feedback is stored as searchable correction text.
7. Memory is capped per session.
8. API operations are synchronous.
9. There is no auth or test suite.
10. The strongest next step is secure, observable async productionization.

## Top 10 easy-to-forget details
1. CSV ingestion stores a description and first five rows, not the whole table.
2. Duplicate identity includes filename plus bytes.
3. Reranker failure falls back rather than failing initialization.
4. The client-generated UUID is not authentication.
5. React model choices are not sent to the backend.
6. Pasted text is captured but ignored by the API path.
7. React does not render returned sources.
8. Streamlit expects `video_path`; API returns `video_url`.
9. CORS allows every origin with credentials.
10. `run.sh` uses `.venv`, while docs mention `.venv312`.

## Mnemonics
- **P-S-R-R-G-M**: Parse, Store, Retrieve, Rank, Generate, Memory.
- **D-K-F**: Dense, Keyword, Feedback retrieval.
- **D-F-M**: Documents, Feedback, Memory collections.
- **UI/API/Brain/Media**: React, FastAPI, `rag.py`, `video_gen.py`.

## Final study notes
### What to say in an interview
Use the 30-second version first, then expand using P-S-R-R-G-M. Frame weaknesses as known prototype boundaries and propose concrete fixes.

### What to study next
Review the exact request schemas, Chroma metadata, cross-encoder behavior, and secure deployment remediation.

### Open questions / uncertainties
Expected scale, target hosting, user identity model, and answer-quality targets are not stated.
