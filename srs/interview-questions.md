# NexaStudy Interview Questions and Answers

## Recruiter and hiring manager

### What does the project do?
**Strong answer:** It helps students ask questions about their own notes and documents. It extracts and indexes uploaded material, retrieves relevant passages, and uses Gemini to answer with source citations. It also remembers recent conversation and can make narrated video summaries.

**Short version:** A citation-aware RAG study assistant.
**Tests:** Can you explain value clearly?
**Avoid:** Calling it a generic ChatGPT clone or claiming training/fine-tuning.

### Why is it interesting technically?
**Strong answer:** It combines multi-format parsing, OCR fallback, vector and keyword retrieval, cross-encoder reranking, feedback memory, a REST API, a React UI, and media generation in one coherent flow.
**Short version:** It demonstrates an end-to-end AI product rather than only an LLM call.
**Tests:** Scope and technical judgment.
**Avoid:** Listing libraries without explaining why they exist.

### What did you learn?
**Strong answer:** Retrieval quality depends on ingestion and metadata as much as generation. I also learned that a prototype needs explicit boundaries: authentication, async work, tests, observability, and evaluation cannot be assumed from a working demo.
**Short version:** Grounding and operational design matter as much as prompts.
**Tests:** Reflection.
**Avoid:** Saying the model alone solved accuracy.

## Product and stakeholder questions

### Who is the user and what is the main journey?
**Answer:** A student uploads material, asks a study question, reads a cited answer, optionally corrects it, and can request a video summary. The main workflow is upload -> retrieve -> answer -> revise.
**Short version:** Turn personal study material into an interactive revision session.
**Tests:** Product thinking.
**Avoid:** Treating library statistics as the product outcome.

### What would you measure?
**Answer:** Retrieval recall and citation correctness, answer helpfulness, time to first answer, upload success by format, OCR success, correction rate, video completion, Gemini cost, and failure rates. The repository currently exposes only simple counts and health information.
**Short version:** Measure quality, latency, cost, and retention, not just API uptime.
**Tests:** Outcome orientation.
**Avoid:** Claiming these metrics already exist.

## Technical questions

### Walk through one chat request.
**Answer:** `App.tsx` posts query and session ID to `/api/chat`. `api.py` gets the cached engine. `rag.py` loads memory, performs dense/keyword/feedback retrieval, merges candidates, reranks with MiniLM, builds a citation-constrained prompt, tries Gemini candidates, saves user and assistant turns, and returns answer plus sources/chunks/scores.
**Short version:** Retrieve, rerank, prompt, generate, persist memory.
**Tests:** Code comprehension.
**Avoid:** Saying the frontend calls Gemini directly.

### Why hybrid retrieval and reranking?
**Answer:** Dense embeddings catch semantic paraphrases; keyword `$contains` helps exact terms such as names or codes; feedback adds known corrections. The cross-encoder then scores query-document pairs more precisely. The tradeoff is extra latency and model complexity.
**Short version:** Recall from multiple signals, precision from reranking.
**Tests:** Retrieval judgment.
**Avoid:** Calling Chroma distances final relevance scores.

### How does ingestion preserve citations?
**Answer:** Each chunk stores source filename, page or slide label, chunk index, total chunks, file type, ingestion time, and document hash. Prompt formatting carries source/page into context, and the model is instructed to cite it.
**Short version:** Metadata travels with every chunk.
**Tests:** Traceability.
**Avoid:** Claiming citations are independently verified.

### What happens if Tesseract is unavailable?
**Answer:** The engine tries Tesseract first and then Gemini vision OCR. For PDFs with weak native text it can render the page and OCR the rendered image. This improves coverage but adds API cost and privacy exposure.
**Short version:** Local OCR first, Gemini vision fallback.
**Tests:** Resilience and tradeoffs.

### Is it production-ready?
**Answer:** Not as currently implemented. It is a useful local prototype. Missing production controls include auth, tenant isolation, restrictive CORS, upload limits, async jobs, tests, monitoring, CI, backups, and deployment configuration.
**Short version:** Strong prototype, incomplete production platform.
**Tests:** Honesty and senior judgment.

