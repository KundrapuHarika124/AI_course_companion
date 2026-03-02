#!/usr/bin/env python3
"""
RAG API Client
Simple client for interacting with the RAG Pipeline API
"""

import requests
import json
from typing import Optional

class RagAPIClient:
    """Client for RAG Pipeline REST API"""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        """
        Initialize the RAG API client
        
        Args:
            base_url: Base URL of the RAG API (default: http://localhost:8000)
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
    
    def health_check(self) -> dict:
        """Check API health status"""
        response = self.session.get(f"{self.base_url}/health")
        response.raise_for_status()
        return response.json()
    
    def answer_question(self, question: str, top_k: int = 3) -> dict:
        """
        Get answer to a question
        
        Args:
            question: The question to ask
            top_k: Number of documents to retrieve
        
        Returns:
            Response containing answer and retrieval details
        """
        payload = {
            "question": question,
            "top_k": top_k
        }
        response = self.session.post(
            f"{self.base_url}/answer",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def classify_question(self, question: str) -> dict:
        """
        Classify a question into a category
        
        Args:
            question: The question to classify
        
        Returns:
            Response containing question classification
        """
        payload = {"question": question}
        response = self.session.post(
            f"{self.base_url}/classify",
            json=payload
        )
        response.raise_for_status()
        return response.json()
    
    def retrieve_documents(self, question: str, top_k: int = 3) -> dict:
        """
        Retrieve relevant documents for a question
        
        Args:
            question: The question to search for
            top_k: Number of documents to retrieve
        
        Returns:
            Response containing retrieved documents
        """
        payload = {
            "question": question,
            "top_k": top_k
        }
        response = self.session.post(
            f"{self.base_url}/retrieve",
            json=payload
        )
        response.raise_for_status()
        return response.json()


def print_answer_result(result: dict):
    """Pretty print answer result"""
    print("\n" + "="*80)
    print(f"QUESTION: {result['question']}")
    print(f"CATEGORY: {result['category']}")
    print("-"*80)
    print(f"ANSWER:\n{result['answer']}")
    print("-"*80)
    print("RETRIEVAL RESULTS:")
    for r in result['retrieval_results']:
        print(f"\n[{r['index']}] {r['document_type'].upper()}")
        print(f"    Score: {r['similarity_score']:.4f}")
        print(f"    Preview: {r['content_preview'][:80]}...")
    print("="*80 + "\n")


def print_classification_result(result: dict):
    """Pretty print classification result"""
    print(f"Question: {result['question']}")
    print(f"Category: {result['category']}")
    print(f"Timestamp: {result['timestamp']}\n")


def main():
    """Main demo function"""
    print("RAG API Client Demo")
    print("="*80)
    
    # Initialize client
    client = RagAPIClient()
    
    # Check health
    print("\n1. Health Check")
    try:
        health = client.health_check()
        print(f"Status: {health['status']}")
        print(f"Vector Store: {'Loaded ✓' if health['vectorstore_loaded'] else 'Not loaded ✗'}")
    except Exception as e:
        print(f"Error: {e}")
        return
    
    # Sample questions
    questions = [
        "How is the final grade calculated?",
        "What are the certification requirements?",
        "When is the midterm exam?",
        "What is the late submission penalty?",
        "What topics are covered in this course?"
    ]
    
    # Answer questions
    print("\n2. Answer Sample Questions")
    for q in questions[:2]:  # Demo with first 2 questions
        try:
            result = client.answer_question(q)
            print_answer_result(result)
        except Exception as e:
            print(f"Error answering question: {e}\n")
    
    # Classify questions
    print("\n3. Classify Questions")
    for q in questions:
        try:
            result = client.classify_question(q)
            print_classification_result(result)
        except Exception as e:
            print(f"Error classifying question: {e}\n")
    
    # Retrieve documents
    print("\n4. Retrieve Documents (without answering)")
    try:
        result = client.retrieve_documents("What is the grading policy?", top_k=2)
        print(f"Question: {result['question']}")
        print(f"Documents Retrieved: {result['documents_retrieved']}")
        for r in result['results']:
            print(f"\n[{r['index']}] {r['document_type'].upper()} (Score: {r['similarity_score']:.4f})")
            print(f"Content: {r['content'][:200]}...")
    except Exception as e:
        print(f"Error: {e}\n")


if __name__ == "__main__":
    main()
