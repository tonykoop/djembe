# Djembe Bare-Bones Design Packet

Current status: bare-bones readiness packet.
Fabrication authority: not build-ready.
CAD/DXF status: future authority unless a reviewed drawing or design table is promoted.
Measurement status: measurement-required for tuning, shell fit, head tension, and jig geometry.

## Intent

This packet organizes the existing djembe repo evidence into a small reviewable
starter packet for a stave-built goblet drum. It does not replace the README,
the historical build notes, the segmented archive, or the Helmholtz/FEM
analysis. It gives the next builder a concrete set of decisions, materials,
and validation gates before the repo can become a shop packet.

The target instrument family is a stave-built djembe: a goblet-shaped hand drum
with a membrane head, open foot, rope tensioning, and a shell profile that
strongly affects the bass cavity mode. The repo currently has historical
finished-drum photos, scanned notebook pages, segmented construction studies,
legacy SolidWorks files, a parametric goblet CSV, and a 1D Webster horn FEM
analysis.

## Evidence Already In The Repo

| Evidence | Current authority | Notes |
| --- | --- | --- |
| `README.md` | narrative and provenance | Strong project story, cultural note, acoustics summary, and current repo map. |
| `analysis/helmholtz-fem/` | analysis scaffold | Solver self-checks against a uniform tube; no physical drum mic/FFT validation yet. |
| `analysis/helmholtz-fem/results.csv` | computed analysis output | Shows FEM mode 1 below lumped Helmholtz predictions for S/M/L profiles. |
| `CAD/djembe-body/parametric-goblet.csv` | parametric geometry reference | Useful for analysis and future CAD, but not a reviewed fabrication drawing. |
| `CAD/Segmented Djembe/` | historical segmented archive | Pattern spreadsheets and previews exist; current manufacturing authority is not established. |
| `CAD/legacy-archive-2018/` | legacy CAD archive | SolidWorks source exists, but review/export status is unknown. |
| `images/` and `drawings/` | documentation evidence | Photos and scans document history and concepts; they are not dimensional authority by themselves. |
| `validation-loop.csv` | next-build validation scaffold | Rows name the prediction, measurement method, status, and next action for strike, shell, head, and construction-path checks. |
| `visual-output-register.csv` | visual authority guard | Photos, scans, figures, and CAD/archive previews are recorded as reference-only until reviewed geometry authority exists. |

## Acoustic Model Boundary

The current bass-tone model treats the djembe cavity as a goblet resonator. The
README and `analysis/helmholtz-fem/results.md` document a useful analysis
result: a full-goblet Webster FEM predicts lower first cavity modes than the
lumped Helmholtz estimate for the S/M/L profiles.

That result is analysis evidence, not empirical validation. Before claiming
validated tuning behavior, the repo needs recorded strike data from real drums:
mic placement, head diameter, head material, tuning state, room conditions,
strike type, FFT method, and repeated measurements for bass, tone, and slap.

## Strike Validation Plan

Use `validation-loop.csv` as the next-build worksheet. The first empirical pass
should capture one identified physical drum, one head/tensioning state, and
three separate strike families:

| Strike family | What it checks | Required context |
| --- | --- | --- |
| Bass / center strike | Whether the cavity-mode analysis is directionally useful for a real drum. | Drum ID, head diameter, head material, tuning state, mic distance, room notes, sample rate, FFT window, and repeated takes. |
| Open tone | Whether rim/edge membrane response is being confused with the bass cavity model. | Strike position, hand technique, head/tension metadata, and repeated takes. |
| Slap | Whether the high transient content is documented separately from modeled cavity resonance. | Strike position, head/tension metadata, peak/transient notes, and repeated takes. |

Do not revise shell geometry from strike results until the shell dimensions,
head setup, rim/ring hardware, and rope tensioning state are recorded in the
same measurement bundle.

## Design Decisions Still Open

| Decision | Current value | Status | Required evidence |
| --- | --- | --- | --- |
| Construction path | stave-built djembe | assumption | Choose segmented stack, curved staves, or rough-cut plus lathe-finish for the next build. |
| Size target | S/M/L profiles in existing CSV | derived estimate | Confirm physical target dimensions and player ergonomics. |
| Head material and diameter | goatskin / TBD | source needed | Record actual head size, hide source, collar fit, and tensioning method. |
| Rope and ring hardware | rope-tuned / TBD | source needed | Record rope diameter, ring dimensions, knot pattern, and safety factor. |
| Shell wood | North American hardwood / TBD | source needed | Record species, moisture content, blank dimensions, and glue compatibility. |
| Jig geometry | future router jig or miter sled | requires measurement | Promote reviewed CAD/DXF/design table before cutting parts. |
| Acoustic targets | bass cavity mode plus membrane modes | measurement-required | Define target bass, tone, and slap metrics with measured examples. |

## Promotion Gates

This repo can move beyond a bare-bones packet only when:

1. `validation-loop.csv` has measured bass, open-tone, and slap rows for at least one known drum.
2. Shell geometry is captured in a reviewed drawing, design table, or CAD export.
3. Head material, rim/ring hardware, and rope tensioning state are tied to the strike session.
4. BOM and sourcing rows distinguish in-hand parts from supplier-unverified parts.
5. The chosen construction path has a cut list or fixture plan with tolerances.
6. Safety checks cover head tension, rope/ring loads, glue joints, turning work,
   and any CNC/router jig operations.

Until those gates pass, this packet should be read as a scaffold and evidence
map, not as a build-ready djembe plan.
