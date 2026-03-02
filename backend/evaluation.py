"""
Mini Evaluation Script for RAG Pipeline
Tests 15 sample questions and evaluates retrieval accuracy
"""

from rag_pipeline import create_vector_store, classify_question
import json
from datetime import datetime

# Define 15 test questions with expected document types
TEST_QUESTIONS = [
    # Grading questions (5)
    {
        "question": "How is the final grade calculated?",
        "expected_types": ["grading"],
        "category": "Grading"
    },
    {
        "question": "What is the weight of the capstone project?",
        "expected_types": ["grading"],
        "category": "Grading"
    },
    {
        "question": "What is the late submission penalty?",
        "expected_types": ["grading"],
        "category": "Grading"
    },
    {
        "question": "How much does class participation count?",
        "expected_types": ["grading"],
        "category": "Grading"
    },
    {
        "question": "What percentage do I need to pass?",
        "expected_types": ["grading", "certification"],
        "category": "Grading"
    },
    
    # Certification questions (3)
    {
        "question": "What is required to earn the certificate?",
        "expected_types": ["certification"],
        "category": "Certification"
    },
    {
        "question": "How long does it take to get the certificate?",
        "expected_types": ["certification"],
        "category": "Certification"
    },
    {
        "question": "What happens if I plagiarize?",
        "expected_types": ["certification"],
        "category": "Certification"
    },
    
    # Schedule questions (3)
    {
        "question": "How long is this course?",
        "expected_types": ["overview"],
        "category": "Schedule"
    },
    {
        "question": "When are the live sessions?",
        "expected_types": ["overview"],
        "category": "Schedule"
    },
    {
        "question": "When is the midterm exam?",
        "expected_types": ["grading"],
        "category": "Schedule"
    },
    
    # Assignment questions (2)
    {
        "question": "Can I submit assignments late?",
        "expected_types": ["grading", "faq"],
        "category": "Assignment"
    },
    {
        "question": "How many assignments are there?",
        "expected_types": ["grading"],
        "category": "Assignment"
    },
    
    # General/Overview questions (2)
    {
        "question": "What topics are covered in this course?",
        "expected_types": ["overview"],
        "category": "General"
    },
    {
        "question": "What are the prerequisites?",
        "expected_types": ["overview", "faq"],
        "category": "General"
    }
]


def evaluate_retrieval():
    """Run evaluation on test questions."""
    print("=" * 80)
    print("RAG PIPELINE EVALUATION")
    print("=" * 80)
    print(f"Evaluation started at: {datetime.now().isoformat()}\n")
    
    # Load vector store
    print("Loading vector store...")
    vectorstore = create_vector_store()
    print("✓ Vector store loaded\n")
    
    # Track results
    results = []
    correct_count = 0
    total_count = len(TEST_QUESTIONS)
    
    print(f"Running {total_count} test questions...\n")
    print("-" * 80)
    
    for idx, test_item in enumerate(TEST_QUESTIONS, 1):
        question = test_item["question"]
        expected_types = test_item["expected_types"]
        category = test_item["category"]
        
        # Retrieve documents
        relevant_docs = vectorstore.similarity_search_with_score(question, k=3)
        retrieved_types = [doc.metadata.get("type", "unknown") for doc, score in relevant_docs]
        
        # Check if top retrieval matches expected type
        is_correct = retrieved_types[0] in expected_types
        if is_correct:
            correct_count += 1
        
        # Store result
        result = {
            "question_num": idx,
            "question": question,
            "category": category,
            "expected_types": expected_types,
            "retrieved_types": retrieved_types,
            "top_retrieved": retrieved_types[0],
            "correct": is_correct
        }
        results.append(result)
        
        # Print result
        status = "✓ PASS" if is_correct else "✗ FAIL"
        print(f"\nQ{idx}: {status}")
        print(f"  Question: {question}")
        print(f"  Category: {category}")
        print(f"  Expected: {expected_types}")
        print(f"  Retrieved (top): {retrieved_types[0]}")
        print(f"  All retrieved: {retrieved_types}")
    
    # Calculate and display metrics
    print("\n" + "=" * 80)
    print("EVALUATION RESULTS")
    print("=" * 80)
    
    accuracy = (correct_count / total_count) * 100
    print(f"\nAccuracy: {correct_count}/{total_count} ({accuracy:.1f}%)")
    
    # Category breakdown
    print("\nCategory Breakdown:")
    categories = {}
    for result in results:
        cat = result["category"]
        if cat not in categories:
            categories[cat] = {"total": 0, "correct": 0}
        categories[cat]["total"] += 1
        if result["correct"]:
            categories[cat]["correct"] += 1
    
    for cat in sorted(categories.keys()):
        cat_total = categories[cat]["total"]
        cat_correct = categories[cat]["correct"]
        cat_accuracy = (cat_correct / cat_total) * 100
        print(f"  {cat}: {cat_correct}/{cat_total} ({cat_accuracy:.1f}%)")
    
    # Save results to JSON
    eval_file = f"evaluation_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(eval_file, "w", encoding="utf-8") as f:
        json.dump({
            "timestamp": datetime.now().isoformat(),
            "total_questions": total_count,
            "correct": correct_count,
            "accuracy_percent": accuracy,
            "category_breakdown": categories,
            "detailed_results": results
        }, f, indent=2)
    
    print(f"\nDetailed results saved to: {eval_file}")
    print("\n" + "=" * 80)
    
    return accuracy, results


if __name__ == "__main__":
    evaluate_retrieval()
