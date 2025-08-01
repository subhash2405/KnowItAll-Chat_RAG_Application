# streamlit_app.py


import streamlit as st
import requests
import os
import dotenv
dotenv.load_dotenv()

API_URL = os.getenv("API_URL")  # FastAPI backend URL
print(API_URL)

st.set_page_config(page_title="RAG Chat App", layout="wide")
st.title("🧠 RAG Chat App")

# --- Session state for uploaded files, URLs, and chat history ---

# --- On new session, clean up uploaded_files/ and context.txt ---
def cleanup_files():
    upload_dir = os.path.join(os.path.dirname(__file__), 'uploaded_files')
    context_file = os.path.join(os.path.dirname(__file__), 'context.txt')
    index_dir = os.path.join(os.path.dirname(__file__), 'index')
    # Delete all files in uploaded_files/
    if os.path.exists(upload_dir):
        for fname in os.listdir(upload_dir):
            fpath = os.path.join(upload_dir, fname)
            if os.path.isfile(fpath):
                try:
                    os.remove(fpath)
                except Exception:
                    pass
    # Delete context.txt
    if os.path.exists(context_file):
        try:
            os.remove(context_file)
        except Exception:
            pass
    # Delete index folder and its contents
    if os.path.exists(index_dir):
        import shutil
        try:
            shutil.rmtree(index_dir)
        except Exception:
            pass

if 'initialized' not in st.session_state:
    cleanup_files()
    st.session_state.initialized = True
if 'uploaded_files' not in st.session_state:
    st.session_state.uploaded_files = []  # list of (name, type)
if 'uploaded_urls' not in st.session_state:
    st.session_state.uploaded_urls = []
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []  # list of {"role": "user"/"assistant", "content": text}

# === Sidebar: Upload & History ===
with st.sidebar:
    st.header("📎 Uploaded Content")

    # Show previously uploaded files
    if st.session_state.uploaded_files:
        st.subheader("Files:")
        for fname, ftype in st.session_state.uploaded_files:
            st.write(f"- {fname} ({ftype})")

    # Show previously uploaded URLs
    if st.session_state.uploaded_urls:
        st.subheader("YouTube URLs:")
        for url in st.session_state.uploaded_urls:
            st.write(f"- {url}")

    st.divider()
    st.subheader("📤 Upload Files and YouTube URLs")

    with st.form("upload_form", clear_on_submit=True):
        uploaded_files = st.file_uploader(
            "Upload PDF or TXT files",
            type=['pdf', 'txt'],
            accept_multiple_files=True,
            key="file_uploader"
        )
        links = st.text_area(
            "YouTube URLs (one per line)",
            height=100,
            key="url_textarea"
        )
        upload_submit = st.form_submit_button("Upload")

    if upload_submit:
        # Filter new files
        prev_files = set((f[0], f[1]) for f in st.session_state.uploaded_files)
        new_files = []
        files_data = []
        if uploaded_files:
            for uploaded_file in uploaded_files:
                if (uploaded_file.name, uploaded_file.type) not in prev_files:
                    files_data.append(
                        ('files', (uploaded_file.name, uploaded_file, uploaded_file.type))
                    )
                    new_files.append((uploaded_file.name, uploaded_file.type))

        # Filter new URLs
        url_list = [u.strip() for u in links.splitlines() if u.strip()]
        prev_urls = set(st.session_state.uploaded_urls)
        new_urls = [u for u in url_list if u not in prev_urls]

        # Send data to backend if there’s anything new
        if files_data or new_urls:
            response = requests.post(
                f"{API_URL}/upload_data/",
                files=files_data if files_data else None,
                data=[('urls', u) for u in new_urls] if new_urls else None
            )
            if response.status_code == 200:
                st.success("Upload successful!")
                st.session_state.uploaded_files.extend(new_files)
                st.session_state.uploaded_urls.extend(new_urls)
            else:
                st.error("Upload failed. Please check the server.")
        else:
            st.info("No new files or URLs to upload.")

# === Main Chat Interface ===
st.header("💬 Chat with your data")

# Display previous chat history
for msg in st.session_state.chat_history:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Input bar for asking new questions
if user_query := st.chat_input("Ask a question..."):
    # Append user query to chat history
    st.session_state.chat_history.append({"role": "user", "content": user_query})
    with st.chat_message("user"):
        st.markdown(user_query)

    try:
        response = requests.post(
            f"{API_URL}/chat/",
            data={"query": user_query}
        )
        if response.status_code == 200:
            response_text = response.json().get("answer", "No response from backend.")
            # response_text = response.json()
        else:
            response_text = f"Error: {response.status_code} - {response.text}"
    except Exception as e:
        response_text = f"⚠️ Exception occurred: {e}"

    # Append assistant response to history
    st.session_state.chat_history.append({"role": "assistant", "content": response_text})
    with st.chat_message("assistant"):
        st.markdown(response_text)

# Optional: Reset button
st.sidebar.divider()
if st.sidebar.button("🧹 Reset Chat & Uploads"):
    cleanup_files()
    st.session_state.uploaded_files = []
    st.session_state.uploaded_urls = []
    st.session_state.chat_history = []
    # Also clear manual chat history if present
    import builtins
    if hasattr(builtins, "_manual_chat_history"):
        builtins._manual_chat_history = []
    st.sidebar.success("Session reset.")
