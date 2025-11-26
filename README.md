# Multi-Agent Platform for Atmospheric Pollutant Capture & Subsea Geological Storage

A **Multi‑Agent AI System** for urban air‑pollution capture and deep‑seabed carbon sequestration.

---

## Overview

This project tackles a complex engineering and environmental challenge: **capture harmful gases** (CO₂, NOx, SOx, PM, VOCs) from highways and industrial zones, compress and store them safely, transport sealed canisters, and finally inject the pollutants into geologically stable formations beneath the ocean floor.

The system integrates:

- Environmental & chemical engineering
- Carbon‑capture (CCS) workflows
- Distributed, event‑driven architecture
- Multi‑agent AI orchestration
- Real‑time geospatial & geological modeling
- Safety, compliance, and audit logging

---
## Live Demo
[![View Artifact](https://img.shields.io/badge/View%20Artifact-%230077B5.svg?style=for-the-badge&logo=claude&logoColor=white)](https://claude.ai/public/artifacts/5e8e6f15-c942-4f15-9caa-66509ee90a87)

---

## System Goals

- **Detect** and quantify air‑pollution hotspots.
- **Capture** pollutants using absorber units and compress them into high‑pressure chambers.
- **Transport** sealed chambers safely to coastal or offshore injection sites.
- **Inject** pollutants into deep‑seabed formations for long‑term storage.
- **Automate** coordination with a multi‑agent AI system.
- **Maintain** safety, regulatory compliance, and continuous monitoring.

---

## Multi‑Agent Architecture

| Agent | Role | Core Responsibilities |
|-------|------|------------------------|
| **Sentinel** | Monitoring | Scan air‑quality sensors, detect spikes, emit pollution events |
| **Compressor** | Capture & Compression | Activate absorber, compress gases, seal chambers, emit `tank_ready` |
| **Hauler** | Transport Logistics | Optimize routes, classify hazards, coordinate pickup/delivery |
| **Geologist** | Sub‑surface Planning | Evaluate geological suitability, approve injection, plan rates |
| **Guardian** | Safety & Compliance | Risk detection, emergency response, audit logs, human‑in‑the‑loop approvals |

### Workflow

```
Sentinel → Compressor → Hauler → Geologist → Guardian
```

1. **Detection** – Sentinel detects elevated pollutant levels and publishes a `pollution_event`.
2. **Capture** – Compressor absorbs the gases, fills a tank, and publishes a `tank_ready` event.
3. **Transport** – Hauler assigns a vehicle, calculates the optimal route, and delivers the tank to the injection port.
4. **Injection** – Geologist validates the geological formation and approves the injection.
5. **Safety** – Guardian logs the operation, checks compliance, and raises alerts if needed.

---

## Technologies Used

- **FastAPI** – API orchestration
- **PostgreSQL** (fallback **SQLite**) – Event persistence
- **Alembic** – Database migrations
- **Python** – Core logic, multi‑threading for agent runners
- **Queue‑based Event Bus** – Inter‑agent messaging
- **Docker** – Containerisation
- **Future‑ready**: Kafka, Kubernetes, LangGraph / CrewAI for advanced agent intelligence

---

##  Engineering & Environmental Challenges

1. **Pollutant capture efficiency** – Different gases require specific absorber media and pressures.
2. **Compression & chamber safety** – Maintaining safe temperature and pressure limits.
3. **Transport risk classification** – High‑pressure CO₂ is a hazardous cargo.
4. **Geological suitability** – Requires analysis of porosity, permeability, fault‑line stability, depth pressure gradients.
5. **Regulatory compliance** – Must obey MARPOL, IMO, and local coastal regulations.

---

## Use Cases

- Smart roadside CO₂ mitigation booths
- Highway pollution absorption stations
- Industrial air‑pollutant processing plants
- Offshore CO₂ sequestration facilities
- Urban emergency air‑quality response
- National‑level carbon‑neutrality projects

---

## Role of AI

Each agent is autonomous and event‑driven. AI is employed for:

- Sensor anomaly detection
- Predictive maintenance
- Geological modelling & risk scoring
- Route optimisation
- Real‑time risk assessment
- Human‑in‑the‑loop decision making

---

## Quick‑Start (Development)

```bash
# 1. Set the database URL (or rely on the SQLite fallback)
export DATABASE_URL='postgresql+psycopg2://user:password@localhost:5432/ccs_db'

# 2. Install dependencies (inside the virtual‑env)
pip install -r requirements.txt

# 3. Run the API server
uvicorn server:app --reload --port 8000
```

The API will be available at <http://localhost:8000>.

---

## License & Contributions

This project is released under the **MIT License**. Contributions are welcome – feel free to open issues or submit pull requests.

---

