# Cooling Tower Design Suite v2 — Phase 1B

This package continues the staged refactor without changing the working Streamlit calculation paths.

## Streamlit deployment

Use `app.py` as the Streamlit Cloud main file. It launches `legacy_app.py`, which remains the stable production application during migration.

Set this secret in Streamlit Cloud:

```toml
APP_PASSWORD = "your-password"
```

## Added in Phase 1B

- Isolated Brentwood thermal and pressure-drop correlations:
  - CT1200AT counterflow dataset
  - CF1900SB/MA counterflow
  - XF75 crossflow
- Explicit graph-validity checking objects and warning generation.
- Fill property records with source-quality notes for assumed free-area fractions.
- Correct open-air-area helper in the new fill model.
- High-range detection and bypass/mixing calculation module.
- Regression tests and a standalone verification script.
- Removed compiled `__pycache__` and `.pyc` files from the package.

## Verification

Run locally or in GitHub Actions:

```bash
python verify_phase1b.py
```

Optional pytest run:

```bash
pytest -q
```

## Migration safety

The new modules are not yet wired into `legacy_app.py`. This is intentional. Phase 1B first freezes equations in independently testable modules. Phase 1C will connect them to the production solver one fill at a time and compare old/new outputs before retiring duplicated code.
