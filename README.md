<div align="center">

# 🎓 NexaStudy: AI-Powered RAG Study Assistant

![MUJ](https://img.shields.io/badge/Manipal%20University%20Jaipur-orange?style=flat-square)
![Batch](https://img.shields.io/badge/Batch-F-blue?style=flat-square)
![DS](https://img.shields.io/badge/Data%20Science-Capstone-green?style=flat-square)
![Status](https://img.shields.io/badge/Status-Completed-brightgreen?style=flat-square)

**Upload your notes, slides, and PDFs. Get intelligent, cited answers and narrated video summaries powered by Google Gemini.**

</div>

---

## 👤 Student Information

| Field | Details |
|-------|---------|
| **Name** | Nishant Gupta |
| **Registration No.** | 23FE10CDS00506 |
| **Branch** | Data Science |
| **GitHub** | [@nishant-gupta911](https://github.com/nishant-gupta911) |

---

## ⚡ What is NexaStudy?

**NexaStudy** is a student-focused AI assistant built on a **Retrieval-Augmented Generation (RAG)** architecture. It goes beyond simple chat by allowing students to upload their actual course materials (PDFs, PPTs, DOCX, Images). The system intelligently extracts the text, understands the context, and uses the **Google Gemini LLM** to provide precise, cited answers to your study questions.

It even goes a step further by optionally synthesizing these answers into **narrated MP4 video summaries**.

## ✨ Key Features

- 📄 **Multi-Format Ingestion**: Supports PDF, PPTX, DOCX, TXT, MD, CSV, and Images (PNG/JPG/WEBP).
- 👁️ **Smart OCR**: Uses Tesseract locally with a robust fallback to Gemini Vision for tricky scanned documents.
- 🎬 **Video Synthesis**: Instantly turns text answers into narrated slide videos using `MoviePy` and `gTTS`.
- 🔍 **Hybrid Retrieval**: Combines dense vector embeddings with keyword search and cross-encoder reranking for maximum accuracy.
- 🧠 **Smart Memory**: Remembers your conversation history and learns from user feedback/corrections.
- 💻 **Multiple Interfaces**: Choose between a polished React/TypeScript frontend, a Streamlit demo, or direct REST API access.

---

## 🛠️ Tech Stack

- **AI/LLM**: Google Gemini (Flash-Lite / Pro), `langchain-google-genai`
- **Vector Database**: ChromaDB
- **Backend**: Python, FastAPI, Uvicorn
- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS v4
- **Media**: PyMuPDF, `python-pptx`, `python-docx`, Tesseract, MoviePy, gTTS

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- Node.js 18+
- [Tesseract OCR](https://github.com/UB-Mannheim/tesseract/wiki) (Optional, but recommended for faster local OCR)

### 2. Setup
Clone the repository and set up your environment variables:
```bash
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY from https://aistudio.google.com
```

### 3. Install Dependencies
**Backend:**
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```
**Frontend:**
```bash
cd frontend
npm install
```

### 4. Run the Application
You will need two terminal windows:

**Terminal 1 (FastAPI Backend):**
```bash
source .venv/bin/activate
uvicorn api:app --host 127.0.0.1 --port 8000
```

**Terminal 2 (React Frontend):**
```bash
cd frontend
npm run dev -- --host 127.0.0.1 --port 5173
```
Open **http://localhost:5173** in your browser!

*(Optional) To run the Streamlit demo instead of React: `streamlit run app.py`*

---

## 🤖 Recreate this Project with AI

Want to see how this project was built or have an AI agent reconstruct it for you? 

We have included a special file called **[`BUILD_PROMPT.txt`](BUILD_PROMPT.txt)**. 
It contains a complete, self-contained mega-prompt. You can paste its contents into any advanced AI coding agent (like Cursor, Antigravity, or Claude) in an empty folder, and it will autonomously generate the entire codebase, directory structure, and configuration for this project.

---

## 📁 Repository Map

```text
nexastudy/
├── api.py                 ← FastAPI REST backend routes
├── rag.py                 ← Core RAG engine logic (Ingestion, Retrieval, LLM)
├── video_gen.py           ← Video synthesis pipeline
├── frontend/              ← React + TypeScript + Vite UI
├── BUILD_PROMPT.txt       ← Mega-prompt to recreate the project via AI agents
├── app.py                 ← Streamlit fallback UI
├── assignments/           ← Weekly course submissions
├── notebooks/             ← Jupyter notebooks for EDA and testing
└── capstone/              ← Project documentation and logs
```

---
*Developed for the MUJ Data Science Training Capstone Project.*