## Senior architecture pressure tests

### What breaks at 10x?
**Answer:** Synchronous ingestion and video generation block workers; Gemini calls and cross-encoder inference increase latency and cost; local Chroma and filesystem storage become a bottleneck; shared session IDs cannot isolate users. I would add auth, a job queue, object storage, managed/vector persistence, rate limits, caching, and tracing.
**Short version:** Worker time, shared local state, and external API throughput break first.
**Tests:** Scaling diagnosis.
**Avoid:** Jumping immediately to microservices without measuring.

### Why not use a relational database?
**Answer:** Chroma is a natural low-setup fit for semantic retrieval and local persistence. A relational database would be better for users, permissions, lifecycle, and transactional metadata, so a production system would likely use both: relational control-plane data and vector retrieval storage.
**Short version:** Chroma fits the prototype; relational metadata is needed for product controls.
**Tests:** Tradeoff reasoning.

### Why not use Ollama everywhere?
**Answer:** The repository contains an Ollama alternative, but Gemini provides generation, embeddings, and vision fallback through a single cloud integration. Local Ollama could improve privacy and offline operation, but it adds model hardware requirements and may reduce convenience or quality.
**Short version:** Gemini simplified capability breadth; Ollama favors local privacy.
**Tests:** Evidence-based alternatives.

### What would you improve next?
**Answer:** First rotate any exposed credential, add authentication and per-user document scoping, restrict CORS, validate uploads, and add tests around ingestion/retrieval/API contracts. Next move ingestion/video to background jobs, add evaluation and observability, reconcile frontend/Streamlit contracts, and define deployment/backups.
**Short version:** Security and correctness first, scale and polish second.
**Tests:** Prioritization.

## Code walk-through questions

### What are the hardest parts?
Answer the five: PDF/OCR branching, mixed retrieval score semantics, feedback injection, vector-backed memory ordering, and multiple UI contracts.

### What is a subtle bug or inconsistency?
The API returns `video_url`, React consumes it, but Streamlit reads `video_path` and checks local filesystem existence. Also `run.sh` activates `.venv` while the README documents `.venv312`. These are concrete integration risks.

### What controls are cosmetic?
React captures pasted text, selected model, and thinking state, but the request only sends message/files/session ID. React also does not submit feedback or display sources.

## Behavioral questions tied to this project

### What was hardest?
**Answer:** Making heterogeneous material usable: normal PDFs, scans, slide tables, documents, CSVs, and images need different extraction paths. The solution was to normalize each into labeled text sections before the shared chunk/embed pipeline, while being honest that visual layout and full tabular reasoning remain limited.

### Tell me about a tradeoff.
**Answer:** I favored a single local Chroma-backed engine for fast iteration and low setup. That enabled multiple UIs, but it sacrifices tenant isolation, horizontal scaling, and operational controls. I would preserve the engine boundary while moving persistence and long work behind production interfaces.

### Explain your contribution if you owned everything.
**Answer:** I would say I designed the product flow, implemented ingestion and retrieval, exposed it through FastAPI, built the React and Streamlit interfaces, and added feedback, memory, OCR, and video capabilities. I would also state clearly which production capabilities remain planned.

### Explain your contribution if you owned only part.
**Answer template:** “I owned [specific files/module]. My contract with the rest was [API/data shape]. I changed [behavior], validated [check], and coordinated with [adjacent module]. I would not claim ownership of the full system or model quality.”

## Final study notes
### What to say in an interview
Use evidence: name `rag.py`, `api.py`, `App.tsx`, Chroma collections, and exact gaps. Strong answers explain both the benefit and cost of each choice.

### What to study next
Prepare a short live code walk-through, a 10x scaling design, a security remediation plan, and a RAG evaluation strategy.

### Open questions / uncertainties
Your personal contribution, user research, business success criteria, and real production usage cannot be inferred reliably from this repository. Do not claim them without separate evidence.
