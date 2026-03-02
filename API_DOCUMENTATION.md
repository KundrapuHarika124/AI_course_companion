# RAG Pipeline API Documentation

## Overview

The RAG Pipeline has been converted into a production-ready REST API using FastAPI. This allows you to integrate the course assistant into any application or service.

---

## Launching the API

### Option 1: Using Uvicorn (Recommended)
```bash
python api.py
```
The API will start on `http://localhost:8000`

### Option 2: Direct Uvicorn Command
```bash
uvicorn api:app --reload --host 0.0.0.0 --port 8000
```

### Option 3: Production Mode
```bash
uvicorn api:app --host 0.0.0.0 --port 8000 --workers 4
```

---

## API Endpoints

### 1. **Health Check**
Verify API status and vector store availability.

```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "Vector store is loaded",
  "vectorstore_loaded": true
}
```

---

### 2. **Answer Question**
Get an answer to a course-related question with retrieval details.

```bash
POST /answer
Content-Type: application/json

{
  "question": "How is the final grade calculated?",
  "top_k": 3
}
```

**Parameters:**
- `question` (string, required): The user's question
- `top_k` (integer, optional): Number of documents to retrieve (default: 3)

**Response:**
```json
{
  "question": "How is the final grade calculated?",
  "category": "Grading",
  "answer": "The final grade is calculated as follows...",
  "timestamp": "2026-03-01T14:30:45.123456",
  "retrieval_results": [
    {
      "index": 1,
      "document_type": "grading",
      "similarity_score": 0.8945,
      "content_preview": "Your final grade is calculated based on..."
    },
    {
      "index": 2,
      "document_type": "grading",
      "similarity_score": 0.7823,
      "content_preview": "Weekly assignments count for 40%..."
    },
    {
      "index": 3,
      "document_type": "certification",
      "similarity_score": 0.7101,
      "content_preview": "A minimum of 70% is required..."
    }
  ]
}
```

---

### 3. **Classify Question**
Classify a question into predefined categories.

```bash
POST /classify
Content-Type: application/json

{
  "question": "When is the midterm exam scheduled?"
}
```

**Parameters:**
- `question` (string, required): The user's question

**Response:**
```json
{
  "question": "When is the midterm exam scheduled?",
  "category": "Schedule",
  "timestamp": "2026-03-01T14:30:45.123456"
}
```

**Categories:**
- `Grading` - Questions about grades, scores, weights
- `Certification` - Questions about certificates, requirements
- `Schedule` - Questions about dates, deadlines, timing
- `Assignment` - Questions about assignments, projects
- `General` - General course information

---

### 4. **Retrieve Documents**
Get relevant documents without generating an answer (for advanced use cases).

```bash
POST /retrieve
Content-Type: application/json

{
  "question": "What are the prerequisites?",
  "top_k": 5
}
```

**Parameters:**
- `question` (string, required): The user's question
- `top_k` (integer, optional): Number of documents to retrieve (default: 3)

**Response:**
```json
{
  "question": "What are the prerequisites?",
  "timestamp": "2026-03-01T14:30:45.123456",
  "documents_retrieved": 3,
  "results": [
    {
      "index": 1,
      "document_type": "overview",
      "similarity_score": 0.9234,
      "content": "Prerequisites: Basic Python programming and linear algebra..."
    }
  ]
}
```

---

### 5. **API Documentation**
Interactive API documentation (Swagger UI):
```
GET /docs
```

Alternative documentation (ReDoc):
```
GET /redoc
```

---

## Curl Examples

### Get Health Status
```bash
curl http://localhost:8000/health
```

### Ask a Question
```bash
curl -X POST http://localhost:8000/answer \
  -H "Content-Type: application/json" \
  -d '{
    "question": "How is certification calculated?",
    "top_k": 3
  }'
```

### Classify a Question
```bash
curl -X POST http://localhost:8000/classify \
  -H "Content-Type: application/json" \
  -d '{"question": "What is the grading policy?"}'
```

### Retrieve Documents
```bash
curl -X POST http://localhost:8000/retrieve \
  -H "Content-Type: application/json" \
  -d '{"question": "Assignment submission deadline", "top_k": 5}'
```

---

## Python Client Example

```python
import requests
import json

BASE_URL = "http://localhost:8000"

# Health check
response = requests.get(f"{BASE_URL}/health")
print("Health:", response.json())

# Ask a question
question_payload = {
    "question": "What topics are covered?",
    "top_k": 3
}
response = requests.post(f"{BASE_URL}/answer", json=question_payload)
result = response.json()

print("Question:", result["question"])
print("Category:", result["category"])
print("Answer:", result["answer"])
print("\nRetrieval Results:")
for r in result["retrieval_results"]:
    print(f"  - {r['document_type']} (Score: {r['similarity_score']})")

# Classify a question
classify_payload = {"question": "When is the exam?"}
response = requests.post(f"{BASE_URL}/classify", json=classify_payload)
print("\nClassification:", response.json())
```

---

## Environment Variables

Make sure your `.env` file contains:
```
GEMINI_API_KEY=your_api_key_here
```

---

## Error Handling

The API returns appropriate HTTP status codes:

- **200 OK**: Successful request
- **400 Bad Request**: Invalid input (e.g., empty question)
- **500 Internal Server Error**: Processing error
- **503 Service Unavailable**: Vector store not loaded

**Example Error Response:**
```json
{
  "detail": "Question cannot be empty"
}
```

---

## Performance Notes

- **Startup Time**: ~30-60 seconds (loading embeddings and building vector store)
- **Response Time**: ~2-5 seconds per question
- **Concurrent Requests**: Supports multiple concurrent requests with async handling
- **Memory Usage**: ~2-3 GB (FAISS index + embeddings)

---

## Deployment

### Docker Deployment
```dockerfile
FROM python:3.10
WORKDIR /app
COPY . .
RUN pip install -r requirements.txt
EXPOSE 8000
CMD ["uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Running with Docker
```bash
docker build -t rag-api .
docker run -p 8000:8000 -e GEMINI_API_KEY=your_key rag-api
```

---

## Integration Examples

### Frontend Integration (JavaScript/React)
```javascript
async function askQuestion(question) {
  const response = await fetch('http://localhost:8000/answer', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ question, top_k: 3 })
  });
  return response.json();
}

// Usage
const result = await askQuestion("How is the final grade calculated?");
console.log(result.answer);
```

### Python Integration
```python
from api import answer_question, vectorstore

# Direct import (if running in same environment)
from rag_pipeline import create_vector_store

vs = create_vector_store()
result = answer_question(vs, "Your question here")
```

---

## Monitoring & Logging

The API logs all operations to console. Key logged events:
- Vector store loading status
- Question answering requests
- Classification operations
- Retrieval operations
- Error conditions

Check logs for debugging and monitoring.

---

## API Metrics (Based on Evaluation)

From the evaluation script:
- **Overall Retrieval Accuracy**: 80.0% (12/15 questions)
- **Grading Questions**: 100% accuracy
- **Certification Questions**: 100% accuracy
- **General Questions**: 100% accuracy
- **Assignment Questions**: 50% accuracy
- **Schedule Questions**: 33.3% accuracy

---

## Future Enhancements

Potential features:
- Rate limiting
- API key authentication
- Caching layer
- Batch question processing
- Feedback mechanism
- Analytics dashboard
- WebSocket support for real-time streaming
