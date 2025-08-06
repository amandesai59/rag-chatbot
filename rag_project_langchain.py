# chatbot.py
import os
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate

# Load vectorstore
embedding = OpenAIEmbeddings()
vectorstore = FAISS.load_local(
    "faiss_index",
    embedding,
    allow_dangerous_deserialization=True
)
retriever = vectorstore.as_retriever(search_kwargs={"k": 4})

# Set up LLM
llm = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.3)

# Prompt
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
        You are a wise teacher speaking in the voice and philosophy of a wise man.

        Use the following context from the books and text to answer the user's question. Your response should reflect the tone, teachings, and clarity of calm, philosophical, and rooted in spiritual wisdom.

        Context:
        {context}

        Question:
        {question}

        Answer as if explaining to a sincere seeker of truth.
"""
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type_kwargs={"prompt": prompt_template}
)

# Chat loop
print("\n🔍 Chatbot ready. Ask a question based on your documents (empty input to exit).\n")
while True:
    try:
        question = input("You: ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\nGoodbye!")
        break
    if not question:
        print("Goodbye!")
        break

    result = qa_chain.invoke({"query": question})
    print(f"\nAssistant: {result['result']}\n")
