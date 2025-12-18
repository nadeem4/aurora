import httpx
import asyncio
from typing import List, Dict, Any

API_URL = "https://november7-730026606190.europe-west1.run.app/messages/"

async def fetch_all_messages() -> List[Dict[str, Any]]:
    """Fetches all messages from the API.

    Iterates through paginated API responses to retrieve the complete dataset
    of messages.

    Returns:
        List[Dict[str, Any]]: A list of dictionaries, each representing a message.

    Raises:
        httpx.HTTPStatusError: If the API returns a non-success status code.
    """
    all_messages = []
    async with httpx.AsyncClient(follow_redirects=True, timeout=60.0) as client:
        limit = 1000
        offset = 0
        
        while True:
            for _ in range(3):
                try:
                    response = await client.get(API_URL, params={"limit": limit, "offset": offset})
                    response.raise_for_status()
                    break
                except httpx.HTTPStatusError as e:
                    if e.response.status_code != 401:
                        print(f"Error fetching data: {e}, retrying...")
                    await asyncio.sleep(1)
            else:
                print("Failed to fetch after 3 attempts.")
                break
                
            data = response.json()
            items = data.get("items", [])
            total = data.get("total", 0)
            
            if not items:
                break
                
            new_msgs = [item for item in items if item not in all_messages]
            
            all_messages.extend(items)
            offset += len(items)
            
            if len(all_messages) >= total:
                break
                
            await asyncio.sleep(0.5)

    print(f"Fetched {len(all_messages)} messages.")
    return all_messages
