import streamlit as st
from rag_pipeline import ask_question

st.set_page_config(page_title="Multimodal RAG", layout="wide")

st.title("Multimodal AI RAG System")

query = st.text_input("Ask your question")

method = st.selectbox(
    "Retrieval Method",
    ["bm25", "semantic", "hybrid", "tfidf"]
)

if st.button("Search"):

    result = ask_question(query, method)

    st.subheader("✅ Final Answer")
    st.write(result["answer"])

    st.subheader("📄 Source PDFs")
    for p in result["pdf"]:
        st.write("- ", p)
    st.subheader("📚 Retrieved Chunks")
    for c in result["chunks"]:
        st.write("- ", c)

    st.subheader("🔍 Verification")
    st.write(result["verification"])