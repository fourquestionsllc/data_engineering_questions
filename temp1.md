import streamlit as st
import pandas as pd
import numpy as np
import openai

# -------------------------
# Setup
# -------------------------
openai.api_key = "YOUR_OPENAI_API_KEY"

# Example: database of Tableau views (you’d load from your real DB)
# This includes random embeddings for demonstration purposes
view_pdf_embeddings = pd.DataFrame({
    "view_name": [f"View {i}" for i in range(10)],
    "workbook_name": [f"Workbook {i%3}" for i in range(10)],
    "pdf_text": [f"Example content for view {i} with some dashboard metrics." for i in range(10)],
    "metadata": [f"Metadata for view {i}" for i in range(10)],
    "embedding": [np.random.rand(768) for _ in range(10)]
})

# -------------------------
# Functions
# -------------------------
def search_views(user_query, top_k=5):
    """Simulate embedding search with cosine similarity."""
    # In real app: get embedding from model
    query_embedding = np.random.rand(768)

    # Normalize
    query_norm = query_embedding / np.linalg.norm(query_embedding)
    embeddings_norm = np.vstack(view_pdf_embeddings["embedding"].to_numpy()) / np.linalg.norm(
        np.vstack(view_pdf_embeddings["embedding"].to_numpy()), axis=1, keepdims=True
    )

    # Cosine similarity
    cosine_similarities = np.dot(embeddings_norm, query_norm)

    # Get top k
    top_indices = np.argsort(cosine_similarities)[-top_k:][::-1]

    results = view_pdf_embeddings.iloc[top_indices].copy()
    results["cosine_similarity"] = cosine_similarities[top_indices]
    return results

def ask_llm_question(df_csv, user_question):
    """Send the CSV + question to the LLM."""
    prompt = f"""
You are an expert data analyst with deep knowledge of Tableau dashboards.
You are given the following retrieved views data in CSV format:

{df_csv}

The user’s question is:
{user_question}

Your task:
1. Use only the provided retrieved views' data to answer the question.
2. If the answer is not fully contained in the data, say so.
3. Reference relevant view names or metadata if helpful.
4. Be concise and accurate.

Answer:
"""
    response = openai.ChatCompletion.create(
        model="gpt-4o-mini",  # or your preferred model
        messages=[
            {"role": "system", "content": "You are a helpful and factual data analysis assistant."},
            {"role": "user", "content": prompt}
        ],
        temperature=0
    )
    return response.choices[0].message["content"]

# -------------------------
# Streamlit UI
# -------------------------
st.set_page_config(layout="wide")
st.title("Tableau Dashboard Search & Q&A")

# Two-column layout
col1, col2 = st.columns(2)

with col1:
    st.subheader("🔍 Search Tableau Views")
    search_query = st.text_input("Enter search query:")
    if st.button("Search"):
        if search_query.strip():
            search_results = search_views(search_query)
            st.session_state["search_results"] = search_results
            st.dataframe(search_results.drop(columns=["embedding"]))
        else:
            st.warning("Please enter a search query.")

with col2:
    st.subheader("💬 Ask about Retrieved Views")
    if "search_results" in st.session_state:
        user_question = st.text_area("Enter your question about the retrieved views:")
        if st.button("Ask LLM"):
            if user_question.strip():
                df_csv = st.session_state["search_results"].drop(columns=["embedding"]).to_csv(index=False)
                answer = ask_llm_question(df_csv, user_question)
                st.markdown("**Answer:**")
                st.write(answer)
            else:
                st.warning("Please enter a question.")
    else:
        st.info("Search for views first to enable Q&A.")
