# Design Intent — djembe rev A

- Master CAD: `CAD/djembe.scad` (sha256: f54640659c859cbd9a7de8aadafbfd12501861a5ecde3acf5de337ba1b588601), driven by `CAD/djembe-body/parametric-goblet.csv` (sha256: 90f9dbf534af5e27823fdf9080c4d266db8c90001bdd95f90c22255b7c81208c)
- Function: A stave-built goblet-shaped hand drum — wide bowl at the head, narrowing neck, flared foot — with a goatskin (or equivalent) membrane head and rope tuning. The bowl/neck geometry sets the air-cavity Helmholtz bass tone (README.md "Acoustics research"); the open and slap tones are governed separately by membrane modes on the head, not modeled here. Three Morgan Drums size variants (S/M/L) exist in the design table.
- Environment: hand-struck acoustic instrument; rope tensioning is a sustained structural load on the shell and rim hardware; stave joints see glue-line stress during turning and tuning.
- Target qty: 1 (prototype). Deadline: TBD. Budget/unit ceiling: TBD.

## Critical dimensions (carry tolerances)

| Feature | Nominal (medium/M) | Tolerance | Why critical | Source |
| --- | --- | --- | --- | --- |
| Head diameter | 10.0 in | measurement-required | membrane strike area, sets tone/slap character | CAD/djembe-body/parametric-goblet.csv (reference_only) |
| Neck diameter | 5.5 in | measurement-required | Helmholtz neck cross-section area (bass coupling) | CAD/djembe-body/parametric-goblet.csv |
| Foot diameter | 8.5 in | measurement-required | shell stability / floor contact | CAD/djembe-body/parametric-goblet.csv |
| Total height | 20.0 in | measurement-required | overall bowl volume, drives bass frequency target | CAD/djembe-body/parametric-goblet.csv |
| Neck z-window (top/bottom, from head) | 4.66 in / 6.66 in | measurement-required | sets effective neck length L_eff in the Helmholtz model | CAD/djembe-body/parametric-goblet.csv |
| Shell wall thickness | TBD | not yet defined | structural load path + tone; do not thin below a floor once set | bom.csv, cut-list.csv (both TBD) |
| Head tension / rope schedule | TBD | not yet defined | membrane mode tuning, safety (stored energy) | risks.md; validation.csv DJM-VAL-005 |

## Incidental (free for DFM)

- Exterior finish (lacquer/oil), stave wood species selection within sourcing constraints, rope color/pattern, decorative seam treatment.

## Must-nots (DFM may never violate)

- Do not cut/turn shell stock until a construction path (segmented stack / curved staves / rough-cut-and-lathe-finish) is chosen and recorded (risks.md "Fabrication Risks"; validation.csv DJM-VAL-006).
- Do not treat the legacy SolidWorks archive (`CAD/Djembe/`, `CAD/Segmented Djembe/`, `CAD/legacy-archive-2018/`) or the Helmholtz/FEM analysis as fabrication authority — both are analysis/historical reference until strike-validated (risks.md "Scope Risks", "Acoustic Risks").
- Do not exceed rope/ring tension design values without a safety review — rope-tuned shells store energy and can fail during tuning (risks.md "Safety Risks").
- Do not skip scrap/coupon trials for router or lathe jig operations before committing instrument-grade stock (risks.md "Fabrication Risks").
- Do not model bearing edge, head/rim hardware, or jig geometry in `CAD/djembe.scad` — these stay measurement-required per the master's header comment and validation.csv DJM-VAL-005/DJM-VAL-007.

## Material intent

Per `bom.csv` (all rows currently source-needed / measurement-required): TBD North American hardwood shell blank, goatskin (or equivalent) drum head, tuning rope, steel tensioning rings, stave adhesive, and finish. No supplier or price data is verified in this packet — see `sourcing.csv`.

## Stage status

Stage 0 intake complete 2026-07-01. Gate A (Alpha shop compile) NOT yet run — no concessions logged, nothing presented as shippable.
