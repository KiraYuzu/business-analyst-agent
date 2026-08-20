from rag.retrieval import search

def search_document(query):
    """
    Search company documents for information relevant
    to the user's query.
    """

    results = search(query, n_results=3)
    documents = results["documents"][0]
    metadatas = results["metadatas"][0]

    search_results = []

    for document, metadata in zip(documents, metadatas):
        search_results.append({
            "text": document,
            "source": metadata["source"],
            "chunk_index": metadata["chunk_index"]
        })

    return search_results