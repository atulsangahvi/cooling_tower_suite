"""Run Phase 1B checks without requiring pytest."""
from __future__ import annotations

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


def main() -> None:
    checks = {
        "CT1200AT thermal positive": ct1200at_kav_over_l(1.5, 1.2) > 0,
        "CF1900 thermal positive": cf1900_kav_over_l(1.5, 1.2) > 0,
        "XF75 thermal positive": xf75_kah_over_l(1.5, 2.438, 1.219) > 0,
        "CT1200AT pressure positive": ct1200at_pressure_drop_pa(2.0, 15.0, 1.2) > 0,
        "CF1900 pressure positive": cf1900_pressure_drop_pa(2.0, 15.0, 1.2) > 0,
        "XF75 pressure positive": xf75_pressure_drop_pa(2.0, 40.0, 1.219) > 0,
    }
    open_area = BRENTWOOD_PROPERTIES["CF1900SBMA"].open_air_area_m2(9.24)
    checks["CF1900 open area"] = math.isclose(open_area or 0.0, 7.9464, abs_tol=1e-9)
    high_range = assess_high_range(200.0, 49.0, 34.0, 10.0)
    checks["High-range bypass"] = (
        math.isclose(high_range.recommended_tower_flow_m3_h, 300.0)
        and math.isclose(high_range.bypass_flow_m3_h, 100.0)
        and math.isclose(high_range.mixed_tower_inlet_c, 44.0)
    )
    warnings = warning_messages(xf75_validity(1.5, 54.7, 4.75, 1.829, 0.914))
    checks["XF75 range warning"] = len(warnings) == 1

    failed = [name for name, passed in checks.items() if not passed]
    for name, passed in checks.items():
        print(("PASS" if passed else "FAIL") + " - " + name)
    if failed:
        raise SystemExit("Phase 1B verification failed: " + ", ".join(failed))
    print("\nAll Phase 1B checks passed.")


if __name__ == "__main__":
    main()
