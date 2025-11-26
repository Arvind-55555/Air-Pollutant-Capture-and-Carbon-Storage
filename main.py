import simpy
import logging
from src.simulation import WorldState
from src.tools import SentinelTools, CompressorTools, LogisticsTools, GeologistTools, SafetyTools
from src.agents import SentinelAgent, CompressorAgent, LogisticsAgent, GeologistAgent, GuardianAgent

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("Main")

def main():
    logger.info("Initializing CCS Multi-Agent System Simulation...")
    
    # 1. Setup Environment
    env = simpy.Environment()
    world = WorldState(env)
    
    # 2. Setup Tools
    sentinel_tools = SentinelTools(world)
    compressor_tools = CompressorTools(world)
    logistics_tools = LogisticsTools(world)
    geologist_tools = GeologistTools(world)
    safety_tools = SafetyTools(world)
    
    # 3. Setup Agents
    sentinel = SentinelAgent(env, sentinel_tools)
    compressor = CompressorAgent(env, compressor_tools, world)
    logistics = LogisticsAgent(env, logistics_tools, world)
    geologist = GeologistAgent(env, geologist_tools, world)
    guardian = GuardianAgent(env, safety_tools)
    
    # 4. Start Processes
    world.run() # Start world physics
    env.process(sentinel.run())
    env.process(compressor.run())
    env.process(logistics.run())
    env.process(geologist.run())
    env.process(guardian.run())
    
    # 5. Run Simulation
    logger.info("Starting Simulation (Duration: 100 ticks)...")
    env.run(until=100)
    logger.info("Simulation Complete.")

if __name__ == "__main__":
    main()
