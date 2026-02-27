import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.documents import Document

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

if os.path.exists("faiss_index"):
    vector_db = FAISS.load_local(
        "faiss_index",
        embedding_model,
        allow_dangerous_deserialization=True
    )
else:
    vector_db = None


def store_documents(text_list):
    global vector_db
    docs = [Document(page_content=text) for text in text_list]

    if vector_db is None:
        vector_db = FAISS.from_documents(docs, embedding_model)
    else:
        vector_db.add_documents(docs)

    vector_db.save_local("faiss_index")


def retrieve(query):
    if vector_db is None:
        return []
    return vector_db.similarity_search(query, k=1)