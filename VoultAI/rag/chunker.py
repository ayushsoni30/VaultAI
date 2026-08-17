def chunk_text(text, chunk_size=500, overlap=50):
    chunks = []

    start = 0

    while start < len(text):

        end = start + chunk_size

        if end < len(text):
            while end > start and not text[end].isspace():
                end -= 1

        chunk = text[start:end].strip()

        chunks.append(chunk)

        start = end - overlap

    return chunks