from database.vector_store import VectorStore

# Initialize VectorStore
vec = VectorStore()

def search(query: str, filters: dict = None) -> list:
    # Semantic & Keyword search + Reranking
    results = vec.hybrid_search(
        query=query, keyword_k=10, semantic_k=10, rerank=True, top_n=5
    )

    return results.to_json()