# Djembe Starter Packet Risks

Current status: bare-bones readiness packet.
Fabrication authority: not build-ready.

## Scope Risks

| Risk | Why it matters | Mitigation |
| --- | --- | --- |
| Analysis is mistaken for empirical proof | The FEM work is useful, but no mic/FFT strike measurements are recorded. | Keep acoustic claims at analysis-only until `validation.csv` strike gates are filled. |
| Historical builds imply current reproducibility | Photos and Morgan Drums history show experience, not a current shop process. | Require current dimensions, process notes, and safety checks before build-ready claims. |
| Segmented, curved-stave, and lathe-finish paths get mixed | Each path has different cut geometry and failure modes. | Choose one construction path before writing cut lists or fixture drawings. |

## Acoustic Risks

| Risk | Why it matters | Mitigation |
| --- | --- | --- |
| Bass cavity model omits membrane coupling | Real djembe sound includes head modes and player strike technique. | Measure bass, open tone, and slap separately with repeatable strike notes. |
| Head tension dominates measured tone | The same shell can sound different under different rope tension and head condition. | Record head material, diameter, tuning state, and tension method with every acoustic test. |
| Room and mic placement skew FFT results | Low-frequency drum measurements are sensitive to placement and room modes. | Standardize mic distance, room notes, strike count, and analysis window. |

## Fabrication Risks

| Risk | Why it matters | Mitigation |
| --- | --- | --- |
| Stave joints open during turning or tuning | Curved shells and rope tension put stress on glue joints. | Validate glue-up on coupons or scrap rings before full-shell work. |
| Jig geometry is under-specified | A router or variable-angle sled can create unsafe or non-repeatable cuts. | Promote reviewed drawings/CAD and run scrap trials before instrument stock. |
| Legacy CAD is over-trusted | SolidWorks archive files may not match current design intent or shop constraints. | Treat legacy CAD as reference until reviewed, exported, and tied to a decision record. |

## Safety Risks

| Risk | Why it matters | Mitigation |
| --- | --- | --- |
| Rope and ring tension failure | Rope-tuned drums store energy and can fail during tuning. | Specify hardware, inspect knots/rings, and test gradually with eye protection. |
| Lathe or router operations on irregular blanks | Goblet shells and curved staves can be difficult to fixture safely. | Add workholding plans, guards, and scrap tests before live cuts. |
| Dust and finish exposure | Drum shell woods and finishing materials can create respiratory or skin hazards. | Add PPE, ventilation, and SDS checks when materials are selected. |

## Evidence Risks

| Risk | Why it matters | Mitigation |
| --- | --- | --- |
| Photos become dimensional authority | Images are useful but can distort scale. | Use scale references and separate photos from measured tables. |
| Supplier rows look current | Starter BOM entries may be mistaken for purchase-ready recommendations. | Keep `source_status` explicit and re-check suppliers at purchase time. |
| Cultural context is too thin | The djembe has Mande origins and should not be framed as an invented object. | Keep lineage notes visible in README and public-facing packet text. |
