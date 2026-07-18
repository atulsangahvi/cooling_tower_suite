"""Preliminary A-weighted cooling-tower sound screening.

This is an engineering screening model, not certified acoustic data. Final sound
levels require octave-band fan, motor, water-fall and casing data from suppliers.
"""
from __future__ import annotations
from dataclasses import dataclass
import math

@dataclass(frozen=True)
class SoundEstimate:
    fan_lwa_db: float
    louver_lwa_db: float
    combined_lwa_db: float
    distance_m: float
    estimated_lpa_db: float
    attenuation_db: float
    status: str
    advisory: str

def _combine(levels):
    return 10.0*math.log10(sum(10.0**(l/10.0) for l in levels)) if levels else 0.0

def estimate_cooling_tower_sound(fan_shaft_power_kw: float, airflow_m3_s: float, louver_passage_velocity_m_s: float, *, distance_m: float=10.0, additional_attenuation_db: float=0.0, tip_speed_m_s: float|None=None) -> SoundEstimate:
    p=max(float(fan_shaft_power_kw),0.01); q=max(float(airflow_m3_s),0.01); v=max(float(louver_passage_velocity_m_s),0.1)
    r=max(float(distance_m),1.0); att=max(float(additional_attenuation_db),0.0)
    # Broad empirical screening relationships, intentionally conservative.
    fan_lwa=88.0 + 10.0*math.log10(p)
    if tip_speed_m_s is not None and tip_speed_m_s>55.0:
        fan_lwa += min((tip_speed_m_s-55.0)*0.25, 6.0)
    louver_lwa=68.0 + 10.0*math.log10(q) + 20.0*math.log10(max(v/2.5,0.2))
    combined=_combine([fan_lwa,louver_lwa])
    # Hemispherical propagation: Lp ≈ Lw - 20log(r) - 8; subtract user attenuation.
    lpa=combined - 20.0*math.log10(r) - 8.0 - att
    status='Low/Moderate' if lpa<70 else ('Caution' if lpa<80 else 'High')
    advisory=('Preliminary A-weighted screening only. Obtain certified octave-band sound power data for fan, motor, '
              'water fall/splash, louvers and casing; then assess receiver locations, reflections, barriers and tonal penalties.')
    return SoundEstimate(fan_lwa,louver_lwa,combined,r,lpa,att,status,advisory)
