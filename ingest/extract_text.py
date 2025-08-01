import fitz  # PyMuPDF
import os
import dotenv

dotenv.load_dotenv()

# FILES_DIR = os.getenv("FILES_DIR", "uploaded_files")


BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CONTEXT_FILE = os.path.join(BASE_DIR, "..", "context.txt")
FILES_DIR = os.path.join(BASE_DIR, "..", "uploaded_files")

def extract_text_from_pdfs():
    """
    Extracts text from all PDF files in FILES_DIR,
    appends the text to 'context.txt', and returns
    the combined extracted text.

    Returns:
        str: The extracted text from all PDFs.
    """
    combined_text = ""
    # pdf_dir = os.path.join("..", FILES_DIR)
    pdf_dir = FILES_DIR
    print(f"Looking for PDFs in: {pdf_dir}")

    try:
        for file in os.listdir(pdf_dir):
            if file.endswith(".pdf"):
                pdf_path = os.path.join(pdf_dir, file)
                print(f"Extracting text from {pdf_path}")
                text = ""
                with fitz.open(pdf_path) as doc:
                    for page in doc:
                        text += page.get_text()

                combined_text += text

                # Write to context.txt (append mode)
                if not os.path.exists(CONTEXT_FILE):
                    with open(CONTEXT_FILE, "w", encoding="utf-8") as f:
                        f.write("")
                        
                with open(CONTEXT_FILE, "a", encoding="utf-8") as f:
                    f.write(f"\n--- Extracted from {file} ---\n")
                    f.write(text)
                    f.write("\n")  # Add an extra newline for clarity
                print("Added text to context.txt")
    except Exception as e:
        print(f"An error occurred while extracting text: {e}")

    return combined_text

