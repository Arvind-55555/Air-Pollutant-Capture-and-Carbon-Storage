// src/components/InjectionStatus.tsx
import { InjectionReport } from '../types';

interface Props {
    reports: InjectionReport[];
}

export function InjectionStatus({ reports }: Props) {
    const latest = reports.slice(0, 6);

    return (
        <div className="card">
            <div className="card-header">
                <div className="card-title">Injection Wells</div>
                <span className="card-tag">Seabed</span>
            </div>
            <table className="table">
                <thead>
                    <tr>
                        <th>Well</th>
                        <th>Tank</th>
                        <th>Status</th>
                        <th>Mass (t)</th>
                    </tr>
                </thead>
                <tbody>
                    {latest.length === 0 && (
                        <tr>
                            <td colSpan={4}>No injections yet.</td>
                        </tr>
                    )}
                    {latest.map((r, idx) => (
                        <tr key={`${r.tank_id}-${idx}`}>
                            <td>{r.well_id ?? '-'}</td>
                            <td>{r.tank_id ?? '-'}</td>
                            <td>
                                <span className="chip chip--info">{r.status ?? 'unknown'}</span>
                            </td>
                            <td>{r.mass_tonnes ?? '-'}</td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
