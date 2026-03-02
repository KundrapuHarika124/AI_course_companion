# 📚 RAG Pipeline - Retrieval-Augmented Generation for Course Assistant

A production-ready Retrieval-Augmented Generation (RAG) system that provides intelligent question-answering about course materials using Google's Gemini AI, FAISS vector search, and LangChain.

---

## 🏗️ Project Structure

```
RAG/
│
├── backend/
│   ├── api.py                      # FastAPI REST API server
│   ├── rag_pipeline.py             # Core RAG logic
│   ├── api_client.py               # Python client library
│   ├── evaluation.py               # Test/evaluation suite (15 questions)
│   ├── streamlit_app.py            # Web UI (Streamlit)
│   ├── requirements.txt            # Python dependencies
│   ├── .env.example                # Environment variables template
│   ├── __init__.py                 # Package initialization
│   ├── data/                       # Course materials
│   │   ├── course_overview.txt
│   │   ├── grading_policy.txt
│   │   ├── certification.txt
│   │   └── faq.txt
│   └── __pycache__/                # Python cache (gitignored)
│
├── frontend/                       # (Future) React/Web UI
│   └── README.md
│
├── Dockerfile                      # Production Docker image
├── docker-compose.yml              # Docker Compose orchestration
├── README.md                       # This file
├── .gitignore                      # Git ignore rules
└── API_DOCUMENTATION.md            # Complete API reference
```

---

## 🚀 Quick Start

### Option 1: Local Development

#### Prerequisites
- Python 3.10+
- GEMINI_API_KEY (from Google AI Studio)

#### Setup
```bash
# Navigate to backend
cd backend

# Copy environment template
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY

# Install dependencies
pip install -r requirements.txt

# Start API server
python api.py
# API available at http://localhost:8000
```

#### API Endpoints
- **Swagger UI**: http://localhost:8000/docs
- **Health Check**: http://localhost:8000/health
- **Answer Question**: POST http://localhost:8000/answer
- **Classify Question**: POST http://localhost:8000/classify
- **Retrieve Documents**: POST http://localhost:8000/retrieve

---

### Option 2: Docker

#### Build Image
```bash
docker build -t rag-api:latest .
```

#### Run Container
```bash
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_api_key \
  rag-api:latest
```

#### Docker Compose (Recommended)
```bash
# Copy and configure .env
cp backend/.env.example .env
# Edit .env with your GEMINI_API_KEY

# Start services
docker-compose up -d

# Check logs
docker-compose logs -f
```

---

## 📊 Features

### Core Features
✅ **FastAPI REST API** - Production-ready endpoints  
✅ **Vector Search** - FAISS-based semantic search  
✅ **AI Generation** - Google Gemini integration  
✅ **Question Classification** - 5 categories (Grading, Certification, Schedule, Assignment, General)  
✅ **Retrieval Logging** - CSV export of all retrievals with similarity scores  
✅ **Type Safety** - Pydantic models for all requests/responses  

### Advanced Features
✅ **Strict Context Check** - LLM only answers from course materials  
✅ **Evaluation Suite** - 15 test questions with accuracy metrics  
✅ **Web UI** - Streamlit dashboard (streamlit_app.py)  
✅ **Python Client** - Easy API consumption library  
✅ **Auto Documentation** - Swagger UI & ReDoc  

---

## 📈 Evaluation Results

From the mini evaluation script (15 test questions):
- **Overall Accuracy**: 80.0% (12/15)
- **Grading Questions**: 100%
- **Certification Questions**: 100%
- **General Questions**: 100%
- **Assignment Questions**: 50%
- **Schedule Questions**: 33.3%

Run evaluation:
```bash
cd backend
python evaluation.py
```

---

## 🔧 Tech Stack

### Backend
- **Framework**: FastAPI (async REST API)
- **LLM**: Google Gemini 2.5 Flash
- **Embeddings**: Google Gemini Embedding v1
- **Vector DB**: FAISS (CPU)
- **Text Splitting**: LangChain RecursiveCharacterTextSplitter
- **Web Server**: Uvicorn
- **Web UI**: Streamlit (optional)

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Python**: 3.10+
- **Environment**: .env configuration

---

## 💻 API Usage

### Python Client Example
```python
from backend.api_client import RagAPIClient

client = RagAPIClient("http://localhost:8000")

# Answer a question
result = client.answer_question("How is the final grade calculated?")
print(result['answer'])
print(f"Category: {result['category']}")

# Classify a question
classification = client.classify_question("What is the grading policy?")
print(f"Classified as: {classification['category']}")

# Check API health
health = client.health_check()
print(f"API Status: {health['status']}")
```

### cURL Example
```bash
# Ask a question
curl -X POST http://localhost:8000/answer \
  -H "Content-Type: application/json" \
  -d '{"question": "How is the final grade calculated?"}'

# Classify a question
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the grading policy?"}'

# Get API docs
curl http://localhost:8000/docs
```

### JavaScript/React Example
```javascript
async function askQuestion(question) {
  const response = await fetch('http://localhost:8000/answer', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, top_k: 3 })
  });
  return response.json();
}

const result = await askQuestion("How is certification calculated?");
console.log(result.answer);
```

---

## 🗂️ Key Files

| File | Purpose |
|------|---------|
| `backend/api.py` | FastAPI server with 5 endpoints |
| `backend/rag_pipeline.py` | Core RAG: embedding, retrieval, generation |
| `backend/api_client.py` | Python client for API |
| `backend/evaluation.py` | 15-question evaluation suite |
| `backend/streamlit_app.py` | Web UI dashboard |
| `Dockerfile` | Production Docker image |
| `docker-compose.yml` | Multi-container orchestration |

---

## 📝 Configuration

