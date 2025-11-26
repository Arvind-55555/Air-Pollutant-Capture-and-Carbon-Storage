// src/types.ts

export type EventType =
    | 'pollution_event'
    | 'tank_ready'
    | 'delivered_to_port'
    | 'injection_report'
    | 'guardian_alert'
    | string;

export interface RawEvent {
    type: EventType;
    payload: any;
    timestamp?: string;
}

export interface Tank {
    tank_id: string;
    origin?: string;
    mass_co2_kg?: number;
    pressure_psi?: number;
    sealed?: boolean;
    timestamp?: string;
}

export interface InjectionReport {
    well_id?: string;
    tank_id?: string;
    status?: string;
    mass_tonnes?: number;
    timestamp?: string;
}
