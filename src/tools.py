import logging
import requests
import json
from datetime import datetime
from .simulation import WorldState

logger = logging.getLogger("Tools")
API_URL = "http://localhost:8000/events/ingest"

def send_event(event_type: str, payload: dict):
    """Helper to send events to the backend API."""
    try:
        event = {
            "type": event_type,
            "payload": payload,
            "timestamp": datetime.utcnow().isoformat() + "Z"
        }
        requests.post(API_URL, json=event, timeout=0.5)
    except Exception as e:
        logger.warning(f"Failed to send event to API: {e}")

class BaseTool:
    def __init__(self, world: WorldState):
        self.world = world

class SentinelTools(BaseTool):
    def read_sensors(self, sector_id: str):
        """Reads current pollution levels from the simulation."""
        levels = self.world.pollution_level
        logger.info(f"[Sentinel] Reading sensors at {sector_id}: {levels}")
        # Optional: Send sensor data as a generic event for debugging
        # send_event("sensor_reading", {"sector": sector_id, "levels": levels})
        return levels

class CompressorTools(BaseTool):
    def activate_scrubber(self, gas_composition: dict):
        """Filters gas. Returns True if CO2 is captured, False if vented."""
        if "CO2" in gas_composition and gas_composition["CO2"] > 500: # Threshold
            logger.info("[Compressor] High CO2 detected. Activating amine scrubbers.")
            # Simulate filling the tank
            self.world.current_tank_level += 100
            self.world.tank_pressure += 300
            logger.info(f"[Compressor] Tank Level: {self.world.current_tank_level}kg, Pressure: {self.world.tank_pressure} PSI")
            return True
        else:
            logger.info("[Compressor] Gas composition normal (mostly N2/O2). Venting to atmosphere.")
            return False

    def check_tank_pressure(self, tank_id: str):
        """Checks if tank is ready for transport."""
        if self.world.tank_pressure >= 2900:
            self.world.is_tank_sealed = True
            logger.info(f"[Compressor] Tank {tank_id} at capacity ({self.world.tank_pressure} PSI). SEALING.")
            
            # Emit tank_ready event
            payload = {
                "tank_id": tank_id,
                "origin": "Refinery-Sector-7",
                "mass_co2_kg": self.world.current_tank_level,
                "pressure_psi": self.world.tank_pressure,
                "sealed": True
            }
            send_event("tank_ready", payload)
            return "SEALED"
        return "FILLING"

class LogisticsTools(BaseTool):
    def dispatch_truck(self, tank_id: str, destination: str):
        """Dispatches a truck to move the tank."""
        if not self.world.is_tank_sealed:
            logger.warning(f"[Logistics] Cannot dispatch {tank_id}. Tank is not sealed!")
            return False
        
        logger.info(f"[Logistics] Dispatching truck for {tank_id} to {destination}.")
        # Simulate transport (instant in this step, but consumes resource in real sim)
        with self.world.trucks_available.request() as req:
            # yield req # In a real agent loop we would yield, but for tools we just check availability
            logger.info(f"[Logistics] Truck assigned. Moving to {destination}...")
            self.world.truck_location = destination
            return True

class GeologistTools(BaseTool):
    def analyze_seabed(self, location: str):
        """Checks geological stability."""
        pressure = self.world.seabed_pressure
        fracture_limit = self.world.fracture_pressure
        logger.info(f"[Geologist] Analyzing {location}. Pressure: {pressure} Bar. Fracture Limit: {fracture_limit} Bar.")
        
        if pressure < fracture_limit * 0.9:
            return "SAFE"
        else:
            return "UNSAFE"

    def inject_gas(self, well_id: str, amount_kg: float):
        """Injects gas if safe."""
        if self.analyze_seabed("Current Well") == "SAFE":
            logger.info(f"[Geologist] Injecting {amount_kg}kg into {well_id}.")
            self.world.current_tank_level = 0 # Empty tank
            self.world.tank_pressure = 0
            self.world.is_tank_sealed = False
            self.world.injection_status = "SUCCESS"
            
            # Emit injection_report event
            payload = {
                "well_id": well_id,
                "tank_id": "Tank-001", # Simplified
                "status": "injected",
                "mass_tonnes": amount_kg / 1000.0,
            }
            send_event("injection_report", payload)
            return True
        else:
            logger.warning(f"[Geologist] Injection ABORTED at {well_id}. Risk of fracture!")
            return False

class SafetyTools(BaseTool):
    def read_system_status(self):
        """Checks for leaks or anomalies."""
        status = {
            "leak_detected": self.world.leak_detected,
            "tank_pressure": self.world.tank_pressure,
            "pollution_levels": self.world.pollution_level
        }
        return status

    def emergency_stop(self):
        """Halts all operations."""
        logger.critical("[Guardian] EMERGENCY STOP TRIGGERED! Halting all agents.")
        self.world.emergency_stop_triggered = True
        
        # Emit guardian_alert event
        payload = {
            "alert_level": "CRITICAL",
            "message": "Leak detected! System halted.",
            "location": "Pipeline-Segment-B"
        }
        send_event("guardian_alert", payload)
        return "SYSTEM_HALTED"
