"""Manufacturer fill property records with explicit source quality metadata."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class FillProperties:
    key: str
    display_name: str
    surface_area_m2_m3: float
    sheet_spacing_mm: float
    flute_angle_deg: float
    free_area_fraction: float | None
    free_area_source: str

    def open_air_area_m2(self, gross_face_area_m2: float) -> float | None:
        if self.free_area_fraction is None:
            return None
        if gross_face_area_m2 < 0:
            raise ValueError("Gross face area cannot be negative")
        return gross_face_area_m2 * self.free_area_fraction


BRENTWOOD_PROPERTIES = {
    "CF1200": FillProperties(
        key="CF1200",
        display_name="Brentwood ACCU-PAK CF1200",
        surface_area_m2_m3=226.0,
        sheet_spacing_mm=11.7,
        flute_angle_deg=30.0,
        free_area_fraction=0.89,
        free_area_source="Engineering estimate; not directly stated in the available Brentwood brochure",
    ),
    "CT1200AT": FillProperties(
        key="CT1200AT",
        display_name="Brentwood CT1200AT performance-sheet dataset",
        surface_area_m2_m3=226.0,
        sheet_spacing_mm=11.7,
        flute_angle_deg=30.0,
        free_area_fraction=0.89,
        free_area_source="Engineering estimate; not directly stated in the available Brentwood brochure",
    ),
    "CF1900SBMA": FillProperties(
        key="CF1900SBMA",
        display_name="Brentwood CF1900SB/MA",
        surface_area_m2_m3=157.5,
        sheet_spacing_mm=19.0,
        flute_angle_deg=31.0,
        free_area_fraction=0.86,
        free_area_source="Engineering estimate; not directly stated in the available Brentwood brochure",
    ),
    "XF75": FillProperties(
        key="XF75",
        display_name="Brentwood XF75",
        surface_area_m2_m3=167.4,
        sheet_spacing_mm=19.0,
        flute_angle_deg=30.0,
        free_area_fraction=0.91,
        free_area_source="Engineering estimate; not directly stated in the available Brentwood brochure",
    ),
}
