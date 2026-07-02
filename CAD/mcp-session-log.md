# MCP / External-Tool Session Log

V5 provenance record for artifacts generated or modified by external tools.
Required before claiming any artifact came from OpenSCAD, Blender, Illustrator,
Photoshop, Fusion, SketchUp, or similar tooling.

| session_id | tool | input_authority | outputs | role | authority_result | review_status | notes |
|---|---|---|---|---|---|---|---|
| fable-v5-refresh-2026-07-01 | claude-code (Fable 5) + OpenSCAD CLI | CAD/djembe-body/parametric-goblet.csv, design.md | CAD/djembe.scad | cad_authoring | pending_measurement | self_checked | Parametric goblet-body envelope master: head/neck/foot diameters, neck z-window, and total height read verbatim from parametric-goblet.csv (S/M/L Morgan profiles); neck cross-section area recomputed in-file as a design-table self-check (computed=23.7583, csv=23.7583 for medium). Wall thickness/hollow interior NOT modeled (no value in bom.csv/cut-list.csv, both TBD); stave layout, jig geometry, bearing edge, and head/rope hardware are out of scope (see risks.md, drawing-brief.md). OpenSCAD render check: pass (openscad -o STL, exit 0). |
| fable-v5-refresh-2026-07-01 | claude-code (Fable 5) | CAD/djembe-body/parametric-goblet.csv, README.md, analysis/helmholtz-fem/results.csv | wolfram/djembe-goblet-acoustics.wl | analysis_source | derived_preview | unreviewed | Pre-existing lumped-Helmholtz cavity acoustics source model for the Morgan S/M/L profiles; source-only, not executed (wolframscript not run this pass). Row added to visual-output-register.csv and this log for V5 provenance completeness; file content unchanged. |
| fable-v5-refresh-2026-07-01 | claude-code (Fable 5) | design.md, CAD/djembe-body/parametric-goblet.csv | bom.csv, sourcing.csv, cut-list.csv, validation.csv | packet_refresh | fabrication | self_checked | V5 refresh pass: existing tabular packet data reviewed against design.md/parametric-goblet.csv baseline; no dimension changes made, all TBD/measurement-required markers left as-is. Provenance rows added to satisfy V5 fabrication-artifact logging. |
