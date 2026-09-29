from embeddings import create_embedding
from chunker import create_chunks


def build_vector_store():
    chunks = create_chunks()

    vector_store = []

    for chunk in chunks:
        embedding = create_embedding(chunk)

        vector_store.append({
            "text": chunk,
            "embedding": embedding
        })

    return vector_store

def cosine_similarity(a, b):
    dot_product = sum(
        x * y
        for x, y in zip(a, b)
    )

    magnitude_a = sum(
        x * x
        for x in a
    ) ** 0.5

    magnitude_b = sum(
        x * x
        for x in b
    ) ** 0.5

    return dot_product / (
        magnitude_a * magnitude_b
    )


def search_vector_store(
    query: str,
    vector_store: list,
    top_k: int = 2,
    min_similarity: float = 0.4
):
    query_embedding = create_embedding(query)

    results = []

    for item in vector_store:

        similarity = cosine_similarity(
            query_embedding,
            item["embedding"]
        )

        results.append({
            "text": item["text"],
            "similarity": similarity
        })

    results.sort(
        key=lambda x: x["similarity"],
        reverse=True
    )

    filtered_results = [
        result
        for result in results
        if result["similarity"] >= min_similarity
    ]

    return filtered_results[:top_k]