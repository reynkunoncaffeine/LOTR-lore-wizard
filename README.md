# LOTR Lore Wizard

*"Not all those who wander are lost — but your Middle-earth facts might be."*

A RAG-powered lore fact-checker built on The Lord of the Rings trilogy. Ask it anything about Middle-earth and it will verify the answer directly from Tolkien's text.

---

## Setup

**1. Clone the repo**
```
git clone <repo-url>
cd lotr-lore-wizard
```

**2. Add the book**

Place your `LOTR.pdf` in the project root.

**3. Set your API key**

Create a `.env` file:
```
GEMINI_API_KEY="your-key-here"
```

**4. Install dependencies**
```
pip install -r requirements.txt
```

**5. Build the vector database**

Run `backend.ipynb` top to bottom. This only needs to be done once — the database is saved to `lotr_db/`.

**6. Launch**
```
streamlit run simpleUI.py
```
OR
```
streamlit run lotrUI.py
```

---

## How it works

The notebook chunks and embeds pages from the trilogy into a local ChromaDB vector store. When you ask a question, the app retrieves the most relevant passages and passes them to Gemini, which answers using only what Tolkien actually wrote — no hallucinated lore.

---

## Notes

- Embedding ~100 pages takes 2–3 minutes on CPU. The full trilogy takes 20–30 minutes.
- Answers are grounded in the text. If the lore isn't in the retrieved passages, the app will say so.
- Tested on Python 3.11+
