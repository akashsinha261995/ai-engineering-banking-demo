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

    # Remove previously stored documents
    collection.delete(
        where={"source": "company_policies.txt"}
    )

    for index, chunk in enumerate(chunks):
        embedding = create_embedding(chunk)

        lines = chunk.splitlines()
        section = lines[0].strip()

        '''
        collection.add(
            ids=[f"policy-{index}"],
            documents=[chunk],
            embeddings=[embedding]
        )
        '''

        collection.upsert(
            ids=[f"policy-{index}"],
            documents=[chunk],
            embeddings=[embedding],
            metadatas=[{
                "source": "company_policies.txt",
                "section": section,
            }]
        )

    print("Documents stored:", collection.count())


def search_chroma(
    query: str,
    top_k: int = 2,
    max_distance: float = 1.0,
    section: str | None = None
):
    query_embedding = create_embedding(query)

    query_kwargs = {
        "query_embeddings": [query_embedding],
        "n_results": top_k
    }

    if section:
        query_kwargs["where"] = {
            "section": section
        }

    results = collection.query(**query_kwargs)

    # results = collection.query(
    #     query_embeddings=[query_embedding],
    #     n_results=top_k
    # )

    filtered_documents = []
    filtered_distances = []
    filtered_metadatas = []

    for document, distance, metadata in zip(
        results["documents"][0],
        results["distances"][0],
        results["metadatas"][0]
    ):
        if distance <= max_distance:
            filtered_documents.append(document)
            filtered_distances.append(distance)
            filtered_metadatas.append(metadata)

    return {
        "documents": [filtered_documents],
        "distances": [filtered_distances],
        "metadatas": [filtered_metadatas]
    }