# NexaStudy Design Review

## Design philosophy
The design favors a single understandable RAG engine with practical format coverage and a calm study-oriented UI. The backend is organized by responsibility at file level rather than by a formal controller/service/repository stack. The frontend is chat-first, with a separate library and overview view. This is consistent with a learning project that grew feature by feature.

## Module boundaries and separation of concerns
`rag.py` owns domain behavior: extraction, chunking, storage, retrieval, prompts, memory, feedback, and file lifecycle. `api.py` owns transport and validation. `video_gen.py` owns media transformation. `App.tsx` owns browser state and presentation. This boundary is useful because the same RAG class powers FastAPI and Streamlit. The weakness is that `rag.py` is a large class with external model calls, storage calls, and parsing all intertwined, which makes unit testing and future replacement harder.

There is no repository abstraction around Chroma and no separate service layer around Gemini. That reduces indirection for a small application but makes provider/database changes cross-cutting.

## Data model design
The document model is chunk-centric: one file maps to many chunks, and each chunk includes source and page/slide metadata. Feedback and memory are separate vector collections rather than fields on documents, allowing semantic retrieval of corrections and conversation context. Cosine similarity is used across collections. The model is appropriate for RAG retrieval but has no explicit user/tenant key, relational constraints, schema version, or source-file record.

CSV handling is intentionally lightweight: it produces a dataset description plus five rows, which is easy to embed but does not support reliable analytical questions over all rows. DOCX and PPTX preserve some structure; images are reduced to OCR text, so visual layout is not retained.

## API and interface design
The API uses small JSON contracts and multipart upload. Pydantic prevents empty query/session fields. Responses expose answer, sources, chunks, model, and scores, which is useful for debugging and future citation UI. The frontend uses a default `/api` base and expects a Vite proxy. Static videos are mounted separately.

A good design choice is keeping model selection out of the core answer contract for now, but the UI presents model options that are not connected. That is a design smell: a control should either be wired end to end or removed until supported.

## UI/UX design
React uses three views: Study Chat, Library, and Overview. The main screen emphasizes conversation, file upload, starter prompts, loading/error states, and video generation. `index.css` defines Manrope and Newsreader, warm neutral colors, an orange accent, responsive layout, and fade-in motion. The component design uses Lucide icons and Tailwind classes. Streamlit provides a functional alternative with sidebar upload/document management and source expanders.

State flows from `App.tsx`: startup fetches files/stats; input emits message and files; upload precedes chat; response is appended; optional video is fetched. Returned source metadata is not rendered in React, although the backend supplies it. Feedback is available in Streamlit/API but absent from the React workflow.

## Extensibility and maintainability
Adding a new file type is localized to extraction dispatch plus a parser method, but format-specific logic remains in one class. Adding another model provider requires changing initialization, embedding calls, generation calls, and OCR fallback. Adding another persistence backend would be similarly invasive. The environment-driven candidate lists are a modest extensibility mechanism.

Good choices include stable metadata, configurable chunk/retrieval values, model fallbacks, cached singleton initialization, content-hash deduplication, and reusable engine access from two UIs. Risky choices include global local storage, client-controlled sessions, synchronous heavy work, permissive CORS, unbounded upload bytes, broad exception strings returned to clients, and reliance on external services without observability.

## Why this design over alternatives?
A formal hexagonal architecture could improve testing and provider replacement, but would add interfaces and files to a small educational application. A microservice design would support independent scaling, but there is no evidence of multiple operational teams or scale requiring it. A relational database could model users/files/turns more rigorously, but Chroma provides the central semantic retrieval capability with almost no setup. The current decisions are understandable for a portfolio prototype, not ideal for a multi-tenant product.

## Final study notes
### What to say in an interview
Point to the reusable `NexaStudyRAG` boundary as the strongest design decision. Then show architectural maturity by noting that storage, provider, and transport concerns still need stronger abstractions before production scale.

### What to study next
Study hexagonal architecture, ports/adapters for LLMs, vector-store repository interfaces, frontend contract testing, and accessibility/performance testing.

### Open questions / uncertainties
The desired design system, target accessibility level, formal API versioning policy, and expected extension points are not documented.
