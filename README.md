# 📄 AI Knowledge Assistant

A production-ready RAG (Retrieval-Augmented Generation) chatbot that lets you upload PDF documents and chat with them using AI.

## 🚀 Live Demo
[Try it here](https://ai-knowledge-assistant-8tzpyee9kazbsnrb2lxpnq.streamlit.app/)

## 🏗️ Architecture

```
PDF Upload → FastAPI → LangChain → ChromaDB → Groq LLM → Streaming Response
```

## ✨ Features

- 📄 **PDF Upload & Processing** — Upload any PDF and start chatting
- 🔍 **Semantic Search** — Finds the most relevant chunks using vector similarity
- 🧠 **Chat Memory** — Remembers conversation history per session
- ⚡ **Streaming Response** — Real-time token-by-token answers like ChatGPT
- 🗂️ **Multi-Document Support** — Each document gets a unique ID
- 🛡️ **Error Handling** — Graceful error messages for all failure cases
- 📝 **Logging** — Full request/response logging to file and console
- ⚙️ **Configuration** — All settings managed via environment variables

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| API | FastAPI |
| LLM | Groq (llama-3.3-70b) |
| Embeddings | HuggingFace (all-MiniLM-L6-v2) |
| Vector Store | ChromaDB |
| Document Processing | LangChain |
| Frontend | Streamlit |
| Deployment | Docker, Hugging Face Spaces |

## 📁 Project Structure

```
ai_knowledge_assistant/
├── main.py                  # FastAPI entry point
├── app/
│   ├── api/
│   │   └── routes.py        # API endpoints
│   ├── core/
│   │   ├── config.py        # Environment configuration
│   │   ├── exceptions.py    # Custom exceptions
│   │   └── logger.py        # Logging setup
│   ├── services/
│   │   ├── ingestion.py     # PDF loading & chunking
│   │   ├── rag.py           # RAG pipeline
│   │   ├── retrieval.py     # Vector search
│   │   └── memory.py        # Chat history
│   ├── llm/
│   │   └── groq_service.py  # Groq LLM integration
│   ├── vector_store/
│   │   └── chroma_db.py     # ChromaDB setup
│   └── ui/
│       └── streamlit_app.py # Streamlit frontend
├── Dockerfile
├── requirements.txt
└── .env.example
```

## 🔧 Installation

**1. Clone the repository:**
```bash
git clone https://github.com/omidshadpour/ai-knowledge-assistant.git
cd ai-knowledge-assistant
```

**2. Install dependencies:**
```bash
pip install -r requirements.txt
```

**3. Set up environment variables:**
```bash
cp .env.example .env
# Edit .env and add your API keys
```

**4. Run FastAPI:**
```bash
uvicorn main:app --reload
```

**5. Run Streamlit:**
```bash
streamlit run app/ui/streamlit_app.py
```

## 🔌 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | `/upload` | Upload a PDF file |
| POST | `/ask` | Ask a question (single response) |
| POST | `/ask-stream` | Ask a question (streaming response) |
| POST | `/ask-sources` | Get source pages for a question |
| GET | `/docs` | Swagger UI |

## ⚙️ Environment Variables

```env
GROQ_API_KEY=your_groq_api_key
GROQ_MODEL=llama-3.3-70b-versatile
CHROMA_PATH=chroma_db
COLLECTION_NAME=langchain
EMBEDDING_MODEL=sentence-transformers/all-MiniLM-L6-v2
CHUNK_SIZE=500
CHUNK_OVERLAP=100
RETRIEVAL_K=3
UPLOAD_DIR=uploads
LOGS_DIR=logs
API_URL=http://localhost:8000
```

## 🐳 Docker

```bash
docker build -t ai-knowledge-assistant .
docker run -p 7860:7860 ai-knowledge-assistant
```

## 📊 How It Works

1. **Upload** — PDF is loaded, split into 500-token chunks, and embedded using HuggingFace
2. **Store** — Chunks are stored in ChromaDB with a unique `document_id`
3. **Query** — User question is embedded and matched against stored chunks
4. **Generate** — Top 3 chunks are passed to Groq LLM as context
5. **Stream** — Answer is streamed token by token to the frontend

## 🙋 Author

**Omid Shadpour**
- GitHub: [@omidshadpour](https://github.com/omidshadpour)

