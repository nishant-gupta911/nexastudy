# NexaStudy — System Architecture

## Overview

NexaStudy is a full-stack AI application with three main layers:

```
┌─────────────────────────────────────────────────────┐
│                    Frontend (React)                  │
│         Upload UI · Chat UI · Video Preview         │
└──────────────────────┬──────────────────────────────┘
                       │ HTTP (REST API)
┌──────────────────────▼──────────────────────────────┐
│                  FastAPI Backend                     │
│   /upload · /query · /generate-video · /feedback    │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│                   RAG Engine (rag.py)                │
│                                                     │
│  ┌─────────────┐   ┌──────────────┐   ┌──────────┐  │
│  │  Ingestion  │   │  Retrieval   │   │Generation│  │
│  │ PyMuPDF OCR │──▶│ ChromaDB     │──▶│  Gemini  │  │
│  │ Chunking    │   │ Hybrid Search│   │   LLM    │  │
│  │ Embeddings  │   │ Cross-Encoder│   │          │  │
│  └─────────────┘   └──────────────┘   └──────────┘  │
└──────────────────────┬──────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────┐
│           Video Generation (video_gen.py)            │
│         gTTS · MoviePy · Slide Assembly              │
└─────────────────────────────────────────────────────┘
```

## Component Details

### RAG Pipeline
- **Ingestion:** Supports PDF, DOCX, PPTX, TXT, MD, CSV, PNG, JPG
- **OCR:** Tesseract (primary) + Gemini Vision (fallback)
- **Chunking:** RecursiveCharacterTextSplitter (800 chars, 150 overlap)
- **Embeddings:** `models/gemini-embedding-001` via LangChain
- **Storage:** ChromaDB (persistent, cosine similarity)
- **Retrieval:** Hybrid dense + keyword search
- **Reranking:** `cross-encoder/ms-marco-MiniLM-L-6-v2`
- **Generation:** Google Gemini (gemini-2.5-flash-lite)

### Video Generation
- Generates narrated MP4 from document answers
- Text-to-speech via gTTS
- Slide assembly with MoviePy
- Configurable duration per slide

### Frontend
- React 18 + TypeScript + Vite
- Dark theme, responsive layout
- File upload with drag & drop
- Real-time chat interface
- Video preview & download
