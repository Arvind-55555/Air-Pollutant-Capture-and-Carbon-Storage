#!/bin/bash

# Root folder
mkdir -p ccs-multiagent-system
cd ccs-multiagent-system

##############################
# BACKEND
##############################
mkdir -p backend/app/api/routes
mkdir -p backend/app/core
mkdir -p backend/app/db/migrations
mkdir -p backend/app/events/handlers
mkdir -p backend/app/schemas
mkdir -p backend/app/agents

touch backend/app/api/routes/pollution.py
touch backend/app/api/routes/tanks.py
touch backend/app/api/routes/manifests.py
touch backend/app/api/routes/injection.py
touch backend/app/api/routes/guardian.py
touch backend/app/api/routes/health.py

touch backend/app/api/deps.py

touch backend/app/core/config.py
touch backend/app/core/security.py
touch backend/app/core/logging_conf.py

touch backend/app/db/db.py
touch backend/app/db/models.py
touch backend/app/db/crud.py
# migrations folder will be used by Alembic

touch backend/app/events/bus.py
touch backend/app/events/handlers/on_pollution.py
touch backend/app/events/handlers/on_tank_ready.py
touch backend/app/events/handlers/on_manifest.py
touch backend/app/events/handlers/on_injection.py
touch backend/app/events/handlers/on_alert.py

touch backend/app/schemas/pollution.py
touch backend/app/schemas/tanks.py
touch backend/app/schemas/manifests.py
touch backend/app/schemas/injection.py
touch backend/app/schemas/guardian.py

touch backend/app/agents/sentinel.py
touch backend/app/agents/compressor.py
touch backend/app/agents/hauler.py
touch backend/app/agents/geologist.py
touch backend/app/agents/guardian.py

touch backend/app/main.py
touch backend/app/dependencies.py
touch backend/app/utils.py

touch backend/requirements.txt
touch backend/Dockerfile
touch backend/gunicorn_conf.py

##############################
# AGENTS (External runner)
##############################
mkdir -p agents/configs
touch agents/agent_runner.py
touch agents/Dockerfile
touch agents/configs/agent_settings.yaml

##############################
# INFRASTRUCTURE
##############################
mkdir -p infra/docker
mkdir -p infra/k8s
mkdir -p infra/terraform

touch infra/docker/docker-compose.dev.yml
touch infra/docker/docker-compose.prod.yml

touch infra/k8s/api-deployment.yaml
touch infra/k8s/api-service.yaml
touch infra/k8s/db-statefulset.yaml
touch infra/k8s/ingress.yaml
touch infra/k8s/agents-deployment.yaml

touch infra/terraform/main.tf
touch infra/terraform/variables.tf

##############################
# FRONTEND
##############################
mkdir -p frontend/src
mkdir -p frontend/public
touch frontend/Dockerfile
touch frontend/vite.config.js

##############################
# TESTS
##############################
mkdir -p tests/api
mkdir -p tests/db
mkdir -p tests/agents
mkdir -p tests/integration

##############################
# SCRIPTS
##############################
mkdir -p scripts
touch scripts/init_db.py
touch scripts/refresh_migrations.sh
touch scripts/run_all_agents.sh

##############################
# ROOT FILES
##############################
touch .env.example
touch .gitignore
touch README.md
touch LICENSE

echo "✅ Project structure created successfully!"
