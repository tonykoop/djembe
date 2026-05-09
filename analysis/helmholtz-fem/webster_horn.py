"""1D Webster's horn FEM for djembe goblet acoustic-cavity modes.

Solves the variable-cross-section Helmholtz wave equation:

    1     d  ⎡       dp ⎤        2
   ─── · ─── ⎢ A(z) ─── ⎥ + (ω/c)  · p = 0
   A(z)   dz ⎣       dz ⎦

with boundary conditions:

    z = 0   →   ∂p/∂z = 0   (rigid; the drumhead is treated as a rigid
                              wall — see "rigid-membrane assumption" in
                              `closed-form.md` and the failure mode
                              listed in `skills/helmholtz-cavity-resonator.md`)
    z = H   →   p = 0        (open foot; Dirichlet radiation BC)

Discretization: linear (P1) Galerkin finite elements on a uniform mesh
of `n_elem` elements over [0, H]. Element matrices use the
piecewise-linear A(z) sampled from `profile.GobletSpec.area_at`.

Generalized eigenvalue problem K p = λ M p,  λ = ω²/c² = k².
Frequencies: f_i = c · √λ_i / (2π).

Pure numpy. Uses `numpy.linalg.eigh` on the dense reduced (N×N)
matrix after enforcing the Dirichlet BC by node elimination. N up to
a few thousand is comfortable for a 1D problem on a laptop.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np

from profile import GobletSpec, SPEED_OF_SOUND_IN_PER_S


@dataclass(frozen=True)
class WebsterResult:
    """Acoustic-cavity mode-frequency result for a single goblet."""

    size: str
    n_elem: int
    z_nodes_in: np.ndarray              # (n_elem+1,)
    area_nodes_in2: np.ndarray          # (n_elem+1,)
    eigenvalues_per_in2: np.ndarray     # k^2 in 1/in^2, sorted ascending
    mode_shapes: np.ndarray             # (n_elem+1, n_modes); column k is mode k
    speed_of_sound_in_per_s: float

    @property
    def frequencies_hz(self) -> np.ndarray:
        c = self.speed_of_sound_in_per_s
        # f = c * k / (2 pi); k = sqrt(eigenvalue)
        k = np.sqrt(np.maximum(self.eigenvalues_per_in2, 0.0))
        return c * k / (2.0 * math.pi)


def assemble_webster(
    z: np.ndarray,
    A: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    """Assemble linear-FE stiffness K and mass M for Webster's horn.

    K_ij = ∫ A(z) φ_i'(z) φ_j'(z) dz
    M_ij = ∫ A(z) φ_i(z) φ_j(z) dz

    Uses element-averaged area Ā_e = (A_i + A_{i+1}) / 2.
    """
    n_nodes = len(z)
    n_elem = n_nodes - 1
    K = np.zeros((n_nodes, n_nodes))
    M = np.zeros((n_nodes, n_nodes))

    for e in range(n_elem):
        h = z[e + 1] - z[e]
        a_avg = 0.5 * (A[e] + A[e + 1])
        # Stiffness element: (Ā/h) * [[1,-1],[-1,1]]
        ke = (a_avg / h) * np.array([[1.0, -1.0], [-1.0, 1.0]])
        # Consistent mass: (Ā·h) * [[1/3, 1/6],[1/6, 1/3]]
        me = (a_avg * h) * np.array([[1.0 / 3.0, 1.0 / 6.0],
                                     [1.0 / 6.0, 1.0 / 3.0]])
        idx = [e, e + 1]
        for li, gi in enumerate(idx):
            for lj, gj in enumerate(idx):
                K[gi, gj] += ke[li, lj]
                M[gi, gj] += me[li, lj]

    return K, M


def solve_modes(
    spec: GobletSpec,
    n_elem: int = 800,
    n_modes: int = 5,
    c_in_per_s: float = SPEED_OF_SOUND_IN_PER_S,
) -> WebsterResult:
    """Solve K p = k² M p for the lowest `n_modes` modes of `spec`.

    BCs: rigid at z=0 (Neumann, natural), open at z=H (Dirichlet, p=0).
    The Dirichlet BC is imposed by eliminating the last node before
    solving the generalized eigenvalue problem.
    """
    z, A = spec.sample(n_elem + 1)
    K, M = assemble_webster(z, A)

    # Apply Dirichlet at z = H by eliminating the last row/column.
    K_red = K[:-1, :-1]
    M_red = M[:-1, :-1]

    # Solve generalized symmetric-positive-definite eigenproblem.
    # numpy lacks a direct generalized solver; reduce to standard form
    # via Cholesky of the SPD mass: L L^T = M_red, then solve
    # L^{-1} K_red L^{-T} y = λ y, p_red = L^{-T} y.
    L = np.linalg.cholesky(M_red)
    L_inv = np.linalg.inv(L)
    A_std = L_inv @ K_red @ L_inv.T
    # Symmetrize numerically.
    A_std = 0.5 * (A_std + A_std.T)
    eigvals, eigvecs = np.linalg.eigh(A_std)

    # Take lowest n_modes; transform back to physical eigenvectors.
    order = np.argsort(eigvals)
    sel = order[:n_modes]
    lambdas = eigvals[sel]
    p_red = L_inv.T @ eigvecs[:, sel]

    # Reinsert the Dirichlet zero at the foot node.
    p_full = np.vstack([p_red, np.zeros((1, n_modes))])

    return WebsterResult(
        size=spec.size,
        n_elem=n_elem,
        z_nodes_in=z,
        area_nodes_in2=A,
        eigenvalues_per_in2=lambdas,
        mode_shapes=p_full,
        speed_of_sound_in_per_s=c_in_per_s,
    )


# ---------------------------------------------------------------------------
# Self-verification: a uniform tube has analytic closed-open modes
# f_n = (2n - 1) · c / (4 H), n = 1, 2, 3, ...
# Checking the solver against that lets us trust the eigenvalues
# before applying them to a tapered goblet.
# ---------------------------------------------------------------------------


def _verify_uniform_tube(
    radius_in: float = 3.0,
    height_in: float = 20.0,
    n_elem: int = 800,
    c_in_per_s: float = SPEED_OF_SOUND_IN_PER_S,
    rtol: float = 5e-3,
) -> None:
    """Run a uniform-tube sanity check; raise AssertionError on failure."""
    area = math.pi * radius_in ** 2
    z = np.linspace(0.0, height_in, n_elem + 1)
    A = np.full_like(z, area)
    K, M = assemble_webster(z, A)
    K_red = K[:-1, :-1]
    M_red = M[:-1, :-1]
    L = np.linalg.cholesky(M_red)
    L_inv = np.linalg.inv(L)
    A_std = L_inv @ K_red @ L_inv.T
    A_std = 0.5 * (A_std + A_std.T)
    eigvals, _ = np.linalg.eigh(A_std)
    eigvals = np.sort(eigvals)[:5]
    f_numeric = c_in_per_s * np.sqrt(np.maximum(eigvals, 0.0)) / (2.0 * math.pi)
    f_analytic = np.array([(2 * n - 1) * c_in_per_s / (4 * height_in)
                           for n in range(1, 6)])
    rel = np.abs(f_numeric - f_analytic) / f_analytic
    if not (rel < rtol).all():
        raise AssertionError(
            f"uniform-tube verification failed:\n"
            f"  numeric   = {f_numeric}\n"
            f"  analytic  = {f_analytic}\n"
            f"  rel error = {rel}"
        )


if __name__ == "__main__":
    from profile import all_goblets

    print("Verifying solver against uniform closed-open tube ...")
    _verify_uniform_tube()
    print("  OK — first 5 modes within 0.5% of (2n-1) c / (4 H).\n")

    print(f"{'size':4} {'mode':>5} {'k^2 (1/in^2)':>16} {'f (Hz)':>10}")
    for g in all_goblets():
        result = solve_modes(g, n_elem=800, n_modes=3)
        for i, f in enumerate(result.frequencies_hz):
            print(f"{g.size:4} {i+1:5d} "
                  f"{result.eigenvalues_per_in2[i]:16.6f} {f:10.2f}")
