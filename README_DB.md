PostgreSQL persistence for CCS Multi-Agent prototype
===================================================

Files added in: /mnt/data/ccs_multiagent_project

- db.py            : SQLAlchemy engine + session (reads DATABASE_URL)
- models.py        : Declarative models + Base.metadata
- crud.py          : Simple CRUD helpers used by agents/server
- alembic/         : Alembic environment and an initial migration (0001_initial.py)
- requirements.txt : dependencies for migrations and DB access

Quickstart (local)
------------------
1. Install dependencies (in a virtualenv):
   pip install -r /mnt/data/ccs_multiagent_project/requirements.txt

2. Configure DATABASE_URL environment variable:
   export DATABASE_URL='postgresql+psycopg2://USER:PASSWORD@HOST:PORT/DBNAME'

   If DATABASE_URL is not set, db.py falls back to a local sqlite file: ccs_dev.db

3. Run alembic migrations:
   cd /mnt/data/ccs_multiagent_project
   alembic -c alembic.ini upgrade head

   NOTE: alembic.ini is not provided here; an alternative is to run a simple script to create tables:
   >>> python -c "from db import engine; from models import Base; Base.metadata.create_all(bind=engine)"

Integration notes
-----------------
- To persist incoming events from server.py endpoints, call the functions in crud.py:
    from crud import create_pollution_event, create_tank, create_manifest, create_injection_report, create_guardian_alert

  For example, in server.post('/events/pollution') after adding to queues also call:
    create_pollution_event(event_dict)

- Alembic's env.py expects DATABASE_URL to be set in the environment for online migrations.

Security
--------
- Never commit real DB credentials. Use environment variables and a secrets manager for production.

Original uploaded design file (for reference):
- /mnt/data/This is a complex engineering.txt
