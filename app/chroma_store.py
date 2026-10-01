import chromadb

from chunker import create_chunks
from embeddings import create_embedding


client = chromadb.PersistentClient(
    path="./chroma_db"
)

collection = client.get_or_create_collection(
    name="company_policies"
)


def build_chroma_store():
    chunks = create_chunks()

    for index, chunk in enumerate(chunks):
        embedding = create_embedding(chunk)

        collection.add(
            ids=[f"policy-{index}"],
            documents=[chunk],
            embeddings=[embedding]
        )

    print("Documents stored:", collection.count())


def search_chroma(
    query: str,
    top_k: int = 2,
    max_distance: float = 1.0
):
    query_embedding = create_embedding(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    filtered_documents = []
    filtered_distances = []

    for document, distance in zip(
        results["documents"][0],
        results["distances"][0]
    ):
        if distance <= max_distance:
            filtered_documents.append(document)
            filtered_distances.append(distance)

    return {
        "documents": [filtered_documents],
        "distances": [filtered_distances]
    }