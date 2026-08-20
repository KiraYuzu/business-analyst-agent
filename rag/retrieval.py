from rag.embedding import get_embeddings
from rag.vector_store import collection

def search(query, n_results=3):
    """
    Search the vector database for chunks
    that are semantically similar to the user's query.
    """

    query_embedding = get_embeddings(query)

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=n_results
    )

    return results