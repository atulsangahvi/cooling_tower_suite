"""Typed data models for the staged v2 refactor."""
from dataclasses import dataclass, field
from typing import List, Optional


@dataclass(frozen=True)
class ThermalDuty:
    hot_water_c: float
    cold_water_target_c: float
    wet_bulb_c: float
    dry_bulb_c: float
    water_mass_flow_kg_s: float
    air_mass_flow_kg_s: float
    altitude_m: float = 0.0

    @property
    def range_c(self) -> float:
        return self.hot_water_c - self.cold_water_target_c

    @property
    def approach_c(self) -> float:
        return self.cold_water_target_c - self.wet_bulb_c

    @property
    def required_heat_rejection_kw(self) -> float:
        return self.water_mass_flow_kg_s * 4.186 * self.range_c


@dataclass
class EngineeringAssessment:
    passes_thermal_target: bool
    thermal_margin_kw: float
    warnings: List[str] = field(default_factory=list)
    recommendation: Optional[str] = None
