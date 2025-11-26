// src/components/EventStream.tsx
import { RawEvent } from '../types';

interface Props {
    events: RawEvent[];
}

export function EventStream({ events }: Props) {
    return (
        <div className="card">
            <div className="card-header">
                <div className="card-title">Live Event Stream</div>
                <div className="card-tag">Events</div>
            </div>
            <ul className="log-list">
                {events.length === 0 && <li className="log-item">No events yet.</li>}
                {events.map((e, idx) => (
                    <li key={idx} className="log-item">
                        <span>[{e.type}]</span> {shortPayload(e.payload)}
                    </li>
                ))}
            </ul>
        </div>
    );
}

function shortPayload(payload: any): string {
    try {
        if (!payload) return '';
        if (payload.tank_id && payload.origin) {
            return `tank ${payload.tank_id} from ${payload.origin}`;
        }
        if (payload.tank_id && payload.status) {
            return `tank ${payload.tank_id} → ${payload.status}`;
        }
        if (payload.event_id) {
            return payload.event_id;
        }
        return JSON.stringify(payload).slice(0, 120);
    } catch {
        return '';
    }
}
