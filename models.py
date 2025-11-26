from sqlalchemy import Column, Integer, String, DateTime, JSON, Float, Boolean, Text
from sqlalchemy.sql import func
from sqlalchemy.orm import declarative_base

Base = declarative_base()
metadata = Base.metadata

class PollutionEvent(Base):
    __tablename__ = 'pollution_events'
    id = Column(Integer, primary_key=True, index=True)
    event_id = Column(String(128), unique=True, index=True, nullable=False)
    source_id = Column(String(128))
    source_type = Column(String(64))
    species = Column(JSON)
    units = Column(JSON)
    confidence = Column(Float)
    feasibility_flag = Column(Boolean)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    raw = Column(JSON)

class Tank(Base):
    __tablename__ = 'tanks'
    id = Column(Integer, primary_key=True, index=True)
    tank_id = Column(String(128), unique=True, index=True, nullable=False)
    mass_co2_kg = Column(Float)
    pressure_psi = Column(Float)
    sealed = Column(Boolean)
    origin = Column(String(128))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    raw = Column(JSON)

class TransportManifest(Base):
    __tablename__ = 'transport_manifests'
    id = Column(Integer, primary_key=True, index=True)
    manifest_id = Column(String(128), unique=True, index=True, nullable=False)
    tank_id = Column(String(128))
    assigned_vehicle = Column(String(128))
    origin = Column(String(128))
    destination = Column(String(128))
    eta = Column(String(64))
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    raw = Column(JSON)

class InjectionReport(Base):
    __tablename__ = 'injection_reports'
    id = Column(Integer, primary_key=True, index=True)
    well_id = Column(String(128))
    tank_id = Column(String(128))
    status = Column(String(64))
    mass_tonnes = Column(Float)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    raw = Column(JSON)

class GuardianAlert(Base):
    __tablename__ = 'guardian_alerts'
    id = Column(Integer, primary_key=True, index=True)
    alert_id = Column(String(128), unique=True, index=True)
    severity = Column(String(32))
    reason = Column(Text)
    action = Column(String(64))
    details = Column(JSON)
    notify = Column(JSON)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    raw = Column(JSON)
