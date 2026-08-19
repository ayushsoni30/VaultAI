from rag.embeddings import create_embedding


text = "Pradhan Mantri Awas Yojana provides housing assistance."

vector = create_embedding(text)

print("Vector length:", len(vector))
print("First 10 values:", vector[:10])