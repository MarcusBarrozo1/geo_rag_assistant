import chromadb
from chromadb.utils import embedding_functions

class AgKnowledgeBase:
    """
    Vector Database manager to store and retrieve unstructured agronomic 
    guidelines and manuals for the RAG pipeline.
    """
    def __init__(self, db_path="./vector_store"):
        #1. Initialize ChromaDB client
        self.chroma_client = chromadb.PersistentClient(path=db_path)

        #2. Setup embedding model (converting text to vectors)
        # Using lightweight, fast and free local model
        self.embedding_function = embedding_functions.SentenceTransformerEmbeddingFunction(
            model_name="all-MiniLM-L6-v2"
        )

        #3. Create or load collection
        self.collection = self.chroma_client.get_or_create_collection(
            name="agronomic_manuals",
            embedding_function=self.embedding_function
        )

    def build_knowledge(self):
        "Injects agronomic guidelines into the vector DB."
        print("Constructing Agronomic Vector Database...")

        #Simulate chunks of text based on agronomic PDF manual
        documents = [
            "SOYBEAN MANUAL: Ideal temperature is between 20C and 30C. If temperature exceeds 32C and soil moisture drops below 30%, it enters critical drought stress. Immediate irrigation is required to save the yield.",
            "CORN MANUAL: Corn is highly dependent on nitrogen. If NDVI drops below 0.60 during the vegetative stage, it indicates severe nutrient deficiency. Apply top-dressing fertilization.",
            "COTTON MANUAL: Cotton is highly sensitive to heat stress. Temperatures above 34C combined with soil moisture below 25% will cause boll shedding. Agronomic alert must be triggered and rescue irrigation applied."
        ]

        #Filter documents
        metadatas = [
            {"crop": "Soybean", "category": "Climate Stress"},
            {"crop": "Corn", "category": "Nutrients"},
            {"crop": "Cotton", "category": "Climate Stress"}
        ]

        ids = ["doc_soybean_01", "doc_corn_01", "doc_cotton_01"] 
        
        ##[f"doc_{i}" for i in range(len(documents))]##

        #Insert if new, update if exists
        self.collection.upsert(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        print(f"Successfully embedded {self.collection.count()} documents into the vector database.\n")
    
    def search_guideline(self, query_text: str, n_results: int = 1):
        """Retrives most relevant manual section based on semantic search."""
        print(f"--- SEMANTIC SEARCH ---")
        print(f"Query: '{query_text}'")

        results = self.collection.query(
            query_texts=[query_text],
            n_results=n_results
        )

        if not results or len(results['documents'][0]) == 0:
            return "No specific guidelines found for this condition", {"crop": "Unknown"}

        return results['documents'][0][0], results['metadatas'][0][0]
    
    #Execution block for testing Vector DB
if __name__ == "__main__":
    #1. Instantiate Vector DB
    vector_db = AgKnowledgeBase()

    #2. Build the knowledge base
    vector_db.build_knowledge() 

    #3. Test semantic search 
    question = "What should I do if my crop is facing extreme heat and low water?"

    retrieved_info, metadata = vector_db.search_guideline(question)

    print("=== RETRIEVED AGRONOMIC GUIDELINE ===")
    print(f"Target Crop: {metadata['crop']}")
    print(f"Guideline: {retrieved_info}")