from pathlib import Path
LEGACY_MODELS = Path('/mnt/data/ccs_multiagent_project/models.py')
if LEGACY_MODELS.exists():
    import importlib.util, sys
    spec = importlib.util.spec_from_file_location('legacy_models', str(LEGACY_MODELS))
    legacy_models = importlib.util.module_from_spec(spec)
    sys.modules['legacy_models'] = legacy_models
    spec.loader.exec_module(legacy_models)
    Base = getattr(legacy_models, 'Base', None)
else:
    # Minimal SQLAlchemy Base for scaffolding only
    from sqlalchemy.orm import declarative_base
    Base = declarative_base()
