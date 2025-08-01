from sentence_transformers import SentenceTransformer
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
import dotenv
import os
dotenv.load_dotenv()
HUGGINGFACEHUB_ACCESS_TOKEN = os.getenv("HUGGINGFACEHUB_ACCESS_TOKEN")
print(f"HUGGINGFACEHUB_ACCESS_TOKEN: {HUGGINGFACEHUB_ACCESS_TOKEN}")
# model = SentenceTransformer('all-MiniLM-L6-v2')


model_name = "sentence-transformers/all-mpnet-base-v2"
model_kwargs = {'device': 'cpu'}
encode_kwargs = {'normalize_embeddings': False}
embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs=model_kwargs,
    encode_kwargs=encode_kwargs
)


def embed_chunk(chunks, index_path="index"):
    import os

    if not chunks:
        print("No chunks to embed.")
        return None

    print(f"Embedding {len(chunks)} chunks...")
    print(f"Saving index to: {os.path.abspath(index_path)}")

    # Make sure parent directories exist
    os.makedirs(index_path, exist_ok=True)

    vector_store = FAISS.from_texts(chunks, embeddings)

    vector_store.save_local(index_path)
    print(f"✅ Vector store saved to '{os.path.abspath(index_path)}'")

    return vector_store



# def retrieve_context(chunks,vectorstore, query):
    
#     retriever = vectorstore.as_retriever(search_type = "similarity",search_kwargs={"k": 3})

#     context = retriever.invoke(query)
#     return context


# def embed_chunks(chunks):
#     return model.encode(chunks)

