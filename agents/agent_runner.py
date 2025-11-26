"""
Agent Runner System for CCS Multi-Agent Prototype

This runner integrates with the demo FastAPI scaffold in the same workspace.
It uses the synchronous demo event bus `server.sync_event_bus` to communicate with the API
and other components (server.py and sim.py).

Uploaded design file (project reference):
/mnt/data/This is a complex engineering.txt

Usage:
    python agent_runner.py

Notes:
- This is a demo local runner suitable for development and testing.
- For production, replace sync_event_bus with a distributed event bus (Kafka/PubSub).
"""

import threading
import time
import queue
import requests
import json
import sys
import os
from datetime import datetime

# Ensure project path is on import path
sys.path.append(os.path.dirname(__file__))

import server  # imports the demo FastAPI scaffold; uses server.sync_event_bus (queue.Queue)

SYNC_BUS = server.sync_event_bus  # queue.Queue

API_BASE = os.environ.get("CCS_API_BASE", "http://localhost:8000")

STOP_FLAG = threading.Event()

def sentinel_thread(interval=6):
    """Periodically publish pollution_event into sync bus (and optionally HTTP)"""
    i = 0
    while not STOP_FLAG.is_set():
        evt = {
            "event_id": f"evt-sentinel-{int(time.time())}-{i}",
            "source_id": "refinery-koyali-01",
            "source_type": "point_source",
            "species": {"CO2": 5000 + i*10},
            "units": {"CO2": "ppm"},
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "confidence": 0.99,
            "feasibility_flag": True,
        }
        try:
            SYNC_BUS.put_nowait({"type": "pollution_event", "payload": evt})
        except Exception:
            pass
        # Also demonstrate HTTP ingest path (non-blocking)
        try:
            requests.post(f"{API_BASE}/events/pollution", json=evt, timeout=2)
        except Exception:
            # API may be offline in your environment; continue silently
            pass
        print(f"[Sentinel] emitted {evt['event_id']} CO2={evt['species']['CO2']} ppm")
        i += 1
        time.sleep(interval)

def compressor_thread():
    """Consume pollution_event, simulate capture for a fixed time, emit tank_ready"""
    capture_time = 5
    tank_counter = 0
    while not STOP_FLAG.is_set():
        try:
            item = SYNC_BUS.get(timeout=1)
        except queue.Empty:
            continue
        if item["type"] != "pollution_event":
            # requeue for others
            try:
                SYNC_BUS.put_nowait(item)
            except Exception:
                pass
            continue
        event = item["payload"]
        print(f"[Compressor] starting capture for {event['event_id']}")
        # Simulate capture duration with step checks for stop flag
        remaining = capture_time
        while remaining > 0 and not STOP_FLAG.is_set():
            time.sleep(1)
            remaining -= 1
        if STOP_FLAG.is_set():
            break
        tank_counter += 1
        tank = {
            "tank_id": f"TANK-R-{tank_counter:04d}",
            "mass_co2_kg": 5000.0,
            "pressure_psi": 2950.0,
            "sealed": True,
            "origin": event["source_id"],
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        try:
            SYNC_BUS.put_nowait({"type": "tank_ready", "payload": tank})
        except Exception:
            pass
        # Also call HTTP endpoint
        try:
            requests.post(f"{API_BASE}/capture/tank_ready", json=tank, timeout=2)
        except Exception:
            pass
        print(f"[Compressor] sealed {tank['tank_id']} from {tank['origin']}")

def hauler_thread():
    """Consume tank_ready, simulate transport, emit delivered_to_port"""
    vehicle_seq = 1000
    while not STOP_FLAG.is_set():
        try:
            item = SYNC_BUS.get(timeout=1)
        except queue.Empty:
            continue
        if item["type"] != "tank_ready":
            # requeue
            try:
                SYNC_BUS.put_nowait(item)
            except Exception:
                pass
            continue
        tank = item["payload"]
        vehicle_seq += 1
        vehicle = f"HV-TRUCK-{vehicle_seq}"
        print(f"[Hauler] assigned {vehicle} for {tank['tank_id']} from {tank['origin']}")
        # simulate travel time
        for _ in range(2):
            if STOP_FLAG.is_set():
                break
            time.sleep(1)
        arrival_evt = {
            "manifest_id": f"MAN-{tank['tank_id']}",
            "tank_id": tank["tank_id"],
            "assigned_vehicle": vehicle,
            "from": tank["origin"],
            "to": "OFFSHORE_RIG_ALPHA",
            "eta": None,
        }
        try:
            SYNC_BUS.put_nowait({"type": "delivered_to_port", "payload": arrival_evt})
        except Exception:
            pass
        print(f"[Hauler] delivered {arrival_evt['tank_id']} to port via {vehicle}")

def geologist_thread():
    """Consume delivered_to_port, perform a simple safety check, emit injection_report or guardian_alert"""
    while not STOP_FLAG.is_set():
        try:
            item = SYNC_BUS.get(timeout=1)
        except queue.Empty:
            continue
        if item["type"] != "delivered_to_port":
            try:
                SYNC_BUS.put_nowait(item)
            except Exception:
                pass
            continue
        manifest = item["payload"]
        print(f"[Geologist] analyzing {manifest['tank_id']} for injection")
        # simplified safety check (always pass in demo)
        time.sleep(1)
        injection = {
            "well_id": "INJ-W-04",
            "tank_id": manifest["tank_id"],
            "status": "injected",
            "mass_tonnes": 5.0,
            "timestamp": datetime.utcnow().isoformat() + "Z",
        }
        try:
            SYNC_BUS.put_nowait({"type": "injection_report", "payload": injection})
        except Exception:
            pass
        print(f"[Geologist] injection complete for {manifest['tank_id']}")

def guardian_thread():
    """Monitor for injection reports and guardian alerts; escalate if needed"""
    while not STOP_FLAG.is_set():
        try:
            item = SYNC_BUS.get(timeout=1)
        except queue.Empty:
            continue
        if item["type"] == "injection_report":
            print(f"[Guardian] injection_report OK for {item['payload']['tank_id']}")
            # in production, send to Slack/Twilio/Regulator here
        elif item["type"] == "guardian_alert":
            print(f"[Guardian] ALERT -> {item['payload']}")
            # escalate immediately (HIL)
        else:
            # requeue for other agents
            try:
                SYNC_BUS.put_nowait(item)
            except Exception:
                pass
        time.sleep(0.1)

def start_agents():
    threads = []
    t_sent = threading.Thread(target=sentinel_thread, args=(6,), daemon=True, name="Sentinel")
    t_comp = threading.Thread(target=compressor_thread, daemon=True, name="Compressor")
    t_haul = threading.Thread(target=hauler_thread, daemon=True, name="Hauler")
    t_geo = threading.Thread(target=geologist_thread, daemon=True, name="Geologist")
    t_guard = threading.Thread(target=guardian_thread, daemon=True, name="Guardian")

    threads.extend([t_sent, t_comp, t_haul, t_geo, t_guard])
    for t in threads:
        t.start()
    return threads

if __name__ == "__main__":
    print("Starting agent runner. Press Ctrl+C to stop.")
    threads = start_agents()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Shutdown requested. Stopping agents...")
        STOP_FLAG.set()
        time.sleep(2)
        print("Agents stopped.")
