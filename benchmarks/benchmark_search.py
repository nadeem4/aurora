import httpx
import time
import asyncio
import random
import statistics

URL = "http://localhost:8080/search"
NUM_REQUESTS = 500

# Mix of realistic queries for a concierge service
QUERIES = [
    "flight to paris",
    "dinner reservation",
    "urgent help needed",
    "lost my luggage",
    "taxi to airport",
    "book a hotel",
    "vegetarian options",
    "invoice query",
    "cancel my booking",
    "weather in london",
    "luxury suite",
    "limo service",
    "concert tickets",
    "meeting room",
    "spa appointment",
    "late check-in",
    "driver contact",
    "payment issue",
    "surprise gift",
    "weekend getaway"
]

async def run_benchmark():
    print(f"Starting benchmark: {NUM_REQUESTS} requests...")
    
    latencies = []
    errors = 0
    
    async with httpx.AsyncClient(timeout=10.0) as client:
        # Warmup
        await client.get(URL, params={"q": "warmup"})
        
        start_time = time.time()
        
        for i in range(NUM_REQUESTS):
            q = random.choice(QUERIES)
            req_start = time.perf_counter()
            try:
                response = await client.get(URL, params={"q": q})
                response.raise_for_status()
                latencies.append((time.perf_counter() - req_start) * 1000)
            except Exception as e:
                print(f"Request failed: {e}")
                errors += 1
                
    total_time = time.time() - start_time
    
    if not latencies:
        print("No successful requests.")
        return

    avg_lat = statistics.mean(latencies)
    p50 = statistics.median(latencies)
    p95 = statistics.quantiles(latencies, n=20)[18]  # approx 95th percentile
    p99 = statistics.quantiles(latencies, n=100)[98] # approx 99th percentile
    max_lat = max(latencies)
    min_lat = min(latencies)
    
    print("\n--- Benchmark Results ---")
    print(f"Total Requests: {NUM_REQUESTS}")
    print(f"Failed Requests: {errors}")
    print(f"Total Time:     {total_time:.2f}s")
    print(f"Requests/Sec:   {len(latencies) / total_time:.2f}")
    print("-" * 25)
    print(f"Min Latency:    {min_lat:.2f} ms")
    print(f"Avg Latency:    {avg_lat:.2f} ms")
    print(f"P50 Latency:    {p50:.2f} ms")
    print(f"P95 Latency:    {p95:.2f} ms")
    print(f"P99 Latency:    {p99:.2f} ms")
    print(f"Max Latency:    {max_lat:.2f} ms")
    print("-" * 25)

if __name__ == "__main__":
    asyncio.run(run_benchmark())
