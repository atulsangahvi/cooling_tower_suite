"""High cooling-range detection and bypass/mixing recommendations."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class HighRangeAssessment:
    process_range_c: float
    classification: str
    target_tower_range_c: float
    process_flow_m3_h: float
    recommended_tower_flow_m3_h: float
    bypass_flow_m3_h: float
    mixed_tower_inlet_c: float
    advisory: str


def classify_range(range_c: float) -> str:
    if range_c < 5.0:
        return "Low"
    if range_c <= 10.0:
        return "Normal"
    if range_c <= 12.0:
        return "Caution"
    if range_c <= 15.0:
        return "High"
    return "Very High"


def assess_high_range(
    process_flow_m3_h: float,
    hot_process_return_c: float,
    cold_supply_c: float,
    target_tower_range_c: float = 10.0,
) -> HighRangeAssessment:
    if process_flow_m3_h <= 0:
        raise ValueError("Process flow must be greater than zero")
    process_range = hot_process_return_c - cold_supply_c
    if process_range <= 0:
        raise ValueError("Hot process return must exceed cold supply temperature")
    if target_tower_range_c <= 0:
        raise ValueError("Target tower range must be greater than zero")

    tower_flow = process_flow_m3_h * process_range / target_tower_range_c
    tower_flow = max(tower_flow, process_flow_m3_h)
    bypass_flow = tower_flow - process_flow_m3_h
    mixed_inlet = (
        process_flow_m3_h * hot_process_return_c + bypass_flow * cold_supply_c
    ) / tower_flow
    classification = classify_range(process_range)
    advisory = (
        "No bypass is normally required based on range alone. Confirm fill wetting, approach, and graph limits."
        if classification in {"Low", "Normal"}
        else "Consider increased tower circulation with a cold-water bypass/mixing line; confirm pump, piping, distribution, and fill loading."
    )
    return HighRangeAssessment(
        process_range_c=process_range,
        classification=classification,
        target_tower_range_c=target_tower_range_c,
        process_flow_m3_h=process_flow_m3_h,
        recommended_tower_flow_m3_h=tower_flow,
        bypass_flow_m3_h=bypass_flow,
        mixed_tower_inlet_c=mixed_inlet,
        advisory=advisory,
    )
