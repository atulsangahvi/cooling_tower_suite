# Cooling Tower Suite v2 — Phase 1C

Phase 1C fixes the Streamlit runtime error in the pressure-drop result dictionary and integrates the first modular engineering assistants into the working application.

## Main file for Streamlit Cloud

Use `app.py`.

## Added in Phase 1C

- Fixed `NameError: applied_tower_factor is not defined`.
- Published Brentwood pressure-drop equations now use a factor of 1.0 because their correlations already include the applicable fill geometry.
- Legacy/default pressure-drop curves retain the tower factor and fill-depth scaling.
- Preliminary water balance shown in the UI and TXT/PDF reports:
  - evaporation
  - drift
  - blowdown
  - makeup water
- Cooling-range classification shown in the UI and reports.
- High-range advisory calculates suggested tower circulation, bypass flow and mixed tower inlet temperature.
- Existing legacy application remains available through `legacy_app.py` while modular migration continues.

## Important engineering note

The water balance is preliminary and defaults to 4 cycles of concentration and 0.005% drift. Final values must be confirmed using water-treatment limits and the selected eliminator's guaranteed drift rate.
