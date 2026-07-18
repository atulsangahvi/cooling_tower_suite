"""Preliminary cooling-tower fan and motor sizing.

This module does not replace a manufacturer fan curve. It converts the required
airflow and static pressure into shaft power, estimates motor input power and
selects the next standard IEC motor size with a service margin.
"""

from __future__ import annotations

from dataclasses import dataclass
import math


STANDARD_IEC_MOTOR_KW = (
    0.37, 0.55, 0.75, 1.1, 1.5, 2.2, 3.0, 4.0, 5.5, 7.5, 11.0, 15.0,
    18.5, 22.0, 30.0, 37.0, 45.0, 55.0, 75.0, 90.0, 110.0, 132.0,
    160.0, 200.0, 250.0, 315.0,
)


@dataclass(frozen=True)
class FanSelection:
    airflow_m3_s: float
    static_pressure_pa: float
    air_power_kw: float
    fan_shaft_power_kw: float
    motor_input_at_duty_kw: float
    selected_motor_kw: float
    specific_fan_power_w_per_m3_s: float
    fan_efficiency: float
    transmission_efficiency: float
    motor_efficiency: float
    service_factor: float
    fan_diameter_m: float | None
    fan_rpm: float | None
    tip_speed_m_s: float | None
    tip_speed_status: str
    advisory: str


def _next_standard_motor(required_kw: float) -> float:
    for rating in STANDARD_IEC_MOTOR_KW:
        if rating >= required_kw:
            return rating
    return math.ceil(required_kw / 25.0) * 25.0


def select_fan_and_motor(
    airflow_m3_s: float,
    static_pressure_pa: float,
    *,
    fan_efficiency: float = 0.78,
    transmission_efficiency: float = 1.0,
    motor_efficiency: float = 0.92,
    service_factor: float = 1.15,
    fan_diameter_m: float | None = None,
    fan_rpm: float | None = None,
) -> FanSelection:
    """Return preliminary fan duty and motor selection.

    The selected motor rating is based on shaft power divided by transmission
    efficiency, multiplied by the service factor. Motor input at duty also
    includes motor efficiency. Fan diameter and RPM are optional and used only
    for tip-speed screening.
    """
    q = max(float(airflow_m3_s), 0.0)
    dp = max(float(static_pressure_pa), 0.0)
    eta_f = min(max(float(fan_efficiency), 0.05), 1.0)
    eta_t = min(max(float(transmission_efficiency), 0.05), 1.0)
    eta_m = min(max(float(motor_efficiency), 0.05), 1.0)
    sf = max(float(service_factor), 1.0)

    air_power_kw = q * dp / 1000.0
    shaft_kw = air_power_kw / eta_f
    drive_kw = shaft_kw / eta_t
    motor_input_kw = drive_kw / eta_m
    selected_kw = _next_standard_motor(drive_kw * sf)
    sfp = (shaft_kw * 1000.0 / q) if q > 0 else 0.0

    tip_speed = None
    tip_status = "Not evaluated"
    if fan_diameter_m and fan_rpm and fan_diameter_m > 0 and fan_rpm > 0:
        tip_speed = math.pi * float(fan_diameter_m) * float(fan_rpm) / 60.0
        if tip_speed <= 55.0:
            tip_status = "Normal"
        elif tip_speed <= 65.0:
            tip_status = "Caution"
        else:
            tip_status = "High"

    advisory_parts = [
        "Preliminary duty only; final fan selection must be checked against the manufacturer's fan curve.",
        f"Select a fan delivering at least {q:.2f} m³/s at {dp:.1f} Pa static pressure.",
    ]
    if tip_speed is not None:
        advisory_parts.append(f"Calculated fan tip speed is {tip_speed:.1f} m/s ({tip_status.lower()}).")

    return FanSelection(
        airflow_m3_s=q,
        static_pressure_pa=dp,
        air_power_kw=air_power_kw,
        fan_shaft_power_kw=shaft_kw,
        motor_input_at_duty_kw=motor_input_kw,
        selected_motor_kw=selected_kw,
        specific_fan_power_w_per_m3_s=sfp,
        fan_efficiency=eta_f,
        transmission_efficiency=eta_t,
        motor_efficiency=eta_m,
        service_factor=sf,
        fan_diameter_m=float(fan_diameter_m) if fan_diameter_m else None,
        fan_rpm=float(fan_rpm) if fan_rpm else None,
        tip_speed_m_s=tip_speed,
        tip_speed_status=tip_status,
        advisory=" ".join(advisory_parts),
    )
