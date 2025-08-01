from process.chunk_txt import process_chunk_txt
from process.embed_chunks import embed_chunk
from ingest.extract_text import extract_text_from_pdfs
from ingest.extract_youtube import extract_youtube_transcript
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent  # adjust if needed
UPLOAD_DIR = BASE_DIR / "uploaded_files"
CONTEXT_FILE = BASE_DIR / "context.txt"

def handle_uploaded_data(files, urls):
    if files:
        extract_text_from_pdfs()
    if urls:
        for url in urls:
            text = extract_youtube_transcript(url)
            with CONTEXT_FILE.open("a", encoding="utf-8") as f:
                f.write(f"\n--- Extracted from {url} ---\n")
                f.write(text)
                f.write("\n")
            
    chunks = process_chunk_txt(CONTEXT_FILE, chunk_size=1000, chunk_overlap=200)
    text_chunks = [chunk.page_content for chunk in chunks]
    embed_chunk(text_chunks)

def chat_with_user(query):
    from chain.qa_chain import qa_chain, llm
    # Try to import memory if available
    try:
        from chain.qa_chain import memory
        # Get chat history from memory
        chat_history = memory.load_memory_variables({}).get("chat_history", "")
        # Rewrite the question using the LLM
        rewrite_prompt = f"""
        Given the following chat history and a follow-up question, rewrite the question to be a standalone, contextually clear question for retrieval.
        
        Chat History:
        {chat_history}
        
        Follow-up Question:
        {query}
        
        Rewritten Standalone Question:
        """
        rewritten_message = llm.invoke(rewrite_prompt)
        rewritten_question = rewritten_message.content.strip()
        # Use the rewritten question for retrieval
        result = qa_chain({"question": rewritten_question})
        return result["answer"]
    except ImportError:
        # No memory (no vectorstore): manually track chat history
        import builtins
        if not hasattr(builtins, "_manual_chat_history"):
            builtins._manual_chat_history = []
        # Append user message
        builtins._manual_chat_history.append({"role": "user", "content": query})
        # Build chat history string
        chat_history_str = "\n".join([
            f"{msg['role'].capitalize()}: {msg['content']}" for msg in builtins._manual_chat_history
        ])
        # Compose prompt with chat history
        prompt = f"""
        You are an assistant for question-answering tasks. Use the chat history below to answer the user's latest question. If you don't know, say so.
        \nChat History:\n{chat_history_str}\n\nAssistant:"""
        result = qa_chain({"question": prompt})
        # Extract answer
        if isinstance(result, dict):
            answer = result.get("answer")
            if hasattr(answer, "content"):
                answer = answer.content
        else:
            answer = result
        # Append assistant response to manual chat history
        builtins._manual_chat_history.append({"role": "assistant", "content": answer})
        return answer
