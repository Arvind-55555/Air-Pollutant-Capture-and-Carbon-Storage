// src/components/AgentLogs.tsx
import { RawEvent } from '../types';

interface Props {
    events: RawEvent[];
    alerts: RawEvent[];
}

export function AgentLogs({ events, alerts }: Props) {
    const logs = events.slice(0, 15);

    return (
        <div className="card">
            <div className="card-header">
                <div className="card-title">Agent Logs</div>
                <span className="card-tag">Agents</span>
            </div>

            {alerts.length > 0 && (
                <div style={{ marginBottom: '0.5rem' }}>
                    {alerts.slice(0, 3).map((a, idx) => (
                        <div key={idx} className="chip chip--warning" style={{ marginRight: '0.25rem' }}>
                            ALERT: {a.payload?.reason ?? 'guardian_alert'}
                        </div>
                    ))}
                </div>
            )}

            <ul className="log-list">
                {logs.length === 0 && <li className="log-item">Waiting for agent activity…</li>}
                {logs.map((e, idx) => (
                    <li key={idx} className="log-item">
                        <span className="pill">{agentFromEventType(e.type)}</span>{' '}
                        {renderAgentMessage(e)}
                    </li>
                ))}
            </ul>
        </div>
    );
}

function agentFromEventType(type: string): string {
    switch (type) {
        case 'pollution_event':
            return 'Sentinel';
        case 'tank_ready':
            return 'Compressor';
        case 'delivered_to_port':
            return 'Hauler';
        case 'injection_report':
            return 'Geologist';
        case 'guardian_alert':
            return 'Guardian';
        default:
            return 'System';
    }
}

function renderAgentMessage(e: RawEvent): string {
    const p = e.payload || {};
    switch (e.type) {
        case 'pollution_event':
            return `Detected pollution at ${p.source_id ?? 'unknown source'}`;
        case 'tank_ready':
            return `Sealed tank ${p.tank_id} from ${p.origin}`;
        case 'delivered_to_port':
            return `Delivered tank ${p.tank_id} to ${p.to ?? 'port'}`;
        case 'injection_report':
            return `Injected tank ${p.tank_id} into well ${p.well_id}`;
        case 'guardian_alert':
            return `Alert: ${p.reason ?? 'unknown'}`;
        default:
            return JSON.stringify(p).slice(0, 120);
    }
}
