# NexaStudy Reverse-Engineered Requirements

## Contents
- [Explicit requirements](#explicit-requirements)
- [Inferred requirements](#inferred-requirements)
- [Missing requirements](#missing-but-likely-required-requirements)
- [Final study notes](#final-study-notes)

## Explicit requirements visible in code and docs

### Functional requirements
- Users can upload PDF, PPTX, DOCX, TXT, MD, CSV, PNG, JPG/JPEG, BMP, and WEBP files (`README.md`, `rag.py`).
- The system extracts text, tables, slide/page context, and image text through OCR.
- Users can ask questions about uploaded content and receive Gemini-generated answers with source/page citations.
- The system supports multi-turn memory by `session_id`.
- Users can list and delete ingested files.
- Users can submit corrections through the API and Streamlit UI.
- Users can generate a narrated video from a current or previous answer.
- Users can inspect health and aggregate stats.
- React provides chat, library, and overview views.

### Non-functional requirements evidenced by implementation
- Configuration must be environment-driven through `python-dotenv`.
- Chroma persistence must survive process restarts locally.
- Embedding calls are batched in groups of 50.
- Retrieval and memory are bounded by configuration values.
- The UI should work on desktop and mobile layouts.
- The API should accept cross-origin frontend requests.

### Users and roles
The code only clearly models one user type: a student/operator. The product language suggests learners, researchers, and self-study professionals, but no role database or permissions exist. There is no admin role in the implementation.

## Inferred requirements
The product likely requires grounded answers rather than generic chatbot replies, which explains context-only prompt instructions and inline citations. It likely needs to handle scanned academic material, which explains two-level OCR and page rendering. It likely values fast setup and low operational cost, which explains local Chroma, direct Uvicorn/Streamlit startup, and one Python engine. It likely aims to demonstrate modern AI engineering breadth, which explains feedback memory, cross-encoder reranking, multiple UIs, and video generation.

The data model implies document lineage is important: users need to know which file/page supported a response, and deletion must remove all chunks of a source. The feedback collection implies the product requires learning from explicit corrections, though it does not implement formal evaluation or model training.

## Business rules
- Chat is blocked until at least one document exists.
- Duplicate file content is skipped.
- Empty extracted content produces zero chunks.
- Answers should state when the uploaded context does not contain the answer.
- Memory is trimmed to the newest configured turns.
- Only a configured number of top candidates are passed to generation.
- File deletion is by exact stored filename.
- Video generation can use the last assistant turn when no query is supplied.

## Performance, reliability, and security expectations
The code suggests interactive response latency is expected, but no numeric SLO exists. Reliability depends on Gemini availability, embedding availability, local storage integrity, OCR tools, and cross-encoder loading. The fallback model lists improve resilience, while synchronous work creates timeout risk.

Security expectations are mostly absent from implementation. A real deployment would require authentication, authorization, per-user document scoping, restrictive CORS, upload size/type validation, malware/content checks, rate limits, secret rotation, prompt-injection handling, safe logging, and data deletion/retention policy.

## Integration and operations requirements
Required integrations include Gemini API for embeddings/generation/vision, optional system Tesseract, Hugging Face model download for the cross-encoder, gTTS, and MoviePy/FFmpeg behavior for video. Operations require persistent Chroma and video directories, a Python environment, Node dependencies, and a valid Gemini API key. There are no visible reporting, analytics, admin, monitoring, or incident-management features beyond stats and health endpoints.

## Missing but likely required requirements
1. Define supported maximum file size, pages, rows, and image dimensions.
2. Define latency and availability targets.
3. Add authenticated accounts and tenant isolation.
4. Define retention and deletion semantics for memory and feedback.
5. Add answer-quality evaluation and citation correctness checks.
6. Define behavior for malicious documents and prompt injection.
7. Decide whether source citations must be rendered in React.
8. Define a production deployment and backup strategy.
9. Make video generation asynchronous and report progress.
10. Define model version pinning and migration behavior.

## Why these requirements led to the implementation
Broad format support led to parser-specific methods in one engine. Citation needs led to page/slide metadata. Search quality needs led to hybrid retrieval and reranking. Conversation continuity led to a memory collection. Correction persistence led to feedback embeddings. Low infrastructure tolerance led to embedded Chroma and local files. The same choices create current limitations: a monolith, synchronous model calls, shared storage, and no identity boundary.

## Final study notes
### What to say in an interview
Separate what the repository explicitly implements from what a production product would require. This demonstrates product judgment: the current system solves grounded study assistance locally, but its security and reliability requirements are not complete.

### What to study next
Learn requirements traceability, RAG evaluation requirements, privacy impact analysis, SLO definition, and secure file-processing requirements.

### Open questions / uncertainties
The business owner, commercial constraints, user count, privacy classification of uploaded material, and formal acceptance criteria are not visible.
