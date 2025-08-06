"""
RAG-style Q&A assistant with LLM generation

Place .txt files in the `docs` folder and ask questions based on their content.
"""

import os
import pathlib
import re
from typing import List
from openai import OpenAI
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Set your API key from env variable
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

docs_dir = pathlib.Path(__file__).parent / "docs"

def load_documents(directory: pathlib.Path) -> List[str]:
    documents = []
    for file in directory.glob("*.txt"):
        with open(file, "r", encoding="utf-8", errors="ignore") as f:
            documents.append(f.read())
    return documents

def split_sentences(text: str) -> List[str]:
    sentences = re.split(r"(?<=[.!?])\s+", text.strip())
    return [s for s in sentences if s]

def build_vectorizer(docs: List[str]):
    vectorizer = TfidfVectorizer(stop_words="english")
    doc_vectors = vectorizer.fit_transform(docs)
    return vectorizer, doc_vectors

def retrieve_documents(query: str, vectorizer, doc_vectors, docs: List[str], top_k: int = 2):
    query_vec = vectorizer.transform([query])
    scores = cosine_similarity(query_vec, doc_vectors).flatten()
    top_indices = scores.argsort()[::-1][:top_k]
    return [(docs[i], scores[i]) for i in top_indices]

def ask_llm(question, context):
    prompt = f"""The following context is from Naval Ravikant's videos.\nUse this context to answer the question as if Naval himself were responding — thoughtful, concise, and clear.\n\nContext:\n{context}\n\nQuestion: {question}\nAnswer:"""

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {
                "role": "system",
                "content": "You are Naval Ravikant, responding based on your past talks. Be insightful, minimalist, and confident."
            },
            {"role": "user", "content": prompt}
        ],
        temperature=0.3,
        max_tokens=300
    )

    return response.choices[0].message.content.strip()

def main():
    if not docs_dir.exists():
        print(f"Docs directory '{docs_dir}' does not exist. Create it and add .txt files.")
        return

    docs = load_documents(docs_dir)
    if not docs:
        print(f"No documents found in {docs_dir}. Please add .txt files to use this assistant.")
        return

    vectorizer, doc_vectors = build_vectorizer(docs)
    print("Knowledge base loaded. Ask a question (empty input to exit).\n")
    while True:
        try:
            question = input("You: ").strip()
        except (EOFError, KeyboardInterrupt):
            print("\nGoodbye!")
            break
        if not question:
            print("Goodbye!")
            break

        retrieved = retrieve_documents(question, vectorizer, doc_vectors, docs)
        top_doc, score = retrieved[0]
        context = " ".join(split_sentences(top_doc)[:5])  # Use first 5 sentences as context
        answer = ask_llm(question, context)
        print(f"\nAssistant:\n{answer}\n")

if __name__ == "__main__":
    main()
