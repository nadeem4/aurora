import pytest
from app.indexer import SearchEngine


def test_indexing_and_search():
    engine = SearchEngine()
    docs = [
        {"id": "1", "message": "The quick brown fox", "user_name": "user1"},
        {"id": "2", "message": "Jumps over the lazy dog", "user_name": "user2"},
        {"id": "3", "message": "The quick rabbit", "user_name": "user1"}
    ]
    engine.index_documents(docs)
    
    results = engine.search("animal", top_k=3)
    assert len(results) >= 1
    
    results = engine.search("fox", top_k=1)
    assert results[0]["id"] == "1"
    
    results = engine.search("user1", top_k=5)
    ids = [r["id"] for r in results]
    assert "1" in ids
    assert "3" in ids
