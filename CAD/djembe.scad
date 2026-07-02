// Djembe goblet-body parametric master — outer envelope only.
//
// tonykoop/djembe
// Authority: pending_measurement. NOT fabrication authority until reviewed
// against a measured template (see visual-output-register.csv CAD-001 and
// validation.csv DJM-VAL-004 / DJM-VAL-006 gates).
//
// Dimension source (do not edit values without updating the source record):
//   - head/neck/foot diameters, neck z-window, and total height are read
//     verbatim from CAD/djembe-body/parametric-goblet.csv (Morgan Drums
//     S/M/L profiles; also summarized in README.md "Acoustics research —
//     bass-tone analysis" and wolfram/djembe-goblet-acoustics.wl).
//   - z is measured DOWNWARD from the head rim (z=0 at head, z=total_height
//     at foot), matching parametric-goblet.csv's own convention
//     (neck_length_in = z_neck_bot_in - z_neck_top_in).
//   - neck cross-section area (the CSV's neck_area_in2 column) is
//     recomputed below from neck_diameter_in as an in-file self-check,
//     never re-entered by hand.
//
// Explicitly OUT OF SCOPE here (measurement_required / hand-refined
// geometry per risks.md and drawing-brief.md — this master does not fake
// any of it):
//   - shell wall thickness / hollow interior. No thickness value exists in
//     bom.csv or cut-list.csv (both TBD); this master models the OUTER
//     envelope solid only, not a hollow shell.
//   - stave layout, miter angles, Approach A/B/C construction geometry
//     (see README.md "The engineering challenge") — belongs in CAD/stave/
//     once that geometry is reviewed.
//   - jig / fixture geometry — belongs in CAD/jigs/ once populated.
//   - bearing-edge profile, head/rim/rope tensioning hardware — measurement
//     required per validation.csv DJM-VAL-005 / DJM-VAL-007.
//
// Units: inches.

/* [Variant] */
// 0 = S (Morgan-9, small), 1 = M (Morgan-10, medium), 2 = L (Morgan-12, large)
variant = 1;

/* [Design table -- CAD/djembe-body/parametric-goblet.csv, verbatim] */
profile_label     = ["S -- Morgan-9 (small)", "M -- Morgan-10 (medium)", "L -- Morgan-12 (large)"];
head_dia_in       = [9.0000, 10.0000, 12.0000];
neck_dia_in       = [5.0000, 5.5000, 6.5000];
foot_dia_in       = [8.0000, 8.5000, 10.0000];
total_height_in   = [18.0000, 20.0000, 24.0000];
z_neck_top_in     = [4.1000, 4.6600, 10.1200];   // head-rim to top-of-neck, measured downward
z_neck_bot_in     = [6.1000, 6.6600, 12.6200];   // head-rim to bottom-of-neck, measured downward
neck_area_ref_in2 = [19.6350, 23.7583, 33.1831]; // csv column; self-check only, see below

/* [Active profile, derived from the design table] */
head_r = head_dia_in[variant] / 2;
neck_r = neck_dia_in[variant] / 2;
foot_r = foot_dia_in[variant] / 2;
height = total_height_in[variant];
z_top  = z_neck_top_in[variant];
z_bot  = z_neck_bot_in[variant];

// ---------------------------------------------------------------------------
// Self-check: recompute the neck cross-section area from neck_dia_in and
// diff it against the CSV's neck_area_in2 column. This just echoes at
// render time (OpenSCAD has no assert-and-continue); a nonzero diff means
// the design table and this master have drifted and need reconciling.
// ---------------------------------------------------------------------------
computed_neck_area_in2 = PI * pow(neck_r, 2);
echo(str("djembe.scad variant: ", profile_label[variant]));
echo(str("neck_area_in2 self-check -- computed=", computed_neck_area_in2,
         " csv=", neck_area_ref_in2[variant],
         " diff=", computed_neck_area_in2 - neck_area_ref_in2[variant]));

// ---------------------------------------------------------------------------
// Goblet outer-envelope profile: (radius, y) points where y is measured
// UPWARD from the foot (y=0) to the head rim (y=height), i.e. y = height-z.
// This is fed straight into rotate_extrude(), which revolves the 2D X axis
// as radius and the 2D Y axis as the extrusion/height axis around Z.
// Six points only -- foot axis, foot rim, bottom-of-neck, top-of-neck, head
// rim, head axis. No curvature is invented between the design-table points.
// ---------------------------------------------------------------------------
function goblet_profile() = [
  [0,      0],                // foot, on-axis
  [foot_r, 0],                // foot rim
  [neck_r, height - z_bot],   // bottom of neck (straight run starts)
  [neck_r, height - z_top],   // top of neck (straight run ends)
  [head_r, height],           // head rim
  [0,      height],           // head, on-axis
];

module goblet_shell_envelope(fn = 128) {
  rotate_extrude(angle = 360, $fn = fn)
    polygon(points = goblet_profile());
}

module djembe_assembly() {
  goblet_shell_envelope();
}

djembe_assembly();
