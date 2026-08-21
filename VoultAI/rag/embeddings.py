from sentence_transformers import SentenceTransformer


model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text: str):
    """
    Create embedding for a single piece of text.
    """

    embedding = model.encode(text)

    return embedding.tolist()


def create_embeddings(texts: list[str]):
    """
    Create embeddings for multiple chunks.
    """

    embeddings = model.encode(texts)

    return embeddings.tolist()