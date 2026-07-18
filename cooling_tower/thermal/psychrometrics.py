"""Psychrometric helper functions extracted for v2 modularization."""
import math


def saturation_pressure_kpa(temp_c: float) -> float:
    if temp_c >= 0:
        return 0.61121 * math.exp((18.678 - temp_c / 234.5) * (temp_c / (257.14 + temp_c)))
    return 0.61115 * math.exp((23.036 - temp_c / 333.7) * (temp_c / (279.82 + temp_c)))


def atmospheric_pressure_kpa(altitude_m: float) -> float:
    return 101.325 * (1 - 0.0000225577 * altitude_m) ** 5.25588


def humidity_ratio_from_db_wb(db_c: float, wb_c: float, pressure_kpa: float = 101.325) -> float:
    pws_wb = saturation_pressure_kpa(wb_c)
    ws_wb = 0.62198 * pws_wb / (pressure_kpa - pws_wb)
    h_fg = 2501.0
    cp_air = 1.006
    cp_vapor = 1.86
    value = ((h_fg - cp_vapor * wb_c) * ws_wb - cp_air * (db_c - wb_c)) / (
        h_fg + cp_vapor * db_c - 4.186 * wb_c
    )
    return max(value, 0.0001)


def relative_humidity_percent(db_c: float, wb_c: float, pressure_kpa: float = 101.325) -> float:
    humidity_ratio = humidity_ratio_from_db_wb(db_c, wb_c, pressure_kpa)
    pws_db = saturation_pressure_kpa(db_c)
    ws_db = 0.62198 * pws_db / (pressure_kpa - pws_db)
    return 100.0 * humidity_ratio / ws_db


def moist_air_density_kg_m3(db_c: float, wb_c: float, altitude_m: float = 0.0) -> float:
    pressure_kpa = atmospheric_pressure_kpa(altitude_m)
    humidity_ratio = humidity_ratio_from_db_wb(db_c, wb_c, pressure_kpa)
    temperature_k = db_c + 273.15
    return pressure_kpa / (0.28705 * temperature_k * (1 + 1.609 * humidity_ratio))
