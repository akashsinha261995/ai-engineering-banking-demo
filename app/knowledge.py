from chunker import create_chunks


def search_knowledge(query: str):
    chunks = create_chunks()

    results = []

    for section in chunks:
        if any(
            word.lower() in section.lower()
            for word in query.split()
        ):
            results.append(section)

    return results