import os
from pathlib import Path

# This file bootstraps DB. You can replace with the project's db.py implementation.
LEGACY_DB = Path('/mnt/data/ccs_multiagent_project/db.py')
if LEGACY_DB.exists():
    # import legacy module by path - copy it into this project for quick reuse
    import importlib.util, sys
    spec = importlib.util.spec_from_file_location('legacy_db', str(LEGACY_DB))
    legacy_db = importlib.util.module_from_spec(spec)
    sys.modules['legacy_db'] = legacy_db
    spec.loader.exec_module(legacy_db)
    engine = getattr(legacy_db, 'engine', None)
    SessionLocal = getattr(legacy_db, 'SessionLocal', None)
    def init_db():
        try:
            from models import Base
            if engine is not None:
                Base.metadata.create_all(bind=engine)
        except Exception as e:
            print('legacy init_db error', e)
else:
    # fallback simple sqlite
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker
    DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///./pollutant_ccs_dev.db')
    engine = create_engine(DATABASE_URL, echo=False, future=True)
    SessionLocal = sessionmaker(bind=engine)
    def init_db():
        print('No legacy DB found; using simple sqlite, create tables manually.')
