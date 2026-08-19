from sentence_transformers import SentenceTransformer


# Load embedding model once
model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embedding(text: str):

    embedding = model.encode(text)

    return embedding.tolist()


def create_embeddings(texts: list[str]):

    embeddings = model.encode(texts)

    return embeddings.tolist()