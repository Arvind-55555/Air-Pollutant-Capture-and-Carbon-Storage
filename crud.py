from db import get_session
from models import PollutionEvent, Tank, TransportManifest, InjectionReport, GuardianAlert
from sqlalchemy.exc import IntegrityError

def create_pollution_event(data: dict):
    db = get_session()
    try:
        ev = PollutionEvent(
            event_id = data.get('event_id'),
            source_id = data.get('source_id'),
            source_type = data.get('source_type'),
            species = data.get('species'),
            units = data.get('units'),
            confidence = data.get('confidence'),
            feasibility_flag = data.get('feasibility_flag'),
            raw = data
        )
        db.add(ev)
        db.commit()
        db.refresh(ev)
        return ev
    except IntegrityError:
        db.rollback()
        return None
    finally:
        db.close()

def create_tank(data: dict):
    db = get_session()
    try:
        t = Tank(
            tank_id = data.get('tank_id'),
            mass_co2_kg = data.get('mass_co2_kg'),
            pressure_psi = data.get('pressure_psi'),
            sealed = data.get('sealed'),
            origin = data.get('origin'),
            raw = data
        )
        db.add(t)
        db.commit()
        db.refresh(t)
        return t
    except IntegrityError:
        db.rollback()
        return None
    finally:
        db.close()

def create_manifest(data: dict):
    db = get_session()
    try:
        m = TransportManifest(
            manifest_id = data.get('manifest_id'),
            tank_id = data.get('tank_id'),
            assigned_vehicle = data.get('assigned_vehicle'),
            origin = data.get('from'),
            destination = data.get('to'),
            eta = data.get('eta'),
            raw = data
        )
        db.add(m)
        db.commit()
        db.refresh(m)
        return m
    finally:
        db.close()

def create_injection_report(data: dict):
    db = get_session()
    try:
        ir = InjectionReport(
            well_id = data.get('well_id'),
            tank_id = data.get('tank_id'),
            status = data.get('status'),
            mass_tonnes = data.get('mass_tonnes'),
            raw = data
        )
        db.add(ir)
        db.commit()
        db.refresh(ir)
        return ir
    finally:
        db.close()

def create_guardian_alert(data: dict):
    db = get_session()
    try:
        ga = GuardianAlert(
            alert_id = data.get('alert_id'),
            severity = data.get('severity'),
            reason = data.get('reason'),
            action = data.get('action'),
            details = data.get('details'),
            notify = data.get('notify'),
            raw = data
        )
        db.add(ga)
        db.commit()
        db.refresh(ga)
        return ga
    finally:
        db.close()
