

from smart_chunker import smart_chunk_text
from embeddings import create_embeddings


# Sample text for testing
text = """
Artificial intelligence is a branch of computer science.

Machine learning allows computers to learn from data.

Deep learning uses neural networks to solve complex problems.

Generative AI can create text, images, audio, and other content.
"""


# Step 1: Create chunks
chunks = smart_chunk_text(text)


print("Total chunks:", len(chunks))
print()


# Step 2: Create embeddings
embeddings = create_embeddings(chunks)


# Step 3: Display results
for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):

    print(f"Chunk {i}:")
    print(chunk)

    print("Vector length:", len(embedding))
    print("First 5 values:", embedding[:5])

    print("-" * 60)cd..