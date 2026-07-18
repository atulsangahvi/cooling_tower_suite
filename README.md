# Cooling Tower Design Suite v2 — Phase 1A

This repository is the safe modular foundation for the existing Streamlit cooling-tower application.

## Streamlit Cloud entry point

Set the main file to:

```text
app.py
```

`app.py` calls the validated existing application in `legacy_app.py`, so current UI, formulas, Brentwood correlations, vendor comparison, reports, password protection, and other features remain available while modules are extracted gradually.

## Why Phase 1A keeps `legacy_app.py`

A direct one-step split of a large engineering application can introduce silent calculation errors. This version first establishes the package structure without changing validated formulas. The next staged releases will move one tested calculation family at a time into the package.

## New package structure

```text
cooling_tower/
  core/models.py
  thermal/psychrometrics.py
  thermal/water_balance.py
  fills/
  reports/
  vendor/
```

The modular psychrometric and preliminary water-balance functions are included for validation. They are not yet substituted into the legacy calculation path.

## Streamlit Secrets

The existing app continues to read:

```toml
APP_PASSWORD = "your-password"
```

Google Drive settings remain the same as in the current application.

## Phase 1B planned integration

1. Extract and unit-test Brentwood CF1200, CF1900SB/MA, and XF75 correlations.
2. Extract the cooling-tower solver and graph-validity checks.
3. Add required versus available KaV/L and thermal margin assessment.
4. Wire the validated water balance into UI, TXT, PDF, and Word reports.
5. Replace the legacy entry point only after regression results match.
