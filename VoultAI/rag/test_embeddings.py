from embeddings import create_embedding


text = "What is artificial intelligence?"

vector = create_embedding(text)

print("Vector length:", len(vector))
print("First 10 values:", vector[:10])