// src/components/TankTable.tsx
import { Tank } from '../types';

interface Props {
    tanks: Tank[];
}

export function TankTable({ tanks }: Props) {
    const latestTanks = tanks.slice(0, 8);

    return (
        <div className="card">
            <div className="card-header">
                <div className="card-title">Tank Movements</div>
                <span className="card-tag">Tanks</span>
            </div>
            <table className="table">
                <thead>
                    <tr>
                        <th>Tank ID</th>
                        <th>Origin</th>
                        <th>Mass (kg)</th>
                        <th>Pressure (psi)</th>
                        <th>Sealed</th>
                    </tr>
                </thead>
                <tbody>
                    {latestTanks.length === 0 && (
                        <tr>
                            <td colSpan={5}>No tanks yet.</td>
                        </tr>
                    )}
                    {latestTanks.map((t) => (
                        <tr key={t.tank_id}>
                            <td>{t.tank_id}</td>
                            <td>{t.origin ?? '-'}</td>
                            <td>{t.mass_co2_kg ?? '-'}</td>
                            <td>{t.pressure_psi ?? '-'}</td>
                            <td>
                                <span className={`chip ${t.sealed ? 'chip--success' : 'chip--warning'}`}>
                                    {t.sealed ? 'Sealed' : 'Open'}
                                </span>
                            </td>
                        </tr>
                    ))}
                </tbody>
            </table>
        </div>
    );
}
