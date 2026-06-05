memory_store = []


def save_memory(text):
    memory_store.append(text)


def retrieve_memory(query, top_k=3):
    if not memory_store:
        return []

    query_words = set(query.lower().replace(",", "").split())
    scored_memories = []

    for memory in memory_store:
        memory_words = set(memory.lower().replace(",", "").split())
        score = len(query_words.intersection(memory_words))
        scored_memories.append((score, memory))

    scored_memories.sort(reverse=True)

    return [
        memory for score, memory in scored_memories[:top_k]
        if score > 0
    ]