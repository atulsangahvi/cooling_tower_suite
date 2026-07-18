"""Validated Brentwood fill correlations used by Cooling Tower Suite v2.

This module isolates manufacturer-specific equations from the Streamlit UI.
It does not change the production calculation path yet; Phase 1B provides a
single source of truth and regression tests before wiring these functions into
``legacy_app.py``.

Important: equations are only valid inside their published graph envelopes.
Call the corresponding ``*_validity`` function and show its warnings whenever
results are reported.
"""
from __future__ import annotations

from dataclasses import dataclass
from math import isfinite
from typing import Iterable


IN_WG_TO_PA = 249.0889
MPS_TO_FPM = 196.850394
M3H_M2_TO_GPM_FT2 = 4.402867 / 10.763910416709722
M_TO_FT = 1.0 / 0.3048


@dataclass(frozen=True)
class RangeCheck:
    parameter: str
    value: float
    minimum: float
    maximum: float
    unit: str = ""

    @property
    def ok(self) -> bool:
        return isfinite(self.value) and self.minimum <= self.value <= self.maximum

    @property
    def message(self) -> str:
        status = "OK" if self.ok else "OUTSIDE"
        suffix = f" {self.unit}" if self.unit else ""
        return (
            f"{status}: {self.parameter} = {self.value:.4g}{suffix}; "
            f"published range {self.minimum:g}–{self.maximum:g}{suffix}"
        )


def _validate_positive(**values: float) -> None:
    bad = [name for name, value in values.items() if not isfinite(float(value)) or float(value) <= 0]
    if bad:
        raise ValueError("Values must be finite and greater than zero: " + ", ".join(bad))


def ct1200at_kav_over_l(l_over_g: float, fill_height_m: float) -> float:
    """CT1200AT published counterflow thermal correlation.

    KaV/L = 0.967 × (L/G)^(-0.779) × H_ft^(0.632)
    """
    _validate_positive(l_over_g=l_over_g, fill_height_m=fill_height_m)
    height_ft = fill_height_m * M_TO_FT
    return 0.967 * l_over_g ** -0.779 * height_ft ** 0.632


def ct1200at_pressure_drop_pa(
    air_velocity_m_s: float,
    water_loading_m3_h_m2: float,
    fill_height_m: float,
) -> float:
    """CT1200AT published fill pressure-drop correlation converted to SI."""
    _validate_positive(
        air_velocity_m_s=air_velocity_m_s,
        water_loading_m3_h_m2=water_loading_m3_h_m2,
        fill_height_m=fill_height_m,
    )
    vel = air_velocity_m_s * MPS_TO_FPM
    qa = water_loading_m3_h_m2 * M3H_M2_TO_GPM_FT2
    height_ft = fill_height_m * M_TO_FT
    dp_in_wg = (
        4.6192e-6 * vel ** 1.7443
        + qa * 4.9355e-9 * vel ** 2.3711
    ) * (0.1513 + 0.2852 * height_ft)
    return dp_in_wg * IN_WG_TO_PA


def ct1200at_validity(
    l_over_g: float,
    water_loading_m3_h_m2: float,
    air_velocity_m_s: float,
    fill_height_m: float,
) -> list[RangeCheck]:
    return [
        RangeCheck("L/G", l_over_g, 0.5, 2.5),
        RangeCheck("water loading", water_loading_m3_h_m2, 0.0, 30.0, "m³/h·m²"),
        RangeCheck("air face velocity", air_velocity_m_s, 1.0, 4.0, "m/s"),
        RangeCheck("fill height", fill_height_m, 0.610, 1.220, "m"),
    ]


def cf1900_kav_over_l(l_over_g: float, fill_height_m: float) -> float:
    """CF1900SB/MA published counterflow thermal correlation.

    KaV/L = 0.696 × (L/G)^(-0.707) × H_ft^(0.714)
    """
    _validate_positive(l_over_g=l_over_g, fill_height_m=fill_height_m)
    height_ft = fill_height_m * M_TO_FT
    return 0.696 * l_over_g ** -0.707 * height_ft ** 0.714


