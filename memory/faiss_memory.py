import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

dimension = 384
index = faiss.IndexFlatL2(dimension)

memory_store = []


def save_memory(text):
    embedding = model.encode([text])

    index.add(
        np.array(embedding).astype("float32")
    )

    memory_store.append(text)


def retrieve_memory(query, top_k=3):
    if len(memory_store) == 0:
        return []

    query_embedding = model.encode([query])

    distances, indices = index.search(
        np.array(query_embedding).astype("float32"),
        top_k
    )

    results = []

    for idx in indices[0]:
        if idx < len(memory_store):
            results.append(memory_store[idx])

    return results