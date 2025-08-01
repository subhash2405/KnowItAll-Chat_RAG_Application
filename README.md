# 🧠 KnowItAll-Chat RAG Application

A full-stack Retrieval-Augmented Generation (RAG) chat application that allows users to upload documents (PDF/TXT) and YouTube URLs, build a vector index, and chat with their data using advanced LLMs. The app supports both RAG-based and pure LLM chat modes, with robust session and upload management.

---

## Features

- **Document & YouTube Ingestion:** Upload PDF/TXT files or provide YouTube URLs. Extracts and processes text for retrieval.
- **Vector Indexing:** Chunks and embeds text using HuggingFace models, stores in a FAISS vector index.
- **RAG Chat:** Ask questions and get context-aware answers using a combination of retrieval and LLMs.
- **Fallback LLM Chat:** If no index is present, chat directly with the LLM (multi-turn chat supported).
- **Session Management:** Uploaded files, context, and index are cleared on session reset for a fresh start.
- **Modern UI:** Built with Streamlit, featuring sidebar upload/history, chat interface, and reset controls.

---

## Architecture

```
[User]
  │
  ▼
[Streamlit UI (ui.py)]
  │ REST API
  ▼
[FastAPI Backend (server.py)]
  │
  ├─> [Data Processing (processor.py)]
  │     ├─> [Text Extraction: ingest/extract_text.py, ingest/extract_youtube.py]
  │     ├─> [Chunking/Embedding: process/chunk_txt.py, process/embed_chunks.py]
  │     └─> [Vector Index: index/]
  │
  └─> [RAG Chain (chain/qa_chain.py)]
         └─> [LLM, Retriever, Memory]
```

---

## Setup & Installation

1. **Clone the repository:**
   ```bash
   git clone <repo-url>
   cd KnowItAll-Chat_RAG_Application
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables:**
   - Create a `.env` file in the root directory.
   - Add your API keys (e.g., `GROQ_API_KEY`, `API_URL`, etc.)

4. **Run the backend server:**
   ```bash
   uvicorn server:app --reload
   ```

5. **Run the Streamlit UI:**
   ```bash
   streamlit run ui.py
   ```

---

## Usage

1. **Upload Files/YouTube URLs:**
   - Use the sidebar to upload PDF/TXT files or paste YouTube URLs.
   - Only new files/URLs are uploaded each time.

2. **Chat with Your Data:**
   - Ask questions in the chat interface.
   - If an index is present, answers are context-aware (RAG).
   - If no index, the LLM answers directly (multi-turn chat supported).

3. **Reset Session:**
   - Use the sidebar reset button to clear uploads, context, index, and chat history.

---

## Project Structure

```
KnowItAll-Chat_RAG_Application/
├── chain/
│   └── qa_chain.py           # RAG chain setup (LLM, retriever, memory)
├── ingest/
│   ├── extract_text.py       # PDF/TXT text extraction
│   └── extract_youtube.py    # YouTube transcript extraction
├── process/
│   ├── chunk_txt.py          # Text chunking
│   └── embed_chunks.py       # Embedding chunks
├── index/                    # FAISS index and metadata
├── uploaded_files/           # Uploaded user files
├── context.txt               # Aggregated context for indexing
├── processor.py              # Data processing and chat logic
├── server.py                 # FastAPI backend
├── ui.py                     # Streamlit frontend
├── requirements.txt          # Python dependencies
└── .env                      # Environment variables
```

---

## Key Technologies

- **Streamlit**: UI framework
- **FastAPI**: Backend API
- **LangChain**: RAG pipeline, memory, prompt management
- **HuggingFace Transformers**: Embeddings
- **FAISS**: Vector database
- **Python-dotenv**: Environment management

---

## Customization & Extensibility

- Swap out LLMs or embedding models in `chain/qa_chain.py`.
- Adjust chunking/embedding parameters in `process/`.
- Extend file/URL ingestion logic in `ingest/`.
- Add new endpoints or UI features as needed.

---

## License

MIT License

---

## Acknowledgements

- HuggingFace, LangChain, OpenAI, Anthropic, Google, and the open-source community.
KnowItAll - Chat RAG Application

