"""Emit CAD/djembe-body/parametric-goblet.csv from profile.py.

Format mirrors the SolidWorks-design-table convention used in the
instrument-maker skill: one row per goblet size, columns are the
independent inputs (head_diameter, neck_diameter, foot_diameter,
total_height, z_neck_top, z_neck_bot) plus the derived acoustic
quantities (V_0_bowl, V_total, A_neck, L_eff, f_H_lumped).
"""

from __future__ import annotations

import csv
from pathlib import Path

from profile import all_goblets


COLUMNS = [
    "size",
    "label",
    "head_diameter_in",
    "neck_diameter_in",
    "foot_diameter_in",
    "total_height_in",
    "z_neck_top_in",
    "z_neck_bot_in",
    "neck_length_in",
    "neck_area_in2",
    "l_eff_in",
    "v0_bowl_in3",
    "v_total_in3",
    "f_helmholtz_lumped_hz",
]


def main(out_path: Path) -> None:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(COLUMNS)
        for g in all_goblets():
            writer.writerow([
                g.size,
                g.label,
                f"{g.head_diameter_in:.4f}",
                f"{g.neck_diameter_in:.4f}",
                f"{g.foot_diameter_in:.4f}",
                f"{g.total_height_in:.4f}",
                f"{g.z_neck_top_in:.4f}",
                f"{g.z_neck_bot_in:.4f}",
                f"{g.neck_length_in:.4f}",
                f"{g.neck_area_in2:.4f}",
                f"{g.l_eff_in:.4f}",
                f"{g.bowl_volume_in3():.4f}",
                f"{g.total_volume_in3():.4f}",
                f"{g.closed_form_helmholtz_hz():.4f}",
            ])
    print(f"wrote {out_path}")


if __name__ == "__main__":
    here = Path(__file__).resolve().parent
    repo_root = here.parents[1]
    main(repo_root / "CAD" / "djembe-body" / "parametric-goblet.csv")
