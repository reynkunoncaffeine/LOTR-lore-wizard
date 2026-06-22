import os
import streamlit as st
from dotenv import load_dotenv
from google import genai
from langchain_chroma import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))
MODEL_NAME = "gemini-2.5-flash"

vector_store = Chroma(
    persist_directory="./lotr_db",
    embedding_function=HuggingFaceEmbeddings(model_name="sentence-transformers/all-mpnet-base-v2"),
    collection_name="lotr_collection"
)

st.title("LOTR Lore Wizard")
query = st.text_input("Ask a question about Middle-earth:")

if query:
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
    st.write(response.text)
else:
    st.warning("Please enter a question.")
