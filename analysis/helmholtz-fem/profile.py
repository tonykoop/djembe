"""Parametric goblet-body profile for the djembe Helmholtz FEM study.

The goblet is parameterized as a piecewise-linear axial profile r(z) with
four control points:

    z = 0          → drumhead radius (bowl top)         [rigid wall in FEM]
    z = z_neck_top → bowl-to-neck transition radius
    z = z_neck_bot → neck-to-foot transition radius
    z = H          → foot opening radius                 [open in FEM]

For each Morgan Drums size (S/M/L) we publish the control points, the
disk-method bowl-cavity volume V_0_bowl (the volume above the neck —
this is what the lumped Helmholtz model sees), the neck cross-section
area A_neck (the lumped-model port area), and the L_eff with flanged-end
corrections at both neck ends.

This module is the single source of truth for goblet geometry. Both the
parametric-goblet.csv design table and the FEM solver pull from it.

Pure numpy. No SciPy / FEniCS / gmsh dependency.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


SPEED_OF_SOUND_IN_PER_S = 13500.0  # in/s, at ~20 °C, dry air


@dataclass(frozen=True)
class GobletSpec:
    """Parametric goblet profile in inches."""

    size: str                # "S" / "M" / "L"
    label: str               # e.g. "Morgan-9"
    head_diameter_in: float
    neck_diameter_in: float
    foot_diameter_in: float
    total_height_in: float
    z_neck_top_in: float     # axial position of bowl→neck transition
    z_neck_bot_in: float     # axial position of neck→foot transition

    @property
    def head_radius_in(self) -> float:
        return self.head_diameter_in / 2.0

    @property
    def neck_radius_in(self) -> float:
        return self.neck_diameter_in / 2.0

    @property
    def foot_radius_in(self) -> float:
        return self.foot_diameter_in / 2.0

    @property
    def neck_length_in(self) -> float:
        return self.z_neck_bot_in - self.z_neck_top_in

    @property
    def neck_area_in2(self) -> float:
        return math.pi * self.neck_radius_in ** 2

    @property
    def l_eff_in(self) -> float:
        """Neck length + 0.85 * r_neck at each (flanged) end."""
        return self.neck_length_in + 2.0 * 0.85 * self.neck_radius_in

    def radius_at(self, z_in: float) -> float:
        """Piecewise-linear r(z) in inches."""
        if z_in <= 0.0:
            return self.head_radius_in
        if z_in >= self.total_height_in:
            return self.foot_radius_in
        if z_in <= self.z_neck_top_in:
            t = z_in / self.z_neck_top_in
            return (1.0 - t) * self.head_radius_in + t * self.neck_radius_in
        if z_in <= self.z_neck_bot_in:
            return self.neck_radius_in
        t = (z_in - self.z_neck_bot_in) / (self.total_height_in - self.z_neck_bot_in)
        return (1.0 - t) * self.neck_radius_in + t * self.foot_radius_in

    def area_at(self, z_in: float) -> float:
        return math.pi * self.radius_at(z_in) ** 2

    def sample(self, n_nodes: int) -> tuple[np.ndarray, np.ndarray]:
        """Return (z, A(z)) sampled uniformly on [0, H]."""
        z = np.linspace(0.0, self.total_height_in, n_nodes)
        A = np.array([self.area_at(zi) for zi in z])
        return z, A

    def bowl_volume_in3(self, n_quad: int = 4001) -> float:
        """Disk-method volume from drumhead (z=0) down to neck top.

        This is V_0 in the lumped Helmholtz formula — the bowl cavity
        above the neck.
        """
        z = np.linspace(0.0, self.z_neck_top_in, n_quad)
        r = np.array([self.radius_at(zi) for zi in z])
        # trapezoidal integration of pi r^2 dz
        return float(np.trapezoid(math.pi * r * r, z))

    def total_volume_in3(self, n_quad: int = 4001) -> float:
        """Disk-method volume of the entire goblet interior."""
        z = np.linspace(0.0, self.total_height_in, n_quad)
        r = np.array([self.radius_at(zi) for zi in z])
        return float(np.trapezoid(math.pi * r * r, z))

    def closed_form_helmholtz_hz(self, c_in_per_s: float = SPEED_OF_SOUND_IN_PER_S) -> float:
        """Lumped Helmholtz f_H using V_0 = bowl cavity above the neck."""
        v0 = self.bowl_volume_in3()
        a = self.neck_area_in2
        l_eff = self.l_eff_in
        return c_in_per_s / (2.0 * math.pi) * math.sqrt(a / (v0 * l_eff))


# Parameters chosen so the disk-method bowl volume matches the documented
# undergrad-study V_0 values (162 / 226 / 700 in^3) within a couple
# percent. The neck/foot/height values are taken from the README and
# skills/helmholtz-cavity-resonator.md narrative; the z_neck_top and
# z_neck_bot values were tuned to land the bowl volume on target.
# Profile geometry tuned so the disk-method bowl volume above the neck
# (V_0_bowl) matches the documented undergrad-study lumped-Helmholtz V_0
# values (162 / 226 / 700 in^3) within ~2%. The bowl section is short
# (~20% of total height for S/M, ~40% for L) and the foot section is
# long, matching the goblet silhouette in `images/segmented-djembe.png`
# and the stack-design `drawings/img20260426_00575906.png`.
GOBLETS: dict[str, GobletSpec] = {
    "S": GobletSpec(
        size="S",
        label="Morgan-9 (small)",
        head_diameter_in=9.0,
        neck_diameter_in=5.0,
        foot_diameter_in=8.0,
        total_height_in=18.0,
        z_neck_top_in=4.10,
        z_neck_bot_in=6.10,
    ),
    "M": GobletSpec(
        size="M",
        label="Morgan-10 (medium)",
        head_diameter_in=10.0,
        neck_diameter_in=5.5,
        foot_diameter_in=8.5,
        total_height_in=20.0,
        z_neck_top_in=4.66,
        z_neck_bot_in=6.66,
    ),
    "L": GobletSpec(
        size="L",
        label="Morgan-12 (large)",
        head_diameter_in=12.0,
        neck_diameter_in=6.5,
        foot_diameter_in=10.0,
        total_height_in=24.0,
        z_neck_top_in=10.12,
        z_neck_bot_in=12.62,
    ),
}


def all_goblets() -> list[GobletSpec]:
    return list(GOBLETS.values())


if __name__ == "__main__":
    print(f"{'size':5} {'V0_bowl (in^3)':>15} {'V_total (in^3)':>15} "
          f"{'A_neck (in^2)':>15} {'L_eff (in)':>10} {'fH (Hz)':>9}")
    for g in all_goblets():
        print(f"{g.size:5} {g.bowl_volume_in3():15.2f} "
              f"{g.total_volume_in3():15.2f} {g.neck_area_in2:15.2f} "
              f"{g.l_eff_in:10.2f} {g.closed_form_helmholtz_hz():9.2f}")
