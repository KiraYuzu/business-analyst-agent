import chromadb
import json

from rag.embedding import get_embeddings

client = chromadb.PersistentClient(path='./chromadb')
collection = client.get_or_create_collection(
    name="docs"
)

def add_chunks(chunks, document_name):
    for i, chunk in enumerate(chunks):
        embedding = get_embeddings(chunk)

        collection.upsert(
            documents=[chunk],
            embeddings=[embedding],
            ids=[f"{document_name}_chunk_{i}"],
            metadatas=[
                {
                    "source": document_name,
                    "chunk_index": i
                }
            ]
        )

    print(f"Added {len(chunks)} chunks to the collection.")

def delete_document(document_name):
    collection.delete(
        where={"source": document_name}
    )

    print(f"Deleted existing chunks for {document_name}")

def view_database():
    results = collection.get()

    print(f"Total chunks in collection: {len(results['documents'])}")

    database_log = []

    for i in range(len(results["ids"])):

        chunk_info = {
            "id": results["ids"][i],
            "metadata": results["metadatas"][i],
            "text": results["documents"][i]
        }

        database_log.append(chunk_info)

        print("\n" + "=" * 80)
        print("ID:", results["ids"][i])
        print("Source:", results["metadatas"][i]["source"])
        print("Chunk Index:", results["metadatas"][i]["chunk_index"])

        print("\nSTART OF CHUNK:")
        print(results["documents"][i][:300])

        print("\nEND OF CHUNK:")
        print(results["documents"][i][-300:])

    # Save to JSON
    with open("collection_contents.json", "w", encoding="utf-8") as f:
        json.dump(database_log, f, indent=4, ensure_ascii=False)

    print("\nDatabase log saved to collection_contents.json")