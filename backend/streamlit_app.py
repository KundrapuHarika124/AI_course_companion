import streamlit as st
from rag_pipeline import create_vector_store, answer_question

st.title("📚 Course RAG Assistant")
st.write("Ask questions about the course!")

# Initialize vector store
if 'vectorstore' not in st.session_state:
    with st.spinner("Loading knowledge base..."):
        try:
            st.session_state.vectorstore = create_vector_store()
            st.success("✅ Knowledge base loaded!")
        except Exception as e:
            st.error(f"Error loading data: {e}")
            st.info("Make sure you have a 'data/' folder with the required text files.")
            st.stop()

# Question input
question = st.text_input("Ask your question:", placeholder="How is certification calculated?")

if st.button("Get Answer") and question:
    with st.spinner("Thinking..."):
        try:
            answer = answer_question(st.session_state.vectorstore, question)
            st.write("### Answer:")
            st.write(answer)
        except Exception as e:
            st.error(f"Error: {e}")

# Example questions
st.sidebar.header("Example Questions")
st.sidebar.write("- How is certification calculated?")
st.sidebar.write("- What is the grading policy?")
st.sidebar.write("- What is this course about?")
st.sidebar.write("- Are there any FAQs?")