### Environment Variables
```bash
GEMINI_API_KEY=          # Required: Your Google AI API key
API_HOST=0.0.0.0         # API server host (default)
API_PORT=8000            # API server port (default)
API_WORKERS=4            # Number of workers (production)
ENVIRONMENT=development  # Environment type
DEBUG=True               # Debug mode
LOG_LEVEL=INFO           # Logging level
```

Copy `backend/.env.example` to `.env` and fill in values:
```bash
cp backend/.env.example .env
# Edit .env with your API key
```

---

## 📚 Documentation

- **[API_DOCUMENTATION.md](API_DOCUMENTATION.md)** - Complete API reference with examples
- **[API_CONVERSION_SUMMARY.md](API_CONVERSION_SUMMARY.md)** - Architecture overview
- **[QUICK_START.md](QUICK_START.md)** - Quick reference guide

---

## 🧪 Testing

### Run Evaluation Suite
```bash
cd backend
python evaluation.py
```

### Test with Demo Client
```bash
cd backend
python api_client.py
```

### Manual API Testing
```bash
# Start API
cd backend && python api.py

# In another terminal
curl http://localhost:8000/health
```

---

## 🐳 Docker Deployment

### Build and Run
```bash
# Build image
docker build -t rag-api:1.0 .

# Run container
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  -v $(pwd)/backend/data:/app/backend/data \
  rag-api:1.0
```

### Docker Compose (Recommended)
```bash
# Start all services
docker-compose up -d

# View logs
docker-compose logs -f api

# Stop services
docker-compose down
```

### Production Deployment
```bash
# Build with production tag
docker build -t rag-api:prod .

# Push to registry
docker tag rag-api:prod your-registry/rag-api:prod
docker push your-registry/rag-api:prod

# Deploy to Kubernetes, Cloud Run, etc.
```

---

## 🔍 Monitoring & Logging

### Console Logs
```
INFO:__main__:Loading vector store...
INFO:__main__:✓ Vector store loaded successfully
INFO:__main__:Answered question: How is the final grade calculated?... (Category: Grading)
```

### Retrieval Logging
All retrievals logged to `backend/retrieval_log.csv`:
```
Timestamp,Question,Category,Chunk_Index,Document_Type,Similarity_Score,Content_Preview
2026-03-01T14:02:48...,How is the final grade calculated?,Grading,1,grading,0.5486,...
```

---

## 🎯 Performance Metrics

- **Startup Time**: ~30-60 seconds (cold start with embeddings)
- **Response Time**: ~2-5 seconds per question
- **Memory Usage**: ~2-3 GB (FAISS index + embeddings)
- **Concurrent Requests**: Async support for multiple requests
- **Retrieval Accuracy**: 80% (evaluated on 15 test questions)

---

## 🚦 Health Monitoring

### Health Check Endpoint
```bash
curl http://localhost:8000/health

# Response
{
  "status": "healthy",
  "message": "Vector store is loaded",
  "vectorstore_loaded": true
}
```

### Docker Health Check
```bash
docker ps  # Shows health status in STATUS column
```

---

## 🛠️ Development

### Adding New Features
1. Update `backend/rag_pipeline.py` for RAG logic
2. Add endpoints in `backend/api.py`
3. Update `backend/requirements.txt` if dependencies change
4. Test with `backend/evaluation.py`
5. Update documentation

### Running in Development Mode
```bash
cd backend
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

---

## 🔐 Security Considerations

- ✅ API Key stored in `.env` (gitignored)
- ✅ Type validation with Pydantic
- ✅ Non-root user in Docker
- ✅ Health checks for monitoring
- ⚠️ TODO: Add rate limiting
- ⚠️ TODO: Add authentication
- ⚠️ TODO: Add CORS configuration

---

## 📦 Deployment Platforms

### Supported Platforms
- ✅ Docker/Docker Compose
- ✅ Google Cloud Run
- ✅ AWS ECS
- ✅ Heroku
- ✅ Kubernetes
- ✅ Azure Container Instances

### Google Cloud Run
```bash
gcloud run deploy rag-api \
  --source . \
  --platform managed \
  --region us-central1 \
  --set-env-vars GEMINI_API_KEY=your_key
```

---

## 📋 Files Included

### Course Materials (`backend/data/`)
- `course_overview.txt` - Course topics and structure
- `grading_policy.txt` - Grade calculations and weights
- `certification.txt` - Certificate requirements
- `faq.txt` - Frequently asked questions

### Generated Files
- `backend/retrieval_log.csv` - Log of all retrievals
- `backend/evaluation_results_*.json` - Evaluation metrics

---

## 🔄 Updates & Maintenance

### Adding New Course Materials
1. Add `.txt` file to `backend/data/`
2. Update `rag_pipeline.py` load_data() function
3. Rebuild vector store
4. Re-run evaluation

### Updating Dependencies
```bash
cd backend
pip list --outdated
pip install --upgrade -r requirements.txt
```

---

## 📞 Support

For issues or questions:
1. Check [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
2. Run evaluation: `python backend/evaluation.py`
3. Check console logs for error messages
4. Verify `.env` configuration
5. Ensure GEMINI_API_KEY is valid

---

## 📄 License

This project is provided as-is for educational purposes.

---

## ✨ Highlights

🎯 **Production Ready** - Docker, logging, error handling  
⚡ **Fast** - FAISS indexing + async API  
🔍 **Accurate** - 80% retrieval accuracy on test suite  
📊 **Observable** - Comprehensive logging and metrics  
🧪 **Tested** - 15-question evaluation suite  
📚 **Documented** - Complete API docs and examples  

---

**Version**: 1.0.0  
**Last Updated**: March 1, 2026  
**Status**: Production Ready ✓