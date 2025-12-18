from fastapi import FastAPI, Query
from contextlib import asynccontextmanager
from typing import List, Optional
from app.data import fetch_all_messages
from app.indexer import SearchEngine
from app.schemas import SearchResponse, BenchmarkResponse, HealthResponse
import time

search_engine = SearchEngine()

@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifecycle manager for the FastAPI application.

    Handles startup tasks (fetching data and building the index) and shutdown
    cleanup.

    Args:
        app (FastAPI): The FastAPI application instance.
    """
    print("Fetching and indexing data...")
    messages = await fetch_all_messages()
    search_engine.index_documents(messages)
    print("Indexing complete.")
    yield
    pass

app = FastAPI(lifespan=lifespan)

@app.get("/search", response_model=SearchResponse)
async def search(
    q: str = Query(..., min_length=1, description="Search query"),
    limit: int = 100,
    offset: int = 0
):
    """Performs a search against the indexed documents.

    Args:
        q (str): The search query.
        limit (int): The maximum number of results to return. Defaults to 100.
        offset (int): The starting index for the result page. Defaults to 0.

    Returns:
        dict: A dictionary containing the query, pagination metadata, execution time,
            and list of matching items.
    """
    start_time = time.time()
    
    all_results = search_engine.search(q, top_k=offset + limit)
    
    total_count = len(all_results)
    paginated_results = all_results[offset : offset + limit]
    
    process_time_ms = (time.time() - start_time) * 1000
    
    return {
        "query": q,
        "total": total_count,
        "items": paginated_results,
        "limit": limit,
        "offset": offset,
        "time_ms": round(process_time_ms, 2)
    }

@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check endpoint.

    Returns:
        dict: Status OK dictionary.
    """
    return {"status": "ok"}

@app.get("/benchmark", response_model=BenchmarkResponse)
async def benchmark_internal(
    num_queries: int = Query(100, description="Number of queries to run", le=1000)
):
    """Runs a quick internal benchmark on the search engine.

    Args:
        num_queries (int): Number of random queries to execute. Defaults to 100.

    Returns:
        dict: Performance statistics (min, max, avg, p95, p99 latency).
    """
    import random
    import statistics
    
    queries = [
        "flight to paris", "dinner reservation", "urgent help needed", "lost my luggage",
        "taxi to airport", "book a hotel", "vegetarian options", "invoice query",
        "cancel my booking", "weather in london", "luxury suite", "limo service",
        "concert tickets", "meeting room", "spa appointment", "late check-in",
        "driver contact", "payment issue", "surprise gift", "weekend getaway"
    ]
    
    latencies = []
    
    for _ in range(num_queries):
        q = random.choice(queries)
        start = time.perf_counter()
        search_engine.search(q, top_k=1) 
        duration = (time.perf_counter() - start) * 1000
        latencies.append(duration)
        
    return {
        "queries_run": num_queries,
        "avg_ms": round(statistics.mean(latencies), 2),
        "min_ms": round(min(latencies), 2),
        "max_ms": round(max(latencies), 2),
        "p95_ms": round(statistics.quantiles(latencies, n=20)[18], 2),
        "p99_ms": round(statistics.quantiles(latencies, n=100)[98], 2)
    }
