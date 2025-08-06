# RAG-Based Chatbot
LLM-powered chatbot using RAG architecture with vector search and prompt engineering to answer questions from custom data sources.

How it works
 - Text files are placed in the docs/ folder.
 - build_index.py processes these files and builds a vector index.
 - rag_project.py or rag_project_langchain.py can be used to query the index and generate answers using a language model.

Files
 - docs/: Folder for input text files.
 - get_transcript.py: Downloads and processes YouTube transcripts.
 - get_book_text.py: Extracts text from books.
 - build_index.py: Builds FAISS index from text files.
 - rag_project.py: Basic RAG pipeline.
 - rag_project_langchain.py: LangChain-based RAG pipeline.

Notes
 - Index files and contents of docs/ are ignored in version control.
 - Requires Python and relevant dependencies.
