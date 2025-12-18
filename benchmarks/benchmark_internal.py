import time
import asyncio
import random
import statistics
from app.data import fetch_all_messages
from app.indexer import SearchEngine

# Usage: Run this script directly. It will fetch data and index it locally.

NUM_REQUESTS = 500
QUERIES = [
    "flight to paris", "dinner reservation", "urgent help needed", "lost my luggage",
    "taxi to airport", "book a hotel", "vegetarian options", "invoice query",
    "cancel my booking", "weather in london", "luxury suite", "limo service",
    "concert tickets", "meeting room", "spa appointment", "late check-in",
    "driver contact", "payment issue", "surprise gift", "weekend getaway"
]

async def run_internal_benchmark():
    print("Initializing Search Engine and Indexing Data...")
    engine = SearchEngine()
    messages = await fetch_all_messages()
    engine.index_documents(messages)
    
    print(f"\nStarting Internal Benchmark: {NUM_REQUESTS} searches...")
    
    latencies = []
    
    # Warmup
    engine.search("warmup")
    
    start_time = time.time()
    
    for _ in range(NUM_REQUESTS):
        q = random.choice(QUERIES)
        req_start = time.perf_counter()
        engine.search(q)
        latencies.append((time.perf_counter() - req_start) * 1000)
            
    total_time = time.time() - start_time
    
    avg_lat = statistics.mean(latencies)
    p50 = statistics.median(latencies)
    p95 = statistics.quantiles(latencies, n=20)[18]
    p99 = statistics.quantiles(latencies, n=100)[98]
    
    print("\n--- Internal Method Results ---")
    print(f"Total Searches: {NUM_REQUESTS}")
    print(f"Total Time:     {total_time:.2f}s")
    print(f"Queries/Sec:    {len(latencies) / total_time:.2f}")
    print("-" * 25)
    print(f"Avg Latency:    {avg_lat:.2f} ms")
    print(f"P50 Latency:    {p50:.2f} ms")
    print(f"P95 Latency:    {p95:.2f} ms")
    print(f"P99 Latency:    {p99:.2f} ms")
    print("-" * 25)

if __name__ == "__main__":
    asyncio.run(run_internal_benchmark())
