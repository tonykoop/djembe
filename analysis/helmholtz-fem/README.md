# Helmholtz Cavity FEM — Goblet Validation

L3-frontier acoustic-cavity analysis closing the open question in
[`tonykoop/djembe#1`](https://github.com/tonykoop/djembe/issues/1):
does the lumped Helmholtz prediction for a stave-built djembe match a
full wave-equation cavity FEM, and if not by how much?

## Readiness

This analysis is **L3-frontier** per the hardware-development gate:

- ✅ **Physics gate.** Webster's horn equation derived; lumped
  Helmholtz formula documented; assumptions and failure modes called
  out per `skills/helmholtz-cavity-resonator.md`.
- ✅ **Artifact gate.** `parametric-goblet.csv`, three figure plots,
  one machine-readable `results.csv`, one human-readable `results.md`.
- ✅ **Solver-verification gate.** `webster_horn.py` self-checks against
  analytic closed-open uniform-tube modes (within 0.5% at 800 elements,
  used 1200 in production). The check raises on failure; passing it is
  a precondition for the comparison numbers being trustworthy.
- ⏸ **Empirical gate (deferred).** No physical drum was measured.
  The skill doc cites a measured 80–120 Hz range from prior builds; the
  FEM mode-1 numbers (123–190 Hz across S/M/L) are within 1.0–1.5× of
  that range, but this analysis does not claim L4-empirical
  validation. Mic + FFT measurement on the existing stave-built djembes
  is a follow-on.
- 🚫 **Manufacturing / safety gates.** N/A — analysis-only.

## Files

| File | Role |
|---|---|
| [`closed-form.md`](closed-form.md) | A, L_eff, V₀ mapping for the goblet; the lumped baseline |
| [`profile.py`](profile.py) | Parametric `r(z)` profile for S/M/L. Single source of truth for goblet geometry. |
| [`webster_horn.py`](webster_horn.py) | Pure-numpy linear-FE solver for the 1D Webster's horn equation. Self-verifies against analytic uniform-tube modes. |
| [`write_design_table.py`](write_design_table.py) | Emits `CAD/djembe-body/parametric-goblet.csv` from `profile.py`. |
| [`run_comparison.py`](run_comparison.py) | End-to-end driver: solver runs + figures + `results.csv` + `results.md`. |
| [`results.csv`](results.csv) | Machine-readable comparison table (one row per size). |
| [`results.md`](results.md) | Human-readable comparison memo. |
| [`capstone.md`](capstone.md) | Capstone deck (markdown). One slide per heading. |
| [`figures/`](figures/) | `goblet-profiles.png`, `mode-shapes-{S,M,L}.png`, `lumped-vs-fem-bar.png`. |

## Reproduce

```bash
cd analysis/helmholtz-fem

# 1. Sanity-check goblet geometry
python3 profile.py
#   prints V_0 / V_total / A_neck / L_eff / lumped f_H per size

# 2. Verify FEM solver against analytic uniform-tube modes,
#    then run all three goblets
python3 webster_horn.py
#   prints "OK — first 5 modes within 0.5% of (2n-1) c / (4 H)."
#   then prints lowest 3 modes per size

# 3. Generate figures + results.csv + results.md
python3 run_comparison.py

# 4. Re-emit the SolidWorks-style design table CSV
python3 write_design_table.py
```

Pure numpy + matplotlib. No SciPy, FEniCS, gmsh, COMSOL, or external
mesh tooling required. The solver is small enough (1200-element 1D
mesh) to run on any laptop in well under a second.

## Headline result

| Size | Lumped f_H (Hz) | FEM f₁ (Hz) | Δ vs lumped |
|---|---|---|---|
| Small (Morgan-9)  | 299 | 190 | **−36.4%** |
| Medium (Morgan-10) | 270 | 168 | **−37.8%** |
| Large (Morgan-12)  | 165 | 123 | **−25.7%** |

All three deviations exceed the 20% threshold the issue used as the
test for "the goblet effect is real and quantifiable." See
[`results.md`](results.md) for the full table including modes 2 and 3.

## Cross-references

- Issue: [`tonykoop/djembe#1`](https://github.com/tonykoop/djembe/issues/1)
- Skill (canonical formula and provenance):
  [`skills/helmholtz-cavity-resonator.md`](../../skills/helmholtz-cavity-resonator.md)
- Original derivation scan: `drawings/img20260426_00141714.png`
- Worked-example scan: `drawings/img20260426_00115825.png`
- Sister-repo reuse: `tongue-drum/study/README.md` Q4 (cavity coupling),
  `dundun` cavity work
