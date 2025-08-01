from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import TextLoader

import os


def process_chunk_txt(file_path, chunk_size=1000, chunk_overlap=200):
    """
    Processes a text file by splitting it into smaller chunks.

    Args:
        file_path (str): The path to the text file.
        chunk_size (int): The size of each chunk.
        chunk_overlap (int): The overlap between chunks.

    Returns:
        list: A list of text chunks.
    """
    # if not os.path.exists(file_path):
    #     raise FileNotFoundError(f"The file {file_path} does not exist.")

    loader = TextLoader(str(file_path), encoding='utf-8')
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        length_function=len
    )
    
    chunks = text_splitter.split_documents(documents)
    
    return chunks

