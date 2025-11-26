import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import OperationalError

# ------------------------------------------------------------
# Database configuration
# ------------------------------------------------------------
# Read the DATABASE_URL environment variable. If it is not set or contains
# placeholder values (e.g. "USER" or "PASSWORD"), fall back to a local SQLite
# database so the application can run without a real PostgreSQL server.
# ------------------------------------------------------------
raw_url = os.getenv("DATABASE_URL")

def _is_placeholder(url: str) -> bool:
    """Return True if the URL looks like it still contains placeholder credentials.
    This is a simple heuristic – we check for the literal strings 'USER' or
    'PASSWORD' (case‑insensitive) in the URL.
    """
    if not url:
        return True
    lowered = url.lower()
    return "user" in lowered and "password" in lowered and ("user" in lowered.split("://")[1].split(":")[0] or "password" in lowered)

# Determine which URL to use
if raw_url is None or _is_placeholder(raw_url):
    # No valid PostgreSQL URL – use SQLite for local development
    DATABASE_URL = "sqlite:///./ccs_dev.db"
    print("⚠️ Using fallback SQLite database (no valid DATABASE_URL provided).")
else:
    DATABASE_URL = raw_url

# ------------------------------------------------------------
# Engine creation – try PostgreSQL first, fall back to SQLite on error
# ------------------------------------------------------------
try:
    engine = create_engine(DATABASE_URL, echo=False, future=True)
    # Test the connection (this will raise OperationalError if PostgreSQL is unreachable)
    with engine.connect() as _:
        pass
except OperationalError as exc:
    # If we tried PostgreSQL and it failed, switch to SQLite
    print(f"⚠️ Could not connect to PostgreSQL ({DATABASE_URL}): {exc}\n   Falling back to SQLite.")
    DATABASE_URL = "sqlite:///./ccs_dev.db"
    engine = create_engine(DATABASE_URL, echo=False, future=True)

# Session factory
SessionLocal = sessionmaker(bind=engine, autoflush=False, autocommit=False, future=True)

def get_session():
    """Convenient helper to obtain a new DB session.
    Use it with a context manager: `with get_session() as db:`
    """
    return SessionLocal()

# Export Base for model definitions
from sqlalchemy.orm import declarative_base
Base = declarative_base()
