def load_knowledge_base(file_path="data/travel_knowledge.txt"):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return [
        chunk.strip()
        for chunk in text.split("\n\n")
        if chunk.strip()
    ]


def retrieve_travel_knowledge(query, top_k=2):
    chunks = load_knowledge_base()

    query_words = set(query.lower().replace(",", "").split())
    scored_chunks = []

    for chunk in chunks:
        chunk_words = set(chunk.lower().replace(",", "").split())
        score = len(query_words.intersection(chunk_words))
        scored_chunks.append((score, chunk))

    scored_chunks.sort(reverse=True)

    return [
        chunk for score, chunk in scored_chunks[:top_k]
        if score > 0
    ]