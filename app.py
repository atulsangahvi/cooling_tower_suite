"""Streamlit entry point for Cooling Tower Design Suite v2.

Phase 1A preserves the validated single-file application while introducing a
package structure for staged extraction of thermal, fill, report, and vendor
modules. Streamlit Cloud should run this file.
"""
from legacy_app import main

if __name__ == "__main__":
    main()
