# RAG Project - Frontend & Backend Integration

## 🎉 Project Structure

Your RAG project now has both frontend and backend fully integrated:

```
/workspaces/RAG/
├── backend/                 # FastAPI Backend
│   ├── api.py             # REST API endpoints
│   ├── rag_pipeline.py    # RAG logic
│   ├── requirements.txt    # Python dependencies
│   ├── data/              # Course data
│   └── .env               # API key configuration
├── frontend/              # Vue.js + React Frontend
│   ├── src/               # React components
│   ├── package.json       # Node dependencies
│   ├── vite.config.ts     # Vite build config
│   └── .env               # Frontend config
├── docker-compose.yml     # Docker orchestration
└── Dockerfile            # Docker build config
```

## 🚀 Running the Project

### Option 1: Run Both Simultaneously (Recommended)

**Terminal 1 - Backend (Already Running):**
```bash
# Backend is already running in Docker
docker-compose ps    # Verify it's running
curl http://localhost:8000/health  # Test it
```

**Terminal 2 - Frontend Development:**
```bash
cd /workspaces/RAG/frontend
npm run dev
```

The frontend will start at `http://localhost:5173`

### Option 2: Production Build

```bash
# Build the frontend
cd /workspaces/RAG/frontend
npm run build

# Serve production build
npm run preview
```

---

## 📋 Verification Checklist

### Backend Status
- ✅ Docker container running: `docker-compose ps`
- ✅ API health: `curl http://localhost:8000/health`
- ✅ Vector store: Check response says `"vectorstore_loaded": true`

### Frontend Status
- ✅ Dependencies installed: `npm list` (in frontend folder)
- ✅ Configuration: `.env` file has correct API URL
- ✅ Components: `AIAssistantPanel` configured with backend

---

## 🔗 API Endpoints

Your backend provides these endpoints:

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Health check |
| `/answer` | POST | Answer questions with sources |
| `/classify` | POST | Classify questions into categories |
| `/retrieve` | POST | Retrieve relevant documents |
| `/docs` | GET | Swagger API documentation |

### Example: Ask a Question

```bash
curl -X POST http://localhost:8000/answer \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How is the final grade calculated?",
    "top_k": 3
  }'
```

---

## 🌐 Frontend Features

The frontend includes:
- **Course Dashboard**: View course overview and details
- **AI Assistant Panel**: Chat with the RAG system
- **Responsive Design**: Works on desktop and mobile
- **Real-time Answers**: Get answers with sources
- **Beautiful UI**: Built with shadcn/ui and Tailwind CSS

---

## 🔧 Environment Variables

### Backend (`.env`)
```
GEMINI_API_KEY=YOUR_VALID_API_KEY
```

### Frontend (`.env`)
```
VITE_API_URL=https://glowing-spork-69g564qppqx7c5vx7-8000.app.github.dev
VITE_API_TIMEOUT=30000
```

---

## 📝 Important Notes

1. **Backend must be running first** before testing the frontend
2. **API URL is public** - accessible from Lovable and other external apps
3. **API Key is required** - Set valid Gemini API key for vector store to load
4. **CORS enabled** - Backend allows requests from any origin (can be restricted if needed)

---

## 🛠 Troubleshooting

### Frontend can't connect to backend
- Verify backend is running: `docker-compose ps`
- Check API URL in `.env` file
- Ensure port 8000 is public in Codespaces
- Test with curl: `curl https://glowing-spork-69g564qppqx7c5vx7-8000.app.github.dev/health`

### Vector store not loaded
- Check API key is valid
- Restart backend: `docker-compose restart`
- Wait 30-60 seconds for vector store to initialize
- Check logs: `docker-compose logs api`

### Frontend build errors
- Delete `node_modules`: `rm -rf node_modules`
- Reinstall: `npm install`
- Clear cache: `npm cache clean --force`

---

## 📚 Documentation

- Backend API docs: `/docs` endpoint (Swagger UI)
- Frontend README: `./frontend/README.md`
- Backend README: Check project root
- API Documentation: `API_DOCUMENTATION.md`

---

## ✨ Next Steps

1. **Start the frontend**: `cd frontend && npm run dev`
2. **Open browser**: `http://localhost:5173`
3. **Chat with AI**: Ask questions about the course
4. **Build for production**: `npm run build`
5. **Deploy**: Use docker-compose for full stack deployment

---

**Your RAG system is now complete!** 🎓✨
