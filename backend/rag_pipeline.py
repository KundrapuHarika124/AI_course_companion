import os
from google import genai
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings
from dotenv import load_dotenv
import numpy as np
import csv
from datetime import datetime


load_dotenv()

# Configure Gemini
api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)
# ---- Custom Gemini Embedding Wrapper ----
class GeminiEmbedding(Embeddings):
    def embed_documents(self, texts):
        embeddings = []
        for text in texts:
            response = client.models.embed_content(
                model="models/gemini-embedding-001",
                contents=text
            )
            embeddings.append(response.embeddings[0].values)
        return embeddings

    def embed_query(self, text):
        response = client.models.embed_content(
            model="models/gemini-embedding-001",
            contents=text
        )
        return response.embeddings[0].values


# ---- Load Data ----
def load_data():
    docs = []
    files = {
        "course_overview.txt": "overview",
        "grading_policy.txt": "grading",
        "certification.txt": "certification",
        "faq.txt": "faq"
    }

    # Get the directory of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    data_dir = os.path.join(script_dir, "data")

    for file, doc_type in files.items():
        file_path = os.path.join(data_dir, file)
        with open(file_path, "r", encoding="utf-8") as f:
            text = f.read()
            docs.append(Document(
                page_content=text,
                metadata={"type": doc_type}
            ))

    return docs


# ---- Create Vector Store ----
def create_vector_store():
    docs = load_data()

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=150
    )

    split_docs = splitter.split_documents(docs)

    embedding_model = GeminiEmbedding()

    vectorstore = FAISS.from_documents(split_docs, embedding_model)

    return vectorstore


# ---- Classify Question ----
def classify_question(question):
    """Classify user question into predefined categories."""
    question_lower = question.lower()
    
    # Define keywords for each category
    categories = {
        "Grading": ["grade", "grading", "score", "marks", "points", "gpa", "percentage", "weighted", "component"],
        "Certification": ["certificate", "certification", "certified", "credential", "honor", "verify"],
        "Schedule": ["week", "when", "date", "time", "session", "deadline", "due", "duration", "start", "end"],
        "Assignment": ["assignment", "homework", "project", "capstone", "submit", "submission", "solution", "code"],
        "General": ["course", "what", "about", "overview", "prerequisites", "prerequisite", "learn", "cover"]
    }
    
    # Score each category based on keyword matches
    scores = {cat: 0 for cat in categories}
    for category, keywords in categories.items():
        for keyword in keywords:
            if keyword in question_lower:
                scores[category] += 1
    
    # Return category with highest score, default to General
    max_category = max(scores, key=scores.get)
    return max_category if scores[max_category] > 0 else "General"


# ---- Ask Question ----
def answer_question(vectorstore, question):
    # Classify the question
    question_category = classify_question(question)
    
    # Retrieve relevant documents with similarity scores
    relevant_docs = vectorstore.similarity_search_with_score(question, k=3)
    
    # Process retrieved documents and log
    context_parts = []
    timestamp = datetime.now().isoformat()
    
    # Check if CSV file exists, create header if not
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file = os.path.join(script_dir, "retrieval_log.csv")
    file_exists = os.path.exists(csv_file)
    
    with open(csv_file, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(["Timestamp", "Question", "Category", "Chunk_Index", "Document_Type", "Similarity_Score", "Content_Preview"])
        
        # Log each retrieved chunk
        for idx, (doc, score) in enumerate(relevant_docs):
            context_parts.append(doc.page_content)
            doc_type = doc.metadata.get("type", "unknown")
            content_preview = doc.page_content[:100].replace("\n", " ")
            
            writer.writerow([
                timestamp,
                question,
                question_category,
                idx + 1,
                doc_type,
                f"{score:.4f}",
                content_preview
            ])
            
            # Print to console
            print(f"\n[Retrieval {idx + 1}]")
            print(f"  Document Type: {doc_type}")
            print(f"  Similarity Score: {score:.4f}")
            print(f"  Preview: {content_preview}...")
    
    context = "\n\n".join(context_parts)
    
    print(f"\n[Question] {question}")
    print(f"[Category] {question_category}")
    print(f"[Timestamp] {timestamp}")
    print(f"[Logged to] {csv_file}\n")

    prompt = f"""
You are a course workflow assistant.

STRICT INSTRUCTIONS:
1. Use ONLY the context provided below to answer the question.
2. If the answer is NOT explicitly found in the context, respond EXACTLY with: "I do not have that information in the course materials."
3. Do NOT guess, infer, or provide information from your general knowledge.
4. If a question asks for assignment answers, refuse politely.

Context:
{context}

Question:
{question}
"""

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=prompt
    )

    return response.text