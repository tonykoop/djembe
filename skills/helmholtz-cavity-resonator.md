---
name: helmholtz-cavity-resonator
domain: acoustics
description: |
  Predict the bass-tone fundamental frequency of a closed cavity coupled to
  one or more open ports (drum body + drumhead aperture, NAF flute slow-air
  chamber + flue, tongue drum interior + sound port, bottle + neck). Uses
  the Helmholtz lumped-element resonator formula plus a port end-correction.
status: validated against measured djembe bass tones (100–140 Hz prediction
  vs 80–120 Hz typical measurement)
canonical-location: tonykoop/djembe/skills/helmholtz-cavity-resonator.md
also-referenced-from:
  - tonykoop/djembe/README.md (Acoustics research section)
  - tonykoop/tongue-drum/study/README.md (cavity-coupling Q4 + bilateral Q7)
  - tonykoop/tongue-drum/SKILLS.md
provenance: |
  First derived from first principles in my undergrad acoustics
  presentation, ca. 2010. Original handwritten derivation scanned 2026-04-26
  into tonykoop/djembe/drawings/img20260426_*.png — particularly
  img20260426_00141714.png (formula + design rule "as V₀ increases, fH
  decreases ⇒ deeper bass") and img20260426_00115825.png (worked example
  computing V₀ = 162.3 in³ via the disk method).
audience: human (engineers, recruiters, drum builders) + agent (CLI / robotic)
maintainer: Tony Koop
license: CC-BY 4.0
---

# Helmholtz Cavity Resonator — Personal Skill

> *Predict the deep bass tone of an instrument or container by treating its enclosed air as a Helmholtz resonator. Reusable across drums, flutes, slit-tongue drums, and any closed-cavity-with-port geometry.*

## When to invoke this skill

You are predicting (or designing for) the fundamental bass tone of a cavity-with-port system:

- **Stave-built drums** — body cavity coupled through the drumhead aperture (djembe, dundun, frame drum, ashiko, conga).
- **Tongue/slit drums** — body cavity coupled through the slit openings.
- **NAF flutes** — slow-air chamber acting as the cavity, the flue as the port (a different acoustic role than the playing chamber).
- **Any rigid-walled hollow body with an opening** — bottles, gourd resonators, ocarinas in a limit, the cavity behind a guitar's sound hole.

**Don't invoke when:**

- The wavelength of interest is comparable to or smaller than the cavity dimensions (the lumped approximation breaks; you need the full wave equation).
- The port is so large there's no real constriction (e.g. a goblet glass).
- You care about higher modes — this gives only the fundamental.
- The cavity wall is itself a strong resonator (e.g. a tightly-tuned drumhead) — then you have a coupled-oscillator system and need a coupled model, not Helmholtz alone.

## The formula

$$f_H = \frac{c}{2\pi}\sqrt{\frac{A}{V_0 \cdot L_{\text{eff}}}}$$

Where:

| Symbol | Meaning | Typical units |
|---|---|---|
| *c* | Speed of sound in air | ~13,500 in/s, ~343 m/s at 20 °C |
| *A* | Cross-sectional area of the port | in², m² |
| *V₀* | Static cavity volume | in³, m³ |
| *L_eff* | Effective port length (actual + end correction) | in, m |

**End correction** (essential for short ports — the air mass extends slightly beyond the geometric port ends):

- Flanged opening (port flush with a wall, like most drumhead apertures): add `0.85 · r` per open end
- Unflanged opening (port like a tube into open air): add `0.61 · r` per open end
- Both ends open: add the end correction at both ends

Example: a 1" radius port that's 0.5" long, flanged at one end into the cavity and unflanged at the other (a typical sound port), has L_eff ≈ 0.5 + 0.85 · 1 + 0.61 · 1 = **1.96 in**. Without the end corrections you'd compute fH using L = 0.5 — about 2× too high.

## Method — design loop

