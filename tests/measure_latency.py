import httpx
import time
import statistics
import asyncio

URL = "http://localhost:8000/search"

async def measure_latency():
    async with httpx.AsyncClient() as client:
        # Warmup
        await client.get(URL, params={"q": "the"})
        
        latencies = []
        for _ in range(100):
            start = time.time()
            response = await client.get(URL, params={"q": "the"})
            end = time.time()
            latencies.append((end - start) * 1000) # ms
            
        avg_latency = statistics.mean(latencies)
        p99 = statistics.quantiles(latencies, n=100)[98] # approx p99
        
        print(f"Average Latency: {avg_latency:.2f}ms")
        print(f"P99 Latency: {p99:.2f}ms")
        
        if avg_latency > 100:
            print("FAIL: Average latency > 100ms")
            exit(1)
        else:
            print("PASS: Latency within limits")

if __name__ == "__main__":
    asyncio.run(measure_latency())
