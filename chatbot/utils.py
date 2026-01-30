from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings


loader = TextLoader("media/lms_data.txt")
documents = loader.load()


embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)


vectorstore = FAISS.from_documents(documents, embeddings)
retriever = vectorstore.as_retriever()


llm = ChatGroq(
    model="llama-3.1-8b-instant",
    temperature=0
)

def get_chatbot_answer(question: str) -> str:
    docs = retriever.invoke(question)
    if not docs:
        return "I couldn't find relevant information in the LMS content."

    context = "\n\n".join(doc.page_content for doc in docs)

    prompt = f"""
You are an LMS student assistant.
Answer ONLY using the context below.
If the answer is not present, say "I don't have that information."

Context:
{context}

Question:
{question}
"""

    response = llm.invoke(prompt)
    return response.content