1. **Pick the target tone.** What bass fundamental do you want, in Hz? (Convert from musical note via `f = 440 · 2^((n − 49)/12)` where *n* is the piano key number — A4 = 49.)
2. **Compute V₀ for your cavity.**
   - For a simple shape (cylinder, sphere, box), use the closed-form volume.
   - For a non-trivial axisymmetric profile (drum bowl, gourd), fit a circular arc through three measured profile points, then integrate the surface of revolution by the disk method:
     $$V_0 = \pi (b - a)\left[R^2 - \tfrac{1}{3}(b^2 + ab + a^2)\right]$$
     This is the [`circle-through-three-points`](circle-through-three-points.md) + [`surface-of-revolution-volume`](surface-of-revolution-volume.md) companion-skill pair (both stub'd for now; documented in djembe/drawings/ until extracted).
3. **Measure A, L_actual, and the port-end conditions.** Apply end corrections to get L_eff.
4. **Plug into the Helmholtz formula.** Compare predicted fH to target.
5. **Adjust geometry.** Tuning levers, in order of magnitude:
   - **V₀** — *fH ∝ 1/√V₀*. Doubling cavity volume drops fH by ~30%. The dominant lever for bass depth.
   - **L_eff** — *fH ∝ 1/√L_eff*. Lengthening the port (e.g. adding a tube, deepening the wall) drops fH.
   - **A** — *fH ∝ √A*. Smaller port → lower fH, but the square root means the effect is modest for small geometry changes. Easiest to vary if V₀ is fixed.

## Worked examples in my repos

### Djembe ([tonykoop/djembe](https://github.com/tonykoop/djembe))

The original derivation was for djembe bowl + drumhead. Cavity volumes computed from undergrad geometry: 162 in³ (small), 226 in³ (medium), 700 in³ (large). Predicted fH range **100–140 Hz**, sanity-checked against measured djembe bass tones (typically 80–120 Hz).

Full handwritten derivation lives at `djembe/drawings/img20260426_00141714.png` (formula + slide outline + the design rule **"as V₀ increases, fH decreases ⇒ deeper bass"**).

### Tongue drum ([tonykoop/tongue-drum](https://github.com/tonykoop/tongue-drum))

Phase 2 of the planned key-tuning DoE applies this skill to a bilateral-tongue cavity — does damping the tongues on bank A shift the resting fH on bank B? See `tongue-drum/study/README.md` Q4 (cavity coupling) and Q7 (bilateral tongue-bank coupling). The cavity-volume calculation here uses the same disk-method approach scaled to the rectangular box body.

### Future applications

- **Dundun (cylindrical):** trivially V₀ = π·r²·h. Should predict the bass-tone band each dundun voice supports before committing to body dimensions.
- **Didgeridoo:** primarily a tube-resonance instrument (1/4-wavelength), but the bell flare adds a Helmholtz-like correction at the bottom of its range.

## Failure modes I've hit

- **Forgot the end correction on a short port.** Predicted fH was ~30% too high. Lesson: any time `L_actual < port diameter`, the end correction matters more than the actual length. Always add it.
- **Treated a tensioned drumhead as a rigid wall.** A drumhead is the cavity wall but it also vibrates — the membrane modes couple to the cavity. The plain Helmholtz formula assumes rigid walls. For high-tension drumheads where the lowest membrane mode is comparable to the Helmholtz frequency, you need a coupled-oscillator model, not Helmholtz alone. Symptom: predicted fH and measured fH differ by 20–50% even after end correction.
- **Sub-wavelength assumption violation.** If wavelength λ = c/f gets smaller than ~4× cavity dimension, the lumped approximation breaks. For typical drum bass (80–200 Hz, λ = 5–13 ft) this is not a concern. For high-Q small cavities driven hard it could be.

## Provenance and cross-references

- **Original derivation:** Undergrad acoustics presentation, ca. 2010 — derived the resonant angular form `ω_H = √(γAP₀/(mV₀))` from first principles, then simplified to the practical form here.
- **Scanned notes (added 2026-04-26):**
  - `djembe/drawings/img20260426_00141714.png` — formula derivation, slide outline, design-rule annotation
  - `djembe/drawings/img20260426_00115825.png` — single-page worked example (R = 7.98", V₀ = 162.3 in³)
  - `djembe/drawings/img20260426_00132765.png` — height sweep: 20" total → R = 6.34, 22" total → R = 6.72
- **Repo narrative:** [`djembe/README.md`](../README.md) "Acoustics research" section.
- **Cross-referenced from:** [`tongue-drum/study/README.md`](https://github.com/tonykoop/tongue-drum/blob/main/study/README.md) — uses the same model for cavity-coupling Q4 + bilateral Q7.

## Companion skills (stubs — to extract when first re-used)

- **`circle-through-three-points`** — fit a circular arc to a measured drum profile. Provides the *R* needed for the volume integral.
- **`surface-of-revolution-volume`** — disk-method integral V₀ = π·∫[f(x)]² dx for an arbitrary axisymmetric profile.

These aren't yet pulled out as separate skill files — both are documented in `djembe/drawings/img20260426_00115825.png` and `img20260426_00132765.png`. Will extract here when the next instrument repo needs them.

---

*This file is a "human-take agent skill" — a personal-wiki entry written for both human readers (drum builders, engineers, recruiters) and CLI/robotic agents that may, in the near future, want to load my skills as context. Inspired by Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and [autoresearch](https://github.com/karpathy/autoresearch) ideas, with the distinguishing twist that the source material is hardware engineering rather than software/text work.*
