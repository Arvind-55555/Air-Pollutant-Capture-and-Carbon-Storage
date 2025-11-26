// src/hooks/useDashboardData.ts
import { useEffect, useState, useMemo } from 'react';
import type { RawEvent, Tank, InjectionReport } from '../types';

interface DrainResponse {
    drained: number;
    events: RawEvent[];
}

export function useDashboardData(pollIntervalMs = 3000) {
    const [events, setEvents] = useState<RawEvent[]>([]);
    const [isOnline, setIsOnline] = useState<boolean>(false);

    useEffect(() => {
        let isMounted = true;

        const fetchEvents = async () => {
            try {
                const res = await fetch('/api/debug/drain_events?limit=50');
                if (!res.ok) throw new Error(`HTTP ${res.status}`);
                const data: DrainResponse = await res.json();
                if (!isMounted) return;

                const newEvents = data.events || [];
                if (newEvents.length > 0) {
                    setEvents((prev) => {
                        const merged = [...newEvents.reverse(), ...prev];
                        // keep only latest 200 events
                        return merged.slice(0, 200);
                    });
                }
                setIsOnline(true);
            } catch (err) {
                console.error('Failed to fetch events:', err);
                if (isMounted) setIsOnline(false);
            }
        };

        // initial fetch
        fetchEvents();
        const id = setInterval(fetchEvents, pollIntervalMs);

        return () => {
            isMounted = false;
            clearInterval(id);
        };
    }, [pollIntervalMs]);

    const tanks: Tank[] = useMemo(
        () =>
            events
                .filter((e) => e.type === 'tank_ready')
                .map((e) => ({
                    tank_id: e.payload.tank_id,
                    origin: e.payload.origin,
                    mass_co2_kg: e.payload.mass_co2_kg,
                    pressure_psi: e.payload.pressure_psi,
                    sealed: e.payload.sealed,
                    timestamp: e.timestamp || e.payload.timestamp,
                })),
        [events],
    );

    const injectionReports: InjectionReport[] = useMemo(
        () =>
            events
                .filter((e) => e.type === 'injection_report')
                .map((e) => ({
                    well_id: e.payload.well_id,
                    tank_id: e.payload.tank_id,
                    status: e.payload.status,
                    mass_tonnes: e.payload.mass_tonnes,
                    timestamp: e.timestamp || e.payload.timestamp,
                })),
        [events],
    );

    const guardianAlerts = useMemo(
        () => events.filter((e) => e.type === 'guardian_alert'),
        [events],
    );

    const latestEvents = useMemo(() => events.slice(0, 20), [events]);

    return {
        isOnline,
        events,
        latestEvents,
        tanks,
        injectionReports,
        guardianAlerts,
    };
}
