# Closed-Form Helmholtz Bass Tone — Goblet Mapping

## Formula

The undergrad acoustics study (see `skills/helmholtz-cavity-resonator.md`,
provenance: `drawings/img20260426_00141714.png` formula derivation,
`drawings/img20260426_00115825.png` worked example) treats the djembe
bowl as a lumped Helmholtz resonator:

$$f_H = \frac{c}{2\pi}\sqrt{\frac{A}{V_0 \cdot L_{\text{eff}}}}$$

| Symbol | Meaning |
|---|---|
| `c` | Speed of sound in air, ~13 500 in/s ≈ 343 m/s at 20 °C |
| `A` | Cross-sectional area of the acoustic *port* |
| `V_0` | Static cavity volume |
| `L_eff` | Effective port length (geometric length + end corrections) |

The lumped model collapses the goblet into one cavity + one port:

```
  ┌──── drumhead ────┐         ← rigid wall (membrane treated as rigid)
  │                  │
  │   bowl cavity    │         ← V_0
  │                  │
  └─── ↓ neck ↓ ─────┘         ← port: A = neck cross-section
       ↓                       ← L_eff = neck length + end corrections
       ↓
  ┌─── foot opening ──┐        ← treated as "outside" by lumped model
```

The bowl above the neck is `V_0`. The neck is the port. **The foot below
the neck is dropped from the lumped model entirely** — that omission is
the goblet effect this study is trying to quantify.

## Mapping for the goblet body

For a stave-built djembe in the Morgan Drums catalog the three
geometry inputs are:

| Input | Source on goblet |
|---|---|
| `A` | Inside cross-section at the neck, the narrowest point of the body |
| `V_0` | Volume of the bowl section above the neck (disk-method integral over the stave profile from drumhead height down to neck height) |
| `L_eff` | Neck section length + flanged-port end corrections |

End corrections (per `skills/helmholtz-cavity-resonator.md`):

- `0.85 r` per end for a flanged opening (port flush with a wall)
- `0.61 r` per end for an unflanged opening (port like a tube into open air)

For a djembe goblet the top side of the neck opens into the bowl
(flanged), the bottom side of the neck opens into the foot section
(also flanged because the foot interior is wider than the neck), so:

```
L_eff = L_neck_geometric + 0.85 · r_neck + 0.85 · r_neck
      = L_neck_geometric + 1.7 · r_neck
```

## Three Morgan Drums sizes

Cavity volumes from the undergrad study (per `skills/helmholtz-cavity-resonator.md`
worked-example notes):

| Size | Head dia | Neck dia (approx) | Foot dia | Total height | V_0 (bowl above neck) |
|---|---|---|---|---|---|
| Small (S, "9-inch")  | 9.0 in  | 5.0 in | 8.0 in  | 18 in | **162 in³** |
| Medium (M, "10-inch") | 10.0 in | 5.5 in | 8.5 in  | 20 in | **226 in³** |
| Large (L, "12-inch")  | 12.0 in | 6.5 in | 10.0 in | 24 in | **700 in³** |

Per-size port (`neck`) parameters used in the closed-form prediction:

| Size | r_neck (in) | A_neck (in²) | L_neck_geometric (in) | L_eff (in) |
|---|---|---|---|---|
| S | 2.50 | 19.63 | 2.00 | 6.25 |
| M | 2.75 | 23.76 | 2.00 | 6.67 |
| L | 3.25 | 33.18 | 2.50 | 8.02 |

These are the inputs to `parametric-goblet.csv`. Per-size geometry is
parameterized in `analysis/helmholtz-fem/profile.py` and rendered into a
piecewise-linear axial profile `r(z)` for the FEM step.

## Closed-form prediction

Plugging in `c = 13 500 in/s` and using `V_0 = bowl cavity above the neck`
(the conventional lumped interpretation):

```
f_H_S = (13500 / 2π) · √(19.63 / (162 · 6.25))   ≈ 299 Hz
f_H_M = (13500 / 2π) · √(23.76 / (226 · 6.67))   ≈ 270 Hz
f_H_L = (13500 / 2π) · √(33.18 / (700 · 8.02))   ≈ 165 Hz
```

These are the lumped baseline values the FEM step is graded against.
They are conspicuously higher than typical measured djembe bass tones
(80–120 Hz reported in the skill doc); that delta is the *goblet
effect* this study is trying to quantify. The lumped model:

- Ignores the foot section's compliance entirely.
- Ignores the air mass actually inside the neck (the neck is treated as a
  zero-volume port).
- Cannot resolve mode 2 or mode 3.

A 1D Webster's-horn FEM on the full goblet profile resolves all three
of those omissions and is the L3-frontier reference this analysis is
built around. The exact lumped value matters less than the *deviation*
between closed-form and FEM.

## What the lumped model cannot see

1. **Foot cavity.** The volume below the neck is not in `V_0`. If the
   foot is wide and tall, it adds compliance the lumped model misses.
2. **Neck volume.** The neck is treated as a zero-volume port. In a real
   stave goblet the neck is several inches long with a few cubic inches
   of air in it — that air mass is part of the dynamics.
3. **Mode 2 and mode 3.** A lumped resonator has one degree of freedom.
   The full goblet has higher cavity modes the bass player can excite by
   slap and rim shots. The FEM step reports the lowest 3 modes.

## Cross-references

- Skill: [`skills/helmholtz-cavity-resonator.md`](../../skills/helmholtz-cavity-resonator.md)
- Original derivation scan: `drawings/img20260426_00141714.png`
- Worked example scan: `drawings/img20260426_00115825.png`
- Parametric profile: [`profile.py`](profile.py)
- FEM solver: [`webster_horn.py`](webster_horn.py)
- Comparison driver: [`run_comparison.py`](run_comparison.py)
