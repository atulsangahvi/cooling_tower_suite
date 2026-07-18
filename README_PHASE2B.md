# Cooling Tower Suite v2 — Phase 2B

Phase 2B adds transparent preliminary inlet-louver sizing and acoustic screening.

## Added
- Required net and gross louver area from airflow, selected passage velocity and louver free-area fraction.
- Louver pressure drop from `K × ρV²/2`; this replaces the previous fixed inlet-louver allowance.
- Preliminary fan and louver sound-power screening.
- Estimated free-field sound pressure at a user-selected distance.
- Optional allowance for barriers/silencers.
- UI, TXT and PDF reporting.

## Important limitation
The acoustic model is for early design screening only. Certified octave-band data from the selected fan, motor, water distribution, casing, louvers and drift eliminators is required for contractual sound guarantees.
