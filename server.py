from fastapi import FastAPI, UploadFile, File, Form
from fastapi.responses import JSONResponse
from typing import List, Optional
from processor import handle_uploaded_data, chat_with_user
from pathlib import Path

app = FastAPI()

# 📂 Safe base dir
BASE_DIR = Path(__file__).resolve().parent
UPLOAD_DIR = BASE_DIR / "uploaded_files"
UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

@app.post("/upload_data/")
async def upload_data(
    files: Optional[List[UploadFile]] = File(None),
    urls: Optional[List[str]] = Form(None)
):
    uploaded_files = []
    valid_urls = []

    if files:
        for file in files:
            if not file.filename.endswith(('.pdf', '.txt')):
                return JSONResponse(
                    status_code=400,
                    content={"error": f"{file.filename}: Invalid file type."}
                )
            file_path = UPLOAD_DIR / file.filename
            with open(file_path, "wb") as f:
                f.write(await file.read())
            uploaded_files.append(str(file_path))  # store full path

    if urls:
        print(urls)
        for url in urls:
            if "youtube.com" in url or "youtu.be" in url:
                valid_urls.append(url)

    if not uploaded_files and not valid_urls:
        return JSONResponse(
            status_code=400,
            content={"error": "No valid files or URLs provided."}
        )

    handle_uploaded_data(uploaded_files, valid_urls)
    return {"uploaded_files": uploaded_files, "uploaded_urls": valid_urls}

@app.post("/chat/")
async def chat(query: str = Form(...)):
    result = chat_with_user(query)
    if not result:
        return JSONResponse(
            status_code=404,
            content={"error": "No answer found for the query."}
        )
    return {"query": query, "answer": result}
