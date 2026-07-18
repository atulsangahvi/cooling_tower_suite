"""Preliminary cooling-tower inlet louver sizing and pressure-drop estimate."""
from __future__ import annotations
from dataclasses import dataclass

@dataclass(frozen=True)
class LouverSelection:
    airflow_m3_s: float
    free_area_fraction: float
    target_passage_velocity_m_s: float
    required_net_free_area_m2: float
    recommended_gross_louver_area_m2: float
    passage_velocity_m_s: float
    loss_coefficient: float
    pressure_drop_pa: float
    status: str
    advisory: str

def size_louver(airflow_m3_s: float, air_density_kg_m3: float, *, free_area_fraction: float=0.55, target_passage_velocity_m_s: float=2.5, loss_coefficient: float=2.0) -> LouverSelection:
    q=max(float(airflow_m3_s),0.0); rho=max(float(air_density_kg_m3),0.1)
    faf=min(max(float(free_area_fraction),0.10),0.95); v=max(float(target_passage_velocity_m_s),0.1); k=max(float(loss_coefficient),0.0)
    net=q/v if v>0 else 0.0
    gross=net/faf if faf>0 else 0.0
    dp=k*0.5*rho*v*v
    status='Normal' if v<=3.0 else ('Caution' if v<=4.0 else 'High')
    advisory=(f'Provide approximately {gross:.2f} m² gross louver area ({net:.2f} m² net free area) '
              f'for {q:.2f} m³/s at {v:.2f} m/s passage velocity. Estimated louver ΔP={dp:.1f} Pa using K={k:.2f}. '
              'Confirm with the selected louver manufacturer and account for screens, fouling and wind-driven rain.')
    return LouverSelection(q,faf,v,net,gross,v,k,dp,status,advisory)
