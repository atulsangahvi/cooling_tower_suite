"""Preliminary cooling-tower water-balance calculations.

These functions are isolated for validation before they are wired into the UI
and professional report in the next phase.
"""
from dataclasses import dataclass


@dataclass(frozen=True)
class WaterBalance:
    evaporation_m3_h: float
    drift_m3_h: float
    blowdown_m3_h: float
    makeup_m3_h: float


def estimate_water_balance(
    circulation_m3_h: float,
    range_c: float,
    cycles_of_concentration: float = 4.0,
    drift_percent: float = 0.005,
    evaporation_coefficient: float = 0.00085,
) -> WaterBalance:
    if circulation_m3_h < 0:
        raise ValueError("Circulation flow cannot be negative.")
    if range_c < 0:
        raise ValueError("Cooling range cannot be negative.")
    if cycles_of_concentration <= 1.0:
        raise ValueError("Cycles of concentration must be greater than 1.0.")
    if drift_percent < 0:
        raise ValueError("Drift percentage cannot be negative.")

    evaporation = evaporation_coefficient * circulation_m3_h * range_c
    drift = circulation_m3_h * drift_percent / 100.0
    blowdown = max(evaporation / (cycles_of_concentration - 1.0) - drift, 0.0)
    makeup = evaporation + drift + blowdown
    return WaterBalance(evaporation, drift, blowdown, makeup)
