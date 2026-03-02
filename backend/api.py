"""
FastAPI-based RAG Pipeline API
Exposes RAG functionality through REST endpoints
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import logging
import asyncio
import os
from rag_pipeline import create_vector_store, answer_question, classify_question

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="RAG Pipeline API",
    description="Retrieval-Augmented Generation API for Course Assistant",
    version="1.0.0"
)

# ---- CORS Configuration ----
raw_cors_origins = os.getenv("CORS_ORIGINS", "*").strip()
if raw_cors_origins == "*":
    cors_origins = ["*"]
    cors_allow_credentials = False
else:
    cors_origins = [origin.strip() for origin in raw_cors_origins.split(",") if origin.strip()]
    cors_allow_credentials = True

app.add_middleware(
    CORSMiddleware,
    allow_origins=cors_origins,
    allow_credentials=cors_allow_credentials,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Global vectorstore (loaded once at startup)
vectorstore = None


# ---- Request/Response Models ----
class QuestionRequest(BaseModel):
    """Request model for answering questions"""
    question: str
    top_k: Optional[int] = 3


class RetrievalResult(BaseModel):
    """Single retrieval result"""
    index: int
    document_type: str
    similarity_score: float
    content_preview: str


class QuestionResponse(BaseModel):
    """Response model for question answering"""
    question: str
    category: str
    answer: str
    timestamp: str
    retrieval_results: List[RetrievalResult]


class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    vectorstore_loaded: bool


class ClassifyRequest(BaseModel):
    """Request model for question classification"""
    question: str


class ClassifyResponse(BaseModel):
    """Response model for question classification"""
    question: str
    category: str
    timestamp: str


# ---- Startup Events ----
@app.on_event("startup")
async def startup_event():
    """Initialize vector store on startup"""
    global vectorstore
    logger.info("Loading vector store...")
    try:
        vectorstore = create_vector_store()
        logger.info("✓ Vector store loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load vector store: {e}")
        vectorstore = None


# ---- Health Check Endpoint ----
@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Check API health and vectorstore status"""
    return HealthResponse(
        status="healthy" if vectorstore else "degraded",
        message="Vector store is loaded" if vectorstore else "Vector store not loaded",
        vectorstore_loaded=vectorstore is not None
    )


# ---- Question Answering Endpoint ----
@app.post("/answer", response_model=QuestionResponse)
async def answer_question_endpoint(request: QuestionRequest):
    """
    Answer a question using RAG pipeline
    
    Args:
        question: The user's question
        top_k: Number of documents to retrieve (default: 3)
    
    Returns:
        Question, answer, category, and retrieval results
    """
    if vectorstore is None:
        raise HTTPException(
            status_code=503,
            detail="Vector store not loaded. Please try again later."
        )
    
    question = request.question.strip()
    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )
    
    try:
        # Classify question
        category = classify_question(question)
        
        # Get relevant documents
        relevant_docs = vectorstore.similarity_search_with_score(question, k=request.top_k)
        
        # Prepare retrieval results
        retrieval_results = []
        for idx, (doc, score) in enumerate(relevant_docs):
            doc_type = doc.metadata.get("type", "unknown")
            content_preview = doc.page_content[:150].replace("\n", " ")
            
            retrieval_results.append(RetrievalResult(
                index=idx + 1,
                document_type=doc_type,
                similarity_score=round(float(score), 4),
                content_preview=content_preview
            ))
        
        # Generate answer
        answer = answer_question(vectorstore, question)
        
        logger.info(f"Answered question: {question[:50]}... (Category: {category})")
        
        return QuestionResponse(
            question=question,
            category=category,
            answer=answer,
            timestamp=datetime.now().isoformat(),
            retrieval_results=retrieval_results
        )
    
    except Exception as e:
        logger.error(f"Error processing question: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error processing question: {str(e)}"
        )


# ---- Question Classification Endpoint ----
@app.post("/classify", response_model=ClassifyResponse)
async def classify_question_endpoint(request: ClassifyRequest):
    """
    Classify a question into predefined categories
    
    Args:
        question: The user's question
    
    Returns:
        Question and its category
    """
    question = request.question.strip()
    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )
    
    try:
        category = classify_question(question)
        logger.info(f"Classified question: {question[:50]}... → {category}")
        
        return ClassifyResponse(
            question=question,
            category=category,
            timestamp=datetime.now().isoformat()
        )
    
    except Exception as e:
        logger.error(f"Error classifying question: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error classifying question: {str(e)}"
        )


# ---- Retrieval Endpoint ----
@app.post("/retrieve")
async def retrieve_documents(request: QuestionRequest):
    """
    Retrieve relevant documents for a question without generating answer
    
    Args:
        question: The user's question
        top_k: Number of documents to retrieve (default: 3)
    
    Returns:
        List of retrieved documents with similarity scores
    """
    if vectorstore is None:
        raise HTTPException(
            status_code=503,
            detail="Vector store not loaded. Please try again later."
        )
    
    question = request.question.strip()
    if not question:
        raise HTTPException(
            status_code=400,
            detail="Question cannot be empty"
        )
    
    try:
        relevant_docs = vectorstore.similarity_search_with_score(question, k=request.top_k)
        
        results = []
        for idx, (doc, score) in enumerate(relevant_docs):
            doc_type = doc.metadata.get("type", "unknown")
            results.append({
                "index": idx + 1,
                "document_type": doc_type,
                "similarity_score": round(float(score), 4),
                "content": doc.page_content[:500],  # Return more content for retrieval endpoint
            })
        
        logger.info(f"Retrieved {len(results)} documents for: {question[:50]}...")
        
        return {
            "question": question,
            "timestamp": datetime.now().isoformat(),
            "documents_retrieved": len(results),
            "results": results
        }
    
    except Exception as e:
        logger.error(f"Error retrieving documents: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving documents: {str(e)}"
        )


# ---- Root Endpoint ----
@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "RAG Pipeline API",
        "version": "1.0.0",
        "description": "Retrieval-Augmented Generation API for Course Assistant",
        "endpoints": {
            "health": "GET /health - Check API health",
            "answer": "POST /answer - Get answer to a question",
            "classify": "POST /classify - Classify a question",
            "retrieve": "POST /retrieve - Retrieve relevant documents",
            "docs": "GET /docs - Interactive API documentation (Swagger UI)",
            "redoc": "GET /redoc - Alternative API documentation (ReDoc)"
        }
    }


if __name__ == "__main__":
    import uvicorn
    host = os.getenv("API_HOST", "0.0.0.0")
    port = int(os.getenv("PORT", os.getenv("API_PORT", "8000")))
    uvicorn.run(app, host=host, port=port)
