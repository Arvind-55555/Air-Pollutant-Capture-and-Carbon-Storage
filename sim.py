
import time, sys, os
from datetime import datetime
sys.path.append(os.path.dirname(__file__))
import server
# use server.sync_event_bus

def push_sync(evt_type, payload):
    try:
        server.sync_event_bus.put_nowait({'type': evt_type, 'payload': payload})
    except Exception:
        pass

def run_sim(duration=30, sentinel_interval=6):
    now = 0
    capture_in_progress = None
    capture_timer = 0
    capture_time = 5  # hours
    hauler_tasks = []
    print('Starting synchronous time-stepped simulation for', duration, 'time units')
    while now < duration:
        # Sentinel emits every sentinel_interval
        if now % sentinel_interval == 0:
            evt = {
                'event_id': f'evt-{now}',
                'source_id': 'refinery-koyali-01',
                'source_type': 'point_source',
                'species': {'CO2': 5000 + now*10},
                'units': {'CO2': 'ppm'},
                'timestamp': datetime.utcnow().isoformat() + 'Z',
                'confidence': 0.98,
                'feasibility_flag': True
            }
            print(f'[{now:3}] Sentinel emits pollution_event -> CO2={evt["species"]["CO2"]} ppm')
            push_sync('pollution_event', evt)
        # Compressor: if not working and there's a pollution_event in queue, start capture
        try:
            item = server.sync_event_bus.get_nowait()
            if item['type'] == 'pollution_event' and capture_in_progress is None:
                capture_in_progress = item['payload']
                capture_timer = capture_time
                print(f'[{now:3}] Compressor: started capture for {capture_in_progress["event_id"]}')
            else:
                # requeue unknown items
                push_sync(item['type'], item['payload'])
        except Exception:
            pass
        # Continue capture if in progress
        if capture_in_progress is not None:
            capture_timer -= 1
            if capture_timer <= 0:
                # finish capture -> create tank
                tank = {
                    'tank_id': f'TANK-B-{now}',
                    'mass_co2_kg': 5000.0,
                    'pressure_psi': 2950.0,
                    'sealed': True,
                    'origin': capture_in_progress['source_id'],
                    'timestamp': datetime.utcnow().isoformat() + 'Z'
                }
                print(f'[{now:3}] Compressor: tank sealed -> {tank["tank_id"]}')
                push_sync('tank_ready', tank)
                capture_in_progress = None
        # Hauler: check for tank_ready events and start transport tasks
        try:
            item = server.sync_event_bus.get_nowait()
            if item['type'] == 'tank_ready':
                tank = item['payload']
                task = {'tank': tank, 'time_left': 2, 'vehicle': f'HV-TRUCK-{now}'}
                hauler_tasks.append(task)
                print(f'[{now:3}] Hauler: assigned {task["vehicle"]} for {tank["tank_id"]}')
            else:
                push_sync(item['type'], item['payload'])
        except Exception:
            pass
        # Progress hauler tasks
        for task in hauler_tasks[:]:
            task['time_left'] -= 1
            if task['time_left'] <= 0:
                arrival_evt = {'manifest_id': f'MAN-{task["tank"]["tank_id"]}', 'tank_id': task['tank']['tank_id'], 'assigned_vehicle': task['vehicle'], 'from': task['tank']['origin'], 'to': 'OFFSHORE_RIG_ALPHA', 'eta': None}
                print(f'[{now:3}] Hauler: delivered {arrival_evt["tank_id"]} to port')
                push_sync('delivered_to_port', arrival_evt)
                hauler_tasks.remove(task)
        # Geologist: check for delivered_to_port and inject
        try:
            item = server.sync_event_bus.get_nowait()
            if item['type'] == 'delivered_to_port':
                manifest = item['payload']
                print(f'[{now:3}] Geologist: analyzing {manifest["tank_id"]} for injection')
                # simplified safety check - pass
                push_sync('injection_report', {'well_id':'INJ-W-04','tank_id':manifest['tank_id'],'status':'injected','mass_tonnes':5.0,'timestamp': datetime.utcnow().isoformat() + 'Z'})
            else:
                push_sync(item['type'], item['payload'])
        except Exception:
            pass
        # Guardian: consume injection_report or guardian_alert
        try:
            item = server.sync_event_bus.get_nowait()
            if item['type'] == 'injection_report':
                print(f'[{now:3}] Guardian: injection report OK for {item["payload"]["tank_id"]}')
            elif item['type'] == 'guardian_alert':
                print(f'[{now:3}] Guardian: ALERT ->', item['payload'])
            else:
                push_sync(item['type'], item['payload'])
        except Exception:
            pass
        now += 1
        time.sleep(0.05)  # slow down for readability in demo
    print('Simulation complete.')

if __name__ == '__main__':
    run_sim(30)
