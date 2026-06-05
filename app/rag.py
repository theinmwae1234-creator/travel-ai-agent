import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

dimension = 384
rag_index = faiss.IndexFlatL2(dimension)
knowledge_chunks = []


def load_knowledge_base(file_path="data/travel_knowledge.txt"):
    global knowledge_chunks

    with open(file_path, "r", encoding="utf-8") as file:
        text = file.read()

    knowledge_chunks = [
        chunk.strip()
        for chunk in text.split("\n\n")
        if chunk.strip()
    ]

    embeddings = model.encode(knowledge_chunks)
    rag_index.add(np.array(embeddings).astype("float32"))


def retrieve_travel_knowledge(query, top_k=2):
    if len(knowledge_chunks) == 0:
        load_knowledge_base()

    query_embedding = model.encode([query])

    distances, indices = rag_index.search(
        np.array(query_embedding).astype("float32"),
        top_k
    )

    retrieved_chunks = []

    for idx in indices[0]:
        if idx < len(knowledge_chunks):
            retrieved_chunks.append(knowledge_chunks[idx])

    return retrieved_chunks