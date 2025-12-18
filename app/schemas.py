from pydantic import BaseModel, Field
from typing import List, Optional, Any

class Message(BaseModel):
    """Represents a single message item."""
    id: str = Field(..., description="Unique identifier of the message")
    message: str = Field(..., description="Content of the message")
    user_name: str = Field(..., description="Author of the message")
    # Allow extra fields if the API returns more data (like timestamps)
    model_config = {"extra": "allow"} 

class SearchResponse(BaseModel):
    """Response model for the search endpoint."""
    query: str = Field(..., description="The search query used")
    total: int = Field(..., description="Total number of matching results")
    items: List[Message] = Field(..., description="List of matching message items")
    limit: int = Field(..., description="Limit used for pagination")
    offset: int = Field(..., description="Offset used for pagination")
    time_ms: float = Field(..., description="Time taken to execute search in milliseconds")

class BenchmarkResponse(BaseModel):
    """Response model for the benchmark endpoint."""
    queries_run: int = Field(..., description="Number of queries executed")
    avg_ms: float = Field(..., description="Average latency in ms")
    min_ms: float = Field(..., description="Minimum latency in ms")
    max_ms: float = Field(..., description="Maximum latency in ms")
    p95_ms: float = Field(..., description="95th percentile latency in ms")
    p99_ms: float = Field(..., description="99th percentile latency in ms")

class HealthResponse(BaseModel):
    """Response model for the health check."""
    status: str = Field(..., description="Service status")
