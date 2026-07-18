# Cooling Tower Suite v2 Migration Plan

## Completed

### Phase 1A — Safe project structure
- Stable `legacy_app.py` retained.
- Streamlit launcher added.
- Core models, psychrometrics, and initial water balance extracted.

### Phase 1B — Manufacturer correlation freeze and regression checks
- CT1200AT, CF1900SB/MA, and XF75 correlations isolated.
- Graph envelopes represented as executable checks.
- Fill properties and free-area source notes isolated.
- High-range/bypass assistant isolated.
- Automated verification added.

## Next: Phase 1C — Controlled production integration

1. Wire CF1900 thermal and pressure-drop calls to the modular functions.
2. Compare modular results against the existing app over a test matrix.
3. Wire CT1200AT after CF1900 passes.
4. Wire XF75 crossflow after dual-bank geometry tests pass.
5. Add report-level engineering assessment and graph-validity summary.
6. Remove duplicated functions only after exact regression acceptance.

## Later phases

- Phase 2: full water balance and cycles of concentration.
- Phase 3: fan sizing, motor selection, louvers, and pressure-loss breakdown.
- Phase 4: sound prediction and attenuation.
- Phase 5: mechanical sizing and cost/life-cycle optimization.

## Phase 2A completed

- Corrected solver/report propagation of net open area and open-area velocity.
- Added preliminary fan duty, standard motor sizing and optional tip-speed screening.
- Added fan/motor results to the Streamlit UI and downloadable reports.

## Next planned phase — Phase 2B

- Louver sizing and explicit louver pressure-drop calculation.
- Drift-eliminator pressure-drop inputs/database.
- Fan operating-point and multiple-cell airflow allocation.
- Preliminary sound model using fan tip speed, motor/fan source levels and distance attenuation.
