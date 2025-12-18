from typing import List, Dict, Any
from sentence_transformers import SentenceTransformer, util
import torch

class SearchEngine:
    """Semantic search engine using Vector Embeddings.

    Attributes:
        model (SentenceTransformer): The pre-trained model for generating embeddings.
        documents (Dict[str, Dict[str, Any]]): Storage for full documents by ID.
        embeddings (Tensor): A tensor containing embeddings for all indexed documents.
        doc_ids (List[str]): A list of document IDs corresponding to the embeddings rows.
    """

    def __init__(self):
        print("Loading SentenceTransformer model (this may take a few seconds)...")
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.documents: Dict[str, Dict[str, Any]] = {}
        self.embeddings = None
        self.doc_ids: List[str] = []
        
    def index_documents(self, docs: List[Dict[str, Any]]):
        """Builds the vector index from the provided documents.

        Args:
            docs (List[Dict[str, Any]]): A list of document dictionaries to index.
        """
        texts = []
        self.doc_ids = []
        self.documents = {}
        
        for doc in docs:
            doc_id = doc["id"]
            self.documents[doc_id] = doc
            self.doc_ids.append(doc_id)
            
            text_to_index = f"User: {doc.get('user_name', '')}. Message: {doc.get('message', '')}."
            texts.append(text_to_index)
            
        if not texts:
            return

        print(f"Encoding {len(texts)} documents...")
        self.embeddings = self.model.encode(texts, convert_to_tensor=True)
        print("Encoding complete.")

    def search(self, query: str, top_k: int = 100) -> List[Dict[str, Any]]:
        """Searches for documents semantically matching the query.

        Args:
            query (str): The search query string.
            top_k (int): Number of top results to return (internal cap).

        Returns:
            List[Dict[str, Any]]: A list of matching documents sorted by relevance.
        """
        if self.embeddings is None:
            return []

        query_embedding = self.model.encode(query, convert_to_tensor=True)

        cos_scores = util.cos_sim(query_embedding, self.embeddings)[0]

        k = min(top_k, len(self.doc_ids))
        top_results = torch.topk(cos_scores, k=k)

        results = []
        for score, idx in zip(top_results[0], top_results[1]):
            doc_id = self.doc_ids[idx]
            doc = self.documents[doc_id]
            results.append(doc)
            
        return results
