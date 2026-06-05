def load_knowledge_base(file_path="data/travel_knowledge.txt"):
    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    return [
        chunk.strip()
        for chunk in text.split("\n\n")
        if chunk.strip()
    ]


def retrieve_travel_knowledge(query, top_k=3):
    chunks = load_knowledge_base()

    query_words = set(
        query.lower()
        .replace(",", "")
        .replace(".", "")
        .split()
    )

    scored_chunks = []

    for chunk in chunks:
        chunk_words = set(
            chunk.lower()
            .replace(",", "")
            .replace(".", "")
            .split()
        )

        score = len(query_words.intersection(chunk_words))

        scored_chunks.append(
            {
                "score": score,
                "text": chunk
            }
        )

    scored_chunks.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return [
        item["text"]
        for item in scored_chunks[:top_k]
        if item["score"] > 0
    ]