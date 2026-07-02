$fn = 72;

head_diameter_mm = 320;
overall_height_mm = 600;
stave_count = 14;        // valid range: 12 to 16
wall_mm = 12;
glue_gap_deg = 0.45;

wood_color = [0.55, 0.30, 0.13];
edge_color = [0.36, 0.19, 0.08];
hoop_color = [0.08, 0.07, 0.055];
rope_color = [0.78, 0.62, 0.36];

profile_z = [0, 70, 190, 305, 425, 535, 600];
profile_r = [145, 125, 82, 96, 135, 160, 158];

function clamp_staves(n) = min(16, max(12, n));
function lerp(a, b, t) = a + (b - a) * t;
function outer_r_at(i) = profile_r[i];
function inner_r_at(i) = max(2, profile_r[i] - wall_mm);
function pt(r, a, z) = [r * cos(a), r * sin(a), z];

module tube_ring(outer_r, inner_r, h, zc) {
    translate([0, 0, zc - h / 2])
        difference() {
            cylinder(h = h, r = outer_r);
            translate([0, 0, -0.5])
                cylinder(h = h + 1, r = inner_r);
        }
}

module stave(n = stave_count, index = 0, gap_deg = glue_gap_deg) {
    n2 = clamp_staves(n);
    pitch = 360 / n2;
    a0 = -pitch / 2 + gap_deg / 2;
    a1 =  pitch / 2 - gap_deg / 2;

    verts = [
        for (i = [0 : len(profile_z) - 1])
            each [
                pt(outer_r_at(i), a0, profile_z[i]),
                pt(outer_r_at(i), a1, profile_z[i]),
                pt(inner_r_at(i), a1, profile_z[i]),
                pt(inner_r_at(i), a0, profile_z[i])
            ]
    ];

    side_faces = [
        for (i = [0 : len(profile_z) - 2])
            each [
                [4*i + 0, 4*(i+1) + 0, 4*(i+1) + 1, 4*i + 1],
                [4*i + 1, 4*(i+1) + 1, 4*(i+1) + 2, 4*i + 2],
                [4*i + 2, 4*(i+1) + 2, 4*(i+1) + 3, 4*i + 3],
                [4*i + 3, 4*(i+1) + 3, 4*(i+1) + 0, 4*i + 0]
            ]
    ];

    end_faces = [
        [0, 1, 2, 3],
        [
            4*(len(profile_z)-1) + 3,
            4*(len(profile_z)-1) + 2,
            4*(len(profile_z)-1) + 1,
            4*(len(profile_z)-1) + 0
        ]
    ];

    color(index % 2 == 0 ? wood_color : edge_color)
        rotate([0, 0, index * pitch])
            polyhedron(points = verts, faces = concat(side_faces, end_faces), convexity = 5);
}

module shell(n = stave_count) {
    for (i = [0 : clamp_staves(n) - 1])
        stave(n = n, index = i);
}

module flesh_hoop() {
    color(hoop_color)
        tube_ring(outer_r = head_diameter_mm / 2 + 13,
                  inner_r = head_diameter_mm / 2 - 4,
                  h = 12,
                  zc = overall_height_mm + 10);
}

module crown_hoop() {
    color(hoop_color)
        tube_ring(outer_r = head_diameter_mm / 2 + 23,
                  inner_r = head_diameter_mm / 2 + 8,
                  h = 18,
                  zc = overall_height_mm - 18);
}

module base_ring() {
    color(hoop_color)
        tube_ring(outer_r = 158,
                  inner_r = 136,
                  h = 18,
                  zc = 38);
}

module stylized_head() {
    color([0.86, 0.78, 0.62, 0.62])
        translate([0, 0, overall_height_mm + 17])
            cylinder(h = 2, r = head_diameter_mm / 2);
}

module rope_between(a, top_z, top_r, bottom_z, bottom_r, rope_d = 5) {
    p1 = [top_r * cos(a), top_r * sin(a), top_z];
    p2 = [bottom_r * cos(a + 8), bottom_r * sin(a + 8), bottom_z];
    mid = (p1 + p2) / 2;
    v = p2 - p1;
    len_v = norm(v);
    yaw = atan2(v[1], v[0]);
    pitch = acos(v[2] / len_v);

    color(rope_color)
        translate(mid)
            rotate([0, pitch, yaw])
                cylinder(h = len_v, r = rope_d / 2, center = true, $fn = 16);
}

module tuning_ropes(n = stave_count) {
    n2 = clamp_staves(n);
    for (i = [0 : n2 - 1]) {
        a = i * 360 / n2;
        rope_between(a, overall_height_mm - 10, head_diameter_mm / 2 + 18, 50, 151);
        rope_between(a + 360 / (2 * n2), overall_height_mm - 22, head_diameter_mm / 2 + 20, 50, 151);
    }
}

module assembly() {
    shell(stave_count);
    flesh_hoop();
    crown_hoop();
    base_ring();
    stylized_head();
    tuning_ropes(stave_count);
}

assembly();