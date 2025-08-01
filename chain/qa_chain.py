# qa_chain.py
import os
import dotenv

from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_groq import ChatGroq

dotenv.load_dotenv()

GROQ_API_KEY = os.getenv("GROQ_API_KEY")
print(f"GROQ_API_KEY: {GROQ_API_KEY}")
# 1. Embeddings and Vector Store
embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-mpnet-base-v2",
    model_kwargs={'device': 'cpu'},
    encode_kwargs={'normalize_embeddings': False}
)


def get_vectorstore():
    index_folder = "index"
    index_file = os.path.join(index_folder, "index.faiss")
    if os.path.exists(index_file):
        return FAISS.load_local(
            index_folder,
            embeddings=embeddings,
            allow_dangerous_deserialization=True
        )
    else:
        print("Index not found — you may need to create it first.")
        return None
    
    


vectorstore = get_vectorstore()
llm = ChatGroq(
    model_name="meta-llama/llama-4-scout-17b-16e-instruct",
    temperature=0.7
)

if vectorstore is not None:
    retriever = vectorstore.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 5}
    )
    memory = ConversationBufferMemory(
        memory_key="chat_history",
        return_messages=True
    )
    prompt = PromptTemplate(
        input_variables=["context", "question", "chat_history"],
        template="""
            You are an assistant for question-answering tasks.
            Use the following pieces of retrieved context and the chat history to answer the question.
            If the question is not answerable based on the context, say "I don't know" or "Insufficient information".
            Give detailed explanations with intuitive examples when possible.

            Chat History:
            {chat_history}

            Context:
            {context}

            Question:
            {question}

            Answer:
            """
    )
    qa_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=retriever,
        memory=memory,
        combine_docs_chain_kwargs={"prompt": prompt},
        verbose=True
    )
else:
    # Fallback: direct LLM answer (no retrieval, no context)
    class DummyQADirect:
        def __init__(self, llm):
            self.llm = llm
        def __call__(self, inputs):
            # inputs: {"question": ..., "chat_history": ...}
            question = inputs.get("question")
            chat_history = inputs.get("chat_history", "")
            prompt = f"""
            You are an assistant for question-answering tasks. No context is available.
            Chat History:
            {chat_history}

            Question:
            {question}

            Answer:
            """
            return {"answer": self.llm.invoke(prompt)}
    qa_chain = DummyQADirect(llm)


