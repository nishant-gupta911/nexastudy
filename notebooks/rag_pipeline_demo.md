# RAG Pipeline Demo Notebook

> Demonstrates the core NexaStudy RAG pipeline end-to-end.

## Steps
1. Load a sample PDF
2. Extract text with PyMuPDF
3. Chunk with RecursiveCharacterTextSplitter (size=800, overlap=150)
4. Embed chunks with Google Gemini Embeddings
5. Store in ChromaDB
6. Query and retrieve top-k chunks
7. Rerank with cross-encoder
8. Generate answer with Gemini

## Sample Query
> "What is retrieval-augmented generation?"

## Sample Output
> RAG is a technique that combines... [cited from uploaded document, page 3]
