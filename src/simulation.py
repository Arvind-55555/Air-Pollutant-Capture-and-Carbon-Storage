import simpy
import random
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Simulation")

class WorldState:
    def __init__(self, env):
        self.env = env
        
        # Pollution State
        self.pollution_level = {"NOx": 10, "CO2": 400} # Baseline ppm
        self.pollution_threshold = {"NOx": 50, "CO2": 1000}
        self.pollution_event_active = False
        
        # Tank State
        self.tank_capacity = 1000 # kg
        self.current_tank_level = 0
        self.tank_pressure = 0 # PSI
        self.max_safe_pressure = 3000
        self.is_tank_sealed = False
        
        # Logistics State
        self.trucks_available = simpy.Resource(env, capacity=3)
        self.truck_location = "DEPOT" # DEPOT, HIGHWAY, OFFSHORE
        
        # Geology State
        self.seabed_pressure = 500 # Bar
        self.fracture_pressure = 800 # Bar
        self.injection_status = "IDLE"
        
        # Safety State
        self.emergency_stop_triggered = False
        self.leak_detected = False

    def update_pollution(self):
        """Randomly fluctuate pollution levels."""
        while True:
            yield self.env.timeout(1)
            if not self.emergency_stop_triggered:
                # Random walk
                self.pollution_level["NOx"] += random.randint(-5, 10)
                self.pollution_level["CO2"] += random.randint(-10, 20)
                
                # Ensure non-negative
                self.pollution_level["NOx"] = max(0, self.pollution_level["NOx"])
                self.pollution_level["CO2"] = max(0, self.pollution_level["CO2"])
                
                # Check for spikes
                if (self.pollution_level["NOx"] > self.pollution_threshold["NOx"] or 
                    self.pollution_level["CO2"] > self.pollution_threshold["CO2"]):
                    self.pollution_event_active = True
                else:
                    self.pollution_event_active = False

    def simulate_leak(self):
        """Randomly simulate a leak event."""
        while True:
            yield self.env.timeout(random.randint(20, 100))
            if random.random() < 0.1: # 10% chance of leak when check runs
                logger.warning("SIMULATION: LEAK STARTED!")
                self.leak_detected = True

    def run(self):
        self.env.process(self.update_pollution())
        self.env.process(self.simulate_leak())