def cf1900_pressure_drop_pa(
    air_velocity_m_s: float,
    water_loading_m3_h_m2: float,
    fill_height_m: float,
) -> float:
    """CF1900SB/MA published fill pressure-drop correlation converted to SI."""
    _validate_positive(
        air_velocity_m_s=air_velocity_m_s,
        water_loading_m3_h_m2=water_loading_m3_h_m2,
        fill_height_m=fill_height_m,
    )
    vel = air_velocity_m_s * MPS_TO_FPM
    qa = water_loading_m3_h_m2 * M3H_M2_TO_GPM_FT2
    height_ft = fill_height_m * M_TO_FT
    dp_in_wg = (
        2.2470e-6 * vel ** 1.7897
        + qa * 4.8967e-8 * vel ** 1.9362
    ) * (0.1984 + 0.3281 * height_ft)
    return dp_in_wg * IN_WG_TO_PA


def cf1900_validity(
    l_over_g: float,
    water_loading_m3_h_m2: float,
    air_velocity_m_s: float,
    fill_height_m: float,
) -> list[RangeCheck]:
    _validate_positive(l_over_g=l_over_g)
    g_over_l = 1.0 / l_over_g
    return [
        RangeCheck("G/L", g_over_l, 0.5, 3.0),
        RangeCheck("water loading", water_loading_m3_h_m2, 10.0, 25.0, "m³/h·m²"),
        RangeCheck("air face velocity", air_velocity_m_s, 1.5, 3.5, "m/s"),
        RangeCheck("fill height", fill_height_m, 0.610, 1.830, "m"),
    ]


def xf75_kah_over_l(l_over_g: float, fill_height_m: float, air_travel_depth_m: float) -> float:
    """XF75 crossflow SI thermal curve-family correlation.

    KaH/L = 1.706 × (G/L)^0.822 × H^0.178 × AT^0.822
    """
    _validate_positive(
        l_over_g=l_over_g,
        fill_height_m=fill_height_m,
        air_travel_depth_m=air_travel_depth_m,
    )
    g_over_l = 1.0 / l_over_g
    return 1.706 * g_over_l ** 0.822 * fill_height_m ** 0.178 * air_travel_depth_m ** 0.822


def xf75_pressure_drop_pa(
    air_velocity_m_s: float,
    water_loading_m3_h_m2: float,
    air_travel_depth_m: float,
) -> float:
    """XF75 published SI fill pressure-drop correlation."""
    _validate_positive(
        air_velocity_m_s=air_velocity_m_s,
        water_loading_m3_h_m2=water_loading_m3_h_m2,
        air_travel_depth_m=air_travel_depth_m,
    )
    velocity = air_velocity_m_s
    loading = water_loading_m3_h_m2
    return (
        12.879 * velocity ** 1.7532
        + loading * 6.2001e-3 * velocity ** 2
        + 0.32229 * velocity
    ) * air_travel_depth_m


def xf75_validity(
    l_over_g: float,
    water_loading_m3_h_m2: float,
    air_velocity_m_s: float,
    fill_height_m: float,
    air_travel_depth_m: float,
) -> list[RangeCheck]:
    return [
        RangeCheck("L/G", l_over_g, 0.10, 3.00),
        RangeCheck("water loading", water_loading_m3_h_m2, 20.0, 70.0, "m³/h·m²"),
        RangeCheck("air face velocity", air_velocity_m_s, 1.0, 4.0, "m/s"),
        RangeCheck("fill height H", fill_height_m, 1.829, 4.877, "m"),
        RangeCheck("air travel depth AT", air_travel_depth_m, 0.610, 1.829, "m"),
    ]


def warning_messages(checks: Iterable[RangeCheck]) -> list[str]:
    return [check.message for check in checks if not check.ok]
