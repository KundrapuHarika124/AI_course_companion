# RAG Project Reorganization Guide

## What Changed?

The RAG project has been reorganized into a production-ready structure with clear separation of backend and frontend code.

---

## 📁 New Directory Structure

```
RAG/
├── backend/
│   ├── api.py                    # FastAPI REST API server
│   ├── rag_pipeline.py           # Core RAG logic & Vector store
│   ├── api_client.py             # Python client library
│   ├── evaluation.py             # 15-question evaluation suite
│   ├── streamlit_app.py          # Web UI (optional)
│   ├── requirements.txt          # Python dependencies
│   ├── .env                      # Local environment (gitignored)
│   ├── .env.example              # Environment template
│   ├── __init__.py               # Package marker
│   ├── data/                     # Course materials
│   │   ├── course_overview.txt
│   │   ├── grading_policy.txt
│   │   ├── certification.txt
│   │   └── faq.txt
│   ├── retrieval_log.csv         # Generated: retrieval logs
│   ├── evaluation_results_*.json  # Generated: evaluation metrics
│   └── __pycache__/              # Generated: Python cache
│
├── frontend/
│   ├── README.md                 # Future frontend setup guide
│   └── (React/Next.js will go here)
│
├── Dockerfile                    # Production Docker image
├── docker-compose.yml            # Docker Compose orchestration
├── README.md                     # Project overview
├── .env.example                  # Root-level env template
├── .gitignore                    # Git ignore rules
├── API_DOCUMENTATION.md          # Complete API reference
├── API_CONVERSION_SUMMARY.md     # Architecture details
└── QUICK_START.md                # Quick reference guide
```

---

## 🚀 Migration Guide

### If You Were Using the Old Structure

**Old layout:**
```
RAG/
├── api.py
├── rag_pipeline.py
├── app.py
├── evaluation.py
├── requirements.txt
└── data/
```

**New layout:**
```
RAG/
├── backend/
│   ├── api.py
│   ├── rag_pipeline.py
│   ├── streamlit_app.py        # (renamed from app.py)
│   ├── evaluation.py
│   ├── requirements.txt
│   └── data/
└── ...
```

### Update Your Imports

If you had custom code importing from the RAG directory:

**Before:**
```python
from rag_pipeline import create_vector_store, answer_question
from api_client import RagAPIClient
```

**After:**
```python
from backend.rag_pipeline import create_vector_store, answer_question
from backend.api_client import RagAPIClient
```

---

## 📝 Configuration Files

### Root Level: `.env.example`
Template for docker-compose and containerized deployments.

```bash
cp .env.example .env
# Edit .env and add GEMINI_API_KEY
```

### Backend Level: `backend/.env.example`
Template for local development.

```bash
cp backend/.env.example backend/.env
# Edit backend/.env and add GEMINI_API_KEY
```

---

## 🐳 Docker & Docker Compose

### Using Docker Compose (Recommended)

```bash
# Setup
cp .env.example .env
# Edit .env with your GEMINI_API_KEY

# Start
docker-compose up -d

# Monitor
docker-compose logs -f api

# Stop
docker-compose down
```

### Using Dockerfile Directly

```bash
# Build
docker build -t rag-api:latest .

# Run
docker run -p 8000:8000 \
  -e GEMINI_API_KEY=your_key \
  rag-api:latest
```

---

## 🎯 Running the API

### Local Development

```bash
cd backend
python api.py
```

### With Uvicorn (Auto-reload)

```bash
cd backend
uvicorn api:app --reload
```

### With Docker

```bash
docker-compose up -d
# API at http://localhost:8000
```

---

## 🧪 Running Tests & Evaluation

### Evaluation Suite

```bash
cd backend
python evaluation.py
```

### API Client Demo

```bash
cd backend
python api_client.py
```

### Manual Testing

```bash
# Health check
curl http://localhost:8000/health

# Query API
curl -X POST http://localhost:8000/answer \
  -H "Content-Type: application/json" \
  -d '{"question": "How is the final grade calculated?"}'
```

---

## 📚 Documentation Location

| Document | Location | Purpose |
|----------|----------|---------|
| README | Root | Project overview |
| API Docs | `API_DOCUMENTATION.md` | Complete API reference |
| Quick Start | `QUICK_START.md` | Getting started guide |
| Architecture | `API_CONVERSION_SUMMARY.md` | System design details |
| Backend Setup | `backend/` | Backend-specific files |
| Frontend Setup | `frontend/README.md` | Frontend guidance (future) |

---

## 🔄 Workflow with New Structure

### For Backend Development
```bash
cd backend
cp .env.example .env
# Edit .env
pip install -r requirements.txt
uvicorn api:app --reload
```

### For Docker Deployment
```bash
cp .env.example .env
# Edit .env
docker-compose up -d
```

### For Frontend Development (Future)
```bash
cd frontend
npm install
npm start
```

---

## ✅ Checklist for Migration

- [x] Create `backend/` directory
- [x] Move API and RAG pipeline files to `backend/`
- [x] Move requirements to `backend/requirements.txt`
- [x] Move data to `backend/data/`
- [x] Rename `app.py` to `streamlit_app.py` in backend
- [x] Create `frontend/` placeholder directory
- [x] Create Dockerfile for backend
- [x] Create docker-compose.yml for orchestration
- [x] Create root-level .env.example
- [x] Update .gitignore with comprehensive rules
- [x] Create this migration guide

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'backend'"

**Solution**: Make sure you're running from the correct directory:
```bash
# ✓ Correct
cd /workspaces/RAG
python backend/api.py

# ✗ Wrong
cd /workspaces/RAG/backend
python api.py  # Won't find backend module
```

### "GEMINI_API_KEY not found"

**Solution**: Make sure `.env` is set up:
```bash
cp .env.example .env
# Edit .env and add your actual API key
```

### "Vector store not loaded in API"

**Solution**: Wait 30-60 seconds after API startup. Check logs:
```bash
docker-compose logs -f api
# or
python backend/api.py  # (see console output)
```

---

## 🎯 Benefits of New Structure

✅ **Clear Separation** - Backend and frontend are independent  
✅ **Scalability** - Easy to add multiple services (workers, queue, database)  
✅ **Deployment** - Docker-ready, cloud-native architecture  
✅ **Maintainability** - Organized file structure with clear responsibilities  
✅ **Documentation** - Config and deployment docs at root level  
✅ **Testing** - Evaluation suite in backend for CI/CD integration  

---

## 📦 Next Steps

1. **Backend Testing**: Run `python backend/evaluation.py`
2. **Docker Testing**: Run `docker-compose up -d` and test at `http://localhost:8000`
3. **Documentation**: Read `API_DOCUMENTATION.md` for detailed API info
4. **Frontend** (Future): Set up React/Next.js in `frontend/` directory

---

## 📞 Support

- See [README.md](README.md) for overall project overview
- See [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for detailed API docs
- See [QUICK_START.md](QUICK_START.md) for quick reference
- Run `docker-compose logs -f api` for runtime logs

---

**Migration completed**: March 1, 2026  
**Status**: ✅ Production-ready structure
