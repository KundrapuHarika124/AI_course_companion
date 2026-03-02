# Quick Start Guide - RAG API

## 🚀 Get Started in 3 Steps

### Step 1: Start the API Server
```bash
python api.py
```

The API will be available at `http://localhost:8000`

### Step 2: Test with curl
```bash
curl -X POST http://localhost:8000/answer \
  -H "Content-Type: application/json" \
  -d '{"question": "How is the final grade calculated?"}'
```

### Step 3: Use the Interactive Docs
Open your browser: `http://localhost:8000/docs`

---

## 📝 Common Tasks

### Task 1: Answer a Question Programmatically

**Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/answer",
    json={"question": "What is the grading policy?"}
)
result = response.json()
print(result['answer'])
```

**JavaScript:**
```javascript
const response = await fetch('http://localhost:8000/answer', {
  method: 'POST',
  headers: { 'Content-Type': 'application/json' },
  body: JSON.stringify({ question: "What is the grading policy?" })
});
const result = await response.json();
console.log(result.answer);
```

---

### Task 2: Classify Questions

Automatically categorize questions:
```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"question": "When is the exam?"}'
```

Returns: `Grading`, `Certification`, `Schedule`, `Assignment`, or `General`

---

### Task 3: Get Raw Documents

Without AI-generated answers:
```bash
curl -X POST http://localhost:8000/retrieve \
  -H "Content-Type: application/json" \
  -d '{"question": "Prerequisites", "top_k": 5}'
```

---

## 🌐 Using the Python Client

Easy-to-use client library:
```python
from api_client import RagAPIClient

client = RagAPIClient()

# Answer question
answer = client.answer_question("How is certification calculated?")
print(answer['answer'])

# Check what category this is
classification = client.classify_question("What is the grading policy?")
print(f"Category: {classification['category']}")

# Get the raw documents
docs = client.retrieve_documents("Course topics", top_k=3)
for doc in docs['results']:
    print(f"- {doc['document_type']}: Score {doc['similarity_score']}")
```

---

## 📊 Expected Responses

### Answer Endpoint Response
```json
{
  "question": "How is the final grade calculated?",
  "category": "Grading",
  "answer": "Your final grade is calculated as follows: 40% assignments, 20% midterm, 30% capstone project, 10% participation",
  "timestamp": "2026-03-01T14:02:50.001243",
  "retrieval_results": [
    {
      "index": 1,
      "document_type": "grading",
      "similarity_score": 0.8945,
      "content_preview": "Your final grade is calculated based on..."
    }
  ]
}
```

---

## 🔍 API Reference

| Endpoint | Method | Purpose |
|----------|--------|---------|
| `/health` | GET | Check API status |
| `/answer` | POST | Answer a question |
| `/classify` | POST | Classify a question |
| `/retrieve` | POST | Get raw documents |
| `/docs` | GET | Interactive documentation |
| `/redoc` | GET | Alternative docs (ReDoc) |

---

## ⚙️ Configuration

### Default Settings
- Host: `0.0.0.0`
- Port: `8000`
- Top-K (default): `3` documents retrieved
- Vector Store: Auto-loaded at startup

### Custom Port
```bash
uvicorn api:app --port 9000
```

### Development Mode (Auto-reload)
```bash
uvicorn api:app --reload
```

### Production Mode (Multiple Workers)
```bash
uvicorn api:app --workers 4
```

---

## 🐛 Troubleshooting

### Issue: "Port already in use"
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Or use a different port
uvicorn api:app --port 8001
```

### Issue: "Vector store not loaded"
Wait 30-60 seconds after starting the API. Startup logs should show:
```
INFO:__main__:✓ Vector store loaded successfully
```

### Issue: "GEMINI_API_KEY not found"
Make sure `.env` file contains:
```
GEMINI_API_KEY=your_api_key_here
```

---

## 📈 Performance Tips

1. **Reuse connections**: Keep persistent HTTP connections for multiple requests
2. **Batch requests**: Send multiple questions in parallel
3. **Cache responses**: Store answers to frequently asked questions
4. **Use /retrieve endpoint**: If you only need documents, skip AI generation

---

## 🔗 Integration Examples

### FastAPI to another FastAPI app
```python
from fastapi import FastAPI
from api_client import RagAPIClient

app = FastAPI()
client = RagAPIClient("http://other-server:8000")

@app.post("/ask")
def ask(question: str):
    return client.answer_question(question)
```

### Express.js backend
```javascript
const express = require('express');
const app = express();

app.post('/ask', async (req, res) => {
  const response = await fetch('http://localhost:8000/answer', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question: req.body.question })
  });
  const result = await response.json();
  res.json(result);
});
```

---

## 📚 Next Steps

1. Read [API_DOCUMENTATION.md](API_DOCUMENTATION.md) for detailed API specs
2. Check [API_CONVERSION_SUMMARY.md](API_CONVERSION_SUMMARY.md) for architecture details
3. Review [rag_pipeline.py](rag_pipeline.py) to understand the core RAG logic
4. Explore [evaluation.py](evaluation.py) to see retrieval accuracy metrics

---

## ✅ Verification

Run this to verify everything is working:
```bash
python api_client.py
```

Expected output:
```
RAG API Client Demo
================================================================================

1. Health Check
Status: healthy
Vector Store: Loaded ✓

2. Answer Sample Questions
...
```

---

## 💡 What's Happening Under the Hood

1. **API starts** → Loads vector store (~30-60s)
2. **Request received** → UTF-8 decoded and validated
3. **Question classified** → Categorized (Grading/Certification/etc)
4. **Documents retrieved** → FAISS similarity search (1-2s)
5. **Answer generated** → Gemini API call (1-3s)
6. **Logged** → Entry added to retrieval_log.csv
7. **Response sent** → JSON returned to client

---

## 🎯 Common Questions

**Q: Can I use this with my React app?**  
A: Yes! Use the `/docs` endpoint or any HTTP client library

**Q: How many concurrent requests can it handle?**  
A: Depends on your hardware. Recommend starting with 1-5 workers

**Q: Where are requests logged?**  
A: Console logs + `retrieval_log.csv` file

**Q: Can I deploy to cloud?**  
A: Yes! Docker, Cloud Run, AWS Lambda, Heroku all supported

**Q: Do I need the Streamlit app?**  
A: No, the API is independent. Keep or remove `app.py` as needed

---

For detailed documentation, see [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
