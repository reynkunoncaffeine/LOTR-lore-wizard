import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

# 1. Setup
load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-2.5-flash"

# 2. Load DB
vector_store = Chroma(
    persist_directory="./lotr_db",
    embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"),
    collection_name="lotr_collection"
)

# 3. Styling
st.markdown("""
<style>
    .block-container { 
        padding-top: 8rem;
        justify-content: center;
        text-align: center;
    }

    .lotr-title {
        font-size: 4rem;
        font-family: Old English Text MT, serif;
        font-weight: 800;
        color: #C9A84C;
        margin-bottom: 4rem;
        justify-content: center;
        text-align: center;
    }

    .lotr-tagline {
        font-size: 1rem;
        font-family: Garamond, serif;
        color: #e8c96a;
        margin-bottom: 4rem;
        justify-content: center;
        text-align: center;
    }

    div[data-testid="stForm"] {
        border: none;
        padding: 0;
    }

    div[data-testid="stForm"] input {
        border-radius: 0.5rem !important;
        border: 1px solid #444 !important;
        padding: 0.6rem 1rem !important;
        font-size: 1rem !important;
    }

    .answer-box {
    background-color: #000000;
    border-left: 4px solid #C9A84C;
    padding: 1.2rem 1.5rem;
    border-radius: 0.5rem;
    outline: 1px solid #2a2010;
    margin-top: 1.5rem;
    color: #e0e0e0;
    font-family: Garamond, serif;
    font-size: 1rem;
    line-height: 1.7;
}
    div[data-testid="stFormSubmitButton"] {
    display: none;
    }
</style>
""", unsafe_allow_html=True)

# 4. Header
st.markdown('<div class="lotr-title">LOTR lore wizard</div>', unsafe_allow_html=True)
st.markdown('<div class="lotr-tagline">Ask anything about Middle-earth</div>', unsafe_allow_html=True)

# 5. Search bar — Enter to submit
with st.form(key="query_form", border=False):
    query = st.text_input("", placeholder="Enter your question", label_visibility="collapsed")
    submit = st.form_submit_button(label="", use_container_width=False)

# 6. Handle query
if submit and not query:
    st.warning("Please enter a question to fact-check.")
elif submit and query:
    docs = vector_store.similarity_search(query, k=5, filter={"attempt": 2})
    context = "\n".join([d.page_content for d in docs])

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=f"""You are a lore expert for The Lord of the Rings trilogy.
Question:
{query}

Context (passages retrieved from the books):
{context}

Instructions:
- Use ONLY the retrieved passages above to answer.
- If the lore is explicitly stated, quote or paraphrase it directly.
- If the context does not contain enough information to answer, say: "The trilogy does not provide enough information to verify this."
- Do NOT use outside knowledge or invent lore — accuracy is critical for a fact-checker.
- Keep the answer concise and cite which part of the context supports it where possible.
- Answer in a warm, knowledgeable tone — like a fellow Tolkien reader explaining lore to a friend, not a machine listing bullet points.
- Avoid bullet points and lists. Answer in flowing prose.
""",
    )

    st.markdown(f'<div class="answer-box">{response.text}</div>', unsafe_allow_html=True)
