// src/App.tsx
import { useDashboardData } from './hooks/useDashboardData';
import { EventStream } from './components/EventStream';
import { TankTable } from './components/TankTable';
import { InjectionStatus } from './components/InjectionStatus';
import { AgentLogs } from './components/AgentLogs';

function App() {
  const {
    isOnline,
    latestEvents,
    tanks,
    injectionReports,
    guardianAlerts,
  } = useDashboardData();

  return (
    <div className="app-root">
      <header className="dashboard-header">
        <div>
          <div className="dashboard-title">
            Pollutant Absorber + Carbon Capture Dashboard
          </div>
          <div className="dashboard-subtitle">
            Live view of agents, tanks, and injection wells
          </div>
        </div>
        <div className="badge-status">
          <span className="badge-dot" />
          {isOnline ? 'Backend connected' : 'Backend offline'}
        </div>
      </header>

      <main className="grid">
        <EventStream events={latestEvents} />
        <TankTable tanks={tanks} />
        <InjectionStatus reports={injectionReports} />
        <AgentLogs events={latestEvents} alerts={guardianAlerts} />
      </main>
    </div>
  );
}

export default App;
