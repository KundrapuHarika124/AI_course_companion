# 🎓 AI Course Companion

An intelligent AI assistant that answers student questions about a course using official course materials.

## 🔗 Live Demo

https://ai-course-companion-1ck9.vercel.app/


Students can ask questions like:

- “How are grades calculated?”
- “What are the certification requirements?”
- “When is the capstone due?”

The system gives instant, accurate answers grounded in course documents.

## 🚀 What This Project Does

AI Course Companion uses Retrieval-Augmented Generation (RAG) to:

- Search relevant course documents using semantic vector search
- Retrieve the most relevant content
- Generate an answer using Gemini AI
- Ensure responses are based only on official course materials

No guessing. No hallucinations. Only verified course data.

## 🎯 Why This Project Is Useful

### For Students

- Get instant answers (no waiting for emails)
- Clear and consistent information
- 24/7 academic support

### For Instructors

- Reduce repetitive questions
- Save time
- Focus on teaching instead of admin queries

This system can scale from a small class to thousands of students.

## 🛠️ Tech Stack

- Backend: FastAPI
- LLM: Google Gemini
- Embeddings: Gemini Embedding v1
- Vector Database: FAISS
- Frontend: React + TypeScript
- Deployment: Docker

## 📊 Performance

- Average response time: ~2 seconds
- Evaluated on 15 test questions
- Overall accuracy: 80%
- 100% accuracy on grading & certification queries

Run evaluation:

```bash
cd backend
python evaluation.py
```

## ⚙️ Quick Start

```bash
cd backend
cp .env.example .env
# Add your GEMINI_API_KEY

pip install -r requirements.txt
python api.py
```

API runs at:

http://localhost:8000

Swagger docs:

http://localhost:8000/docs

## 🐳 Docker

```bash
docker-compose up -d
```

## 📁 Project Structure

```text
backend/
  ├── api.py
  ├── rag_pipeline.py
  ├── evaluation.py
  └── data/

frontend/
Dockerfile
docker-compose.yml
```

## 💡 Key Highlights

- Real-world RAG implementation
- Production-ready API
- Dockerized deployment
- Built-in evaluation suite
- Frontend + Backend integration

## 🎉 Final Note

AI Course Companion demonstrates how modern AI systems can improve educational support by combining semantic search and large language models into a scalable, deployable solution.







