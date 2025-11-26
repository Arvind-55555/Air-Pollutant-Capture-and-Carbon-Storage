import simpy
import logging
from .tools import SentinelTools, CompressorTools, LogisticsTools, GeologistTools, SafetyTools

logger = logging.getLogger("Agents")

class SentinelAgent:
    def __init__(self, env, tools: SentinelTools):
        self.env = env
        self.tools = tools

    def run(self):
        while True:
            # Monitor every 2 seconds
            yield self.env.timeout(2)
            levels = self.tools.read_sensors("Sector-7")
            if levels["NOx"] > 40 or levels["CO2"] > 800:
                logger.info("[Sentinel] POLLUTION SPIKE DETECTED! Signaling Compressor.")
                # In a real event bus, we'd publish an event. 
                # Here, we rely on the shared world state that the Compressor observes.

class CompressorAgent:
    def __init__(self, env, tools: CompressorTools, world):
        self.env = env
        self.tools = tools
        self.world = world

    def run(self):
        while True:
            yield self.env.timeout(1)
            if self.world.pollution_event_active:
                logger.info("[Compressor] Received capture signal. Starting intake.")
                # Simulate capture process
                gas = self.world.pollution_level
                captured = self.tools.activate_scrubber(gas)
                
                if captured:
                    status = self.tools.check_tank_pressure("Tank-001")
                    if status == "SEALED":
                        logger.info("[Compressor] Tank sealed. Signaling Logistics.")

class LogisticsAgent:
    def __init__(self, env, tools: LogisticsTools, world):
        self.env = env
        self.tools = tools
        self.world = world

    def run(self):
        while True:
            yield self.env.timeout(1)
            if self.world.is_tank_sealed and self.world.truck_location != "OFFSHORE":
                logger.info("[Logistics] Tank ready for transport.")
                success = self.tools.dispatch_truck("Tank-001", "OFFSHORE")
                if success:
                    yield self.env.timeout(5) # Travel time
                    logger.info("[Logistics] Arrived at Offshore Platform.")

class GeologistAgent:
    def __init__(self, env, tools: GeologistTools, world):
        self.env = env
        self.tools = tools
        self.world = world

    def run(self):
        while True:
            yield self.env.timeout(1)
            # Check if truck arrived with full tank
            if self.world.truck_location == "OFFSHORE" and self.world.is_tank_sealed:
                logger.info("[Geologist] Tank arrived. Analyzing seabed...")
                safety = self.tools.analyze_seabed("Basalt-Formation-A")
                
                if safety == "SAFE":
                    yield self.env.timeout(2) # Injection time
                    self.tools.inject_gas("Well-4", 1000)
                    # Reset truck
                    self.world.truck_location = "DEPOT"
                else:
                    logger.error("[Geologist] UNSAFE CONDITIONS. Halting injection.")

class GuardianAgent:
    def __init__(self, env, tools: SafetyTools):
        self.env = env
        self.tools = tools

    def run(self):
        while True:
            yield self.env.timeout(1)
            status = self.tools.read_system_status()
            if status["leak_detected"]:
                logger.critical("[Guardian] LEAK DETECTED! INITIATING EMERGENCY STOP.")
                self.tools.emergency_stop()
                # Break out of loop or just keep ensuring stop is active
