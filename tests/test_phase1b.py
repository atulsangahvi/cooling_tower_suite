"""Regression and sanity checks for Phase 1B manufacturer equations."""
import math

from cooling_tower.fills.brentwood import (
    cf1900_kav_over_l,
    cf1900_pressure_drop_pa,
    ct1200at_kav_over_l,
    ct1200at_pressure_drop_pa,
    warning_messages,
    xf75_kah_over_l,
    xf75_pressure_drop_pa,
    xf75_validity,
)
from cooling_tower.fills.properties import BRENTWOOD_PROPERTIES
from cooling_tower.thermal.high_range import assess_high_range


def test_correlations_positive_and_monotonic():
    assert ct1200at_kav_over_l(1.0, 1.22) > ct1200at_kav_over_l(2.0, 1.22)
    assert cf1900_kav_over_l(1.0, 1.22) > cf1900_kav_over_l(2.0, 1.22)
    assert xf75_kah_over_l(1.0, 2.438, 1.219) > xf75_kah_over_l(2.0, 2.438, 1.219)
    assert ct1200at_pressure_drop_pa(3.0, 20.0, 1.22) > ct1200at_pressure_drop_pa(2.0, 20.0, 1.22)
    assert cf1900_pressure_drop_pa(3.0, 20.0, 1.22) > cf1900_pressure_drop_pa(2.0, 20.0, 1.22)
    assert xf75_pressure_drop_pa(3.0, 40.0, 1.219) > xf75_pressure_drop_pa(2.0, 40.0, 1.219)


def test_open_area_example():
    open_area = BRENTWOOD_PROPERTIES["CF1900SBMA"].open_air_area_m2(9.24)
    assert math.isclose(open_area, 7.9464, rel_tol=0, abs_tol=1e-9)
    assert math.isclose(18.84 / open_area, 2.370884, rel_tol=0, abs_tol=1e-5)


def test_xf75_warning_generation():
    checks = xf75_validity(1.5, 54.7, 4.75, 1.829, 0.914)
    warnings = warning_messages(checks)
    assert len(warnings) == 1
    assert "air face velocity" in warnings[0]


def test_high_range_bypass_reproduces_supplier_concept():
    result = assess_high_range(200.0, 49.0, 34.0, 10.0)
    assert math.isclose(result.recommended_tower_flow_m3_h, 300.0)
    assert math.isclose(result.bypass_flow_m3_h, 100.0)
    assert math.isclose(result.mixed_tower_inlet_c, 44.0)
    assert result.classification == "High"
