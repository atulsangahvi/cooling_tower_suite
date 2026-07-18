# Migration plan

## Phase 1A — completed
- Preserve the currently working Streamlit application.
- Add a stable `app.py` entry point.
- Establish package namespaces and typed core models.
- Add isolated psychrometric and water-balance modules.

## Phase 1B
- Extract fill data and manufacturer correlations.
- Add regression checks against known CF1900 and XF75 cases.
- Add graph-envelope status objects used by UI and reports.

## Phase 1C
- Extract the main thermal solver.
- Calculate required KaV/L, available KaV/L, thermal margin, and utilization.
- Add high-range/bypass assessment as a reusable engineering module.

## Phase 1D
- Extract report builders.
- Add an engineering assessment and recommendation section.
