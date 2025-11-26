from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict, Any, Optional
from collections import deque
import time

app = FastAPI(title='Pollutant Absorber + Carbon Capture API')

# In-memory event store (acting as a queue)
EVENT_QUEUE = deque(maxlen=1000)

class Event(BaseModel):
    type: str
    payload: Dict[str, Any]
    timestamp: Optional[str] = None

class DrainResponse(BaseModel):
    drained: int
    events: List[Event]

@app.get('/')
def root():
    return {'message': 'Welcome to the CCS Multi-Agent API'}

@app.post('/events/ingest')
async def ingest_event(event: Event):
    """Receive an event from the simulation agents."""
    if not event.timestamp:
        event.timestamp = str(time.time())
    EVENT_QUEUE.append(event)
    return {"status": "received", "queue_size": len(EVENT_QUEUE)}

@app.get('/debug/drain_events', response_model=DrainResponse)
async def drain_events(limit: int = 50):
    """Return and remove events from the queue (simulating a stream)."""
    events = []
    count = 0
    while EVENT_QUEUE and count < limit:
        events.append(EVENT_QUEUE.popleft())
        count += 1
    return {"drained": count, "events": events}

# Health check
@app.get('/health')
def health():
    return {"status": "ok"}
