
from fastapi import FastAPI, BackgroundTasks, Response
from crud import create_pollution_event, create_tank


from pydantic import BaseModel
import asyncio
import json
import time
import queue

from fastapi import APIRouter, Query
from typing import Any, Dict, List
import queue
from server import sync_event_bus   # or import your event bus depending on path

router = APIRouter()

@router.get("/debug/drain_events")
def drain_events(limit: int = Query(50, ge=1, le=500)) -> Dict[str, Any]:
    """
    Drain up to N events from sync_event_bus and return them.
    Dashboard-friendly format.
    """
    drained_events: List[Dict[str, Any]] = []
    for _ in range(limit):
        try:
            item = sync_event_bus.get_nowait()
            drained_events.append(item)
        except queue.Empty:
            break
    return {"drained": len(drained_events), "events": drained_events}

# Shared in-memory event buses
event_bus = asyncio.Queue()   # async queue for real async use
sync_event_bus = queue.Queue()  # synchronous queue for demo/simulation

app = FastAPI(title="CCS Multi-Agent API (Sim Prototype)")

class PollutionEvent(BaseModel):
    event_id: str
    source_id: str
    source_type: str
    species: dict
    units: dict | None = None
    timestamp: str
    confidence: float | None = 1.0
    feasibility_flag: bool | None = True

class TankReady(BaseModel):
    tank_id: str
    mass_co2_kg: float
    pressure_psi: float
    sealed: bool
    origin: str
    timestamp: str

@app.on_event('startup')
async def startup_event():
    print('API startup: event bus ready.')

@app.get('/health')
def health():
    return {'status':'OK','timestamp':time.time()}
@app.get('/')
def root():
    return {"message": "Welcome to the CCS Multi-Agent API"}
@app.get('/favicon.ico')
def favicon():
    return Response(status_code=204)



@app.post('/events/pollution', status_code=202)
async def post_pollution(event: PollutionEvent):
    payload = {'type':'pollution_event', 'payload': json.loads(event.json())}
    # push to both async and sync buses for demo interoperability
    await event_bus.put(payload)
    try:
        sync_event_bus.put_nowait(payload)
    except Exception:
        pass
    create_pollution_event(json.loads(event.json()))
    return {'status':'accepted','event_id': event.event_id}

@app.post('/capture/tank_ready', status_code=201)
async def post_tank_ready(tank: TankReady):
    payload = {'type':'tank_ready', 'payload': json.loads(tank.json())}
    await event_bus.put(payload)
    try:
        sync_event_bus.put_nowait(payload)
    except Exception:
        pass
    return {'status':'scheduled','tank_id': tank.tank_id}

@app.get('/debug/drain_events')
async def drain_events(limit: int = 20):
    events = []
    for _ in range(limit):
        if event_bus.empty():
            break
        events.append(await event_bus.get())
    return {'drained': len(events), 'events': events}
