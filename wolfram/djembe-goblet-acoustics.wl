(* Djembe Goblet Drum — Parametric Cavity Acoustics Starter
   tonykoop/djembe
   Authority: estimate placeholders only.
   Goblet profiles from CAD/djembe-body/parametric-goblet.csv (Morgan S/M/L).
   Manipulate block is CloudDeploy-ready (Public-Execute). *)

(* ── Lumped Helmholtz resonator model ──
   f_H = (c / (2π)) * Sqrt[S / (V * L_eff)]
   where S = neck cross-section area, V = bowl volume, L_eff = effective neck length.
   See analysis/helmholtz-fem/ for the 1D Webster FEM that refines these estimates. *)

HelmholtzFreq[S_Real, V_Real, Leff_Real, c_Real : 343.0] :=
  (c / (2 Pi)) * Sqrt[S / (V * Leff)]

(* Convert inches³ → m³ *)
In3ToM3[x_Real] := x * 0.0000163871

(* Convert inches² → m² *)
In2ToM2[x_Real] := x * 0.00064516

(* Convert inches → m *)
InToM[x_Real] := x * 0.0254

(* Morgan profiles from parametric-goblet.csv *)
MorganProfiles = {
  <|"label" -> "Morgan-9 (S)", "head_in" -> 9.0, "neck_dia_in" -> 5.0,
    "foot_in" -> 8.0, "height_in" -> 18.0,
    "S_in2" -> 19.635, "Leff_in" -> 6.25, "V_in3" -> 603.2|>,
  <|"label" -> "Morgan-10 (M)", "head_in" -> 10.0, "neck_dia_in" -> 5.5,
    "foot_in" -> 8.5, "height_in" -> 20.0,
    "S_in2" -> 23.758, "Leff_in" -> 6.675, "V_in3" -> 794.8|>,
  <|"label" -> "Morgan-12 (L)", "head_in" -> 12.0, "neck_dia_in" -> 6.5,
    "foot_in" -> 10.0, "height_in" -> 24.0,
    "S_in2" -> 33.183, "Leff_in" -> 8.025, "V_in3" -> 1400.5|>
};

(* Print reference table *)
TableForm[
  Table[
    Module[{p = MorganProfiles[[i]]},
      {
        p["label"],
        NumberForm[p["head_in"], {4, 1}],
        NumberForm[p["height_in"], {4, 1}],
        NumberForm[
          HelmholtzFreq[
            In2ToM2[p["S_in2"]],
            In3ToM3[p["V_in3"]],
            InToM[p["Leff_in"]]
          ], {5, 1}
        ]
      }
    ],
    {i, 1, 3}
  ],
  TableHeadings -> {
    None,
    {"Profile", "Head diam (in)", "Height (in)", "Lumped f_H (Hz)"}
  }
]

(* ── Interactive Manipulate ── *)

djembeExplorer = Manipulate[
  Module[
    {
      (* Convert user sliders to SI *)
      S_m2   = In2ToM2[N[Pi * (neckDia_in / 2)^2]],
      Leff_m = InToM[leff_in],
      V_m3   = In3ToM3[bowl_in3],
      fH     = HelmholtzFreq[In2ToM2[N[Pi * (neckDia_in / 2)^2]], In3ToM3[bowl_in3], InToM[leff_in]]
    },
    Grid[{
      {"Head diameter (in)", NumberForm[headDia_in, {4, 1}]},
      {"Neck diameter (in)", NumberForm[neckDia_in, {4, 1}]},
      {"Neck effective length (in)", NumberForm[leff_in, {4, 2}]},
      {"Bowl volume (in³)", NumberForm[bowl_in3, {5, 0}]},
      {"Neck S (in²)", NumberForm[N[Pi * (neckDia_in / 2)^2], {4, 2}]},
      {"Lumped Helmholtz f₀ (Hz)", NumberForm[fH, {5, 1}]},
      {"Notes", "L1 estimate; FEM in analysis/ refines this."}
    },
    Frame -> All,
    Background -> {{GrayLevel[0.88], White}, None}]
  ],

  (* Controls *)
  {{headDia_in, 10.0, "Head diameter (in)"}, 8.0, 14.0, 0.5, Appearance -> "Labeled"},
  {{neckDia_in, 5.5, "Neck diameter (in)"}, 3.5, 8.0, 0.25, Appearance -> "Labeled"},
  {{leff_in, 6.5, "Eff. neck length (in)"}, 3.0, 12.0, 0.25, Appearance -> "Labeled"},
  {{bowl_in3, 700.0, "Bowl volume (in³)"}, 100.0, 1600.0, 10.0, Appearance -> "Labeled"},

  ControlPlacement -> Left,
  TrackedSymbols :> {headDia_in, neckDia_in, leff_in, bowl_in3}
]
