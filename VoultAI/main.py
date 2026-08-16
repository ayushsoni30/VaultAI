from fastapi import FastAPI
from rag.loader import extract_text_from_pdf
from rag.chunker import chunk_text

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to VoultAI!"}


@app.get("/test")
def test():
    text= extract_text_from_pdf("data/rag_sample.pdf")
    chunks = chunk_text(text)
    return {
        "total_chunks": len(chunks),
        "chunks": chunks
    }
    # return {
    #     "characters": len(text),
    #     "preview": text[:1000]
    # }