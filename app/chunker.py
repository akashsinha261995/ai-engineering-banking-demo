from pathlib import Path


KNOWLEDGE_FILE = (
    Path(__file__).parent.parent
    / "knowledge"
    / "company_policies.txt"
)


def load_knowledge():
    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
        return file.read()


def create_chunks():
    knowledge = load_knowledge()

    chunks = [
        section.strip()
        for section in knowledge.split("\n\n")
        if section.strip()
    ]

    return chunks