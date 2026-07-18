# Cooling Tower Suite v2 — Phase 2A

Phase 2A retains the Phase 1C thermal, fill, water-balance and high-range logic and adds a preliminary fan/motor design module.

## Report corrections

- Net open air area is now returned by the solver and printed correctly.
- Air velocity through the assumed open fill area is calculated separately from manufacturer graph face velocity.
- Required, achievable and margin heat-rejection values are shown explicitly.
- Achievable capacity is identified as available capacity; normal controls prevent unnecessary overcooling.
- Counterflow rectangular length/width and round diameter metadata are retained in reports.
- Free-area fraction remains clearly labelled as an engineering estimate unless manufacturer data is supplied.

## Preliminary fan and motor module

- Air power from airflow × static pressure.
- Fan shaft power from selected fan efficiency.
- Motor electrical input estimate.
- Next standard IEC motor rating with service factor.
- Specific fan power.
- Optional fan diameter/RPM tip-speed screening.
- UI and PDF/TXT report sections.

Final fan selection must always be checked against a manufacturer fan curve, blade pitch, operating point, motor data, vibration limits and sound requirements.

## Streamlit deployment

Use `app.py` as the Streamlit Cloud main file.
