
from chroma_store import search_chroma


def search_company_knowledge(query: str):
    results = search_chroma(
        query=query,
        top_k=2,
        max_distance=1.0
    )

    documents = results["documents"][0]
    metadatas = results["metadatas"][0]
    distances = results["distances"][0]

    if not documents:
        return {
            "success": True,
            "found": False,
            "message": "No relevant company policy was found."
        }

    matches = []

    for document, metadata, distance in zip(
        documents,
        metadatas,
        distances
    ):
        matches.append({
            "content": document,
            "source": metadata["source"],
            "section": metadata["section"],
            "distance": distance
        })

    return {
        "success": True,
        "found": True,
        "matches": matches
    }
