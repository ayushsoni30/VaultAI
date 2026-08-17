from fastapi import FastAPI

from rag.loader import extract_text_from_pdf
from rag.smart_chunker import smart_chunk


app = FastAPI()


@app.get("/")
def home():
    return {
        "message": "Welcome to VoultAI!"
    }

@app.get("/test")
def test():

    text = extract_text_from_pdf(
        "data/sample.pdf"
    )

    chunks = smart_chunk(
        text,
        chunk_size=500,
        overlap=50,
        source="sample.pdf"
    )

    return {
        "total_chunks": len(chunks),
        "chunks": chunks
    }