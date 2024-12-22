import openai
import chromadb
from chromadb.config import Settings
import uuid  # For generating unique IDs


def get_chromadb_client():
    """
    Initialize and return a ChromaDB client for persistent storage.

    Returns:
        PersistentClient: ChromaDB client instance.
    """
    try:
        client = chromadb.PersistentClient(path="./chromadb")
        return client
    
    except Exception as e:
        print(f"Failed to initialize ChromaDB client: {e}")
        raise


def store_embeddings(client, collection_name, documents):
    """
    Store embeddings in ChromaDB.

    Args:
        client: ChromaDB client instance.
        collection_name: Name of the collection to store embeddings.
        documents: List of dictionaries, each containing:
            - content: Text content to embed.
            - page_number: Page number in the document.
            - document_id: ID of the document.
    """
    try:
        collection = client.get_or_create_collection(
            name=collection_name,
            metadata={"description": "Collection for document embeddings"}
        )

        for doc in documents:
            try:
                response = openai.Embedding.create(
                    input=doc["content"],
                    model="text-embedding-ada-002"
                )
                embedding = response["data"][0]["embedding"]
                doc_id = str(uuid.uuid4())

                collection.add(
                    ids=[doc_id],
                    embeddings=[embedding],
                    documents=[doc["content"]],
                    metadatas=[{
                        "page_number": doc["page_number"],
                        "document_id": doc["document_id"]
                    }]
                )

            except Exception as e:
                print(f"Failed to process document: {doc['content'][:30]}. Error: {e}")
                continue

    except Exception as e:
        print(f"Failed to store embeddings: {e}")
        raise


def retrieve_relevant_documents(query: str, collection_name: str, top_k: int = 3):
    """
    Retrieve the most relevant documents from ChromaDB.

    Args:
        query (str): The query text.
        collection_name (str): ChromaDB collection name.
        top_k (int): Number of top results to return.

    Returns:
        list: List of relevant documents.
    """
    try:
        query_embedding = openai.Embedding.create(
            input=query,
            model="text-embedding-ada-002"
        )["data"][0]["embedding"]

        client = get_chromadb_client()
        collection = client.get_or_create_collection(collection_name)

        results = collection.query(
            query_embeddings=[query_embedding],
            n_results=top_k,
            include=["documents"]
        )
        return results["documents"][0] if "documents" in results and results["documents"] else []
    
    except Exception as e:
        print(f"Error during retrieval: {e}")
        return []
