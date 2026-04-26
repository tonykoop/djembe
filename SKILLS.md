# Skills demonstrated in this repo

> *A "human-take agent skill" index — personal-wiki entries for the engineering methodologies this repository uses. Each linked file is written to be readable by both humans (engineers, drum builders, recruiters) and CLI/robotic agents that may want to load my skills as context. Inspired by Karpathy's [LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) and [autoresearch](https://github.com/karpathy/autoresearch) work, applied to hardware engineering practice.*

## Acoustics

- **[helmholtz-cavity-resonator](skills/helmholtz-cavity-resonator.md)** — Predict the bass-tone fundamental of a closed cavity coupled to an open port. The undergrad derivation that drives this skill is the heart of [`djembe/README.md`](README.md)'s "Acoustics research" section, and the same skill is referenced from the [`tongue-drum`](https://github.com/tonykoop/tongue-drum) study protocol for its bilateral cavity-coupling tests.

## Geometric methods (companion stubs — to extract on first reuse)

- **`circle-through-three-points`** — fit a circular arc to three measured profile points. Currently inline in `drawings/img20260426_00115825.png`. To be extracted as its own skill file when the next non-djembe project needs it.
- **`surface-of-revolution-volume`** — disk-method integral for the cavity volume of an arbitrary axisymmetric body. Currently inline in `drawings/img20260426_00115825.png` + `img20260426_00132765.png`. Same extraction trigger.

## Engineering practice (implicit; not yet extracted)

- **Stave-built shell construction** — the family of techniques (segmented stack, curved staves, lathe-finished cylinder) that this repository documents in narrative form. Not yet a standalone skill — see the README's "Engineering challenge" section for the worked-out tradeoffs.

---

## How this index works

Each skill is a self-contained `.md` file under `skills/` with:

- **YAML frontmatter** — name, description, status, canonical location, provenance, audience. Designed to be loadable by an agent.
- **When-to-use / when-not-to-use** sections.
- **Method** — the actual procedure, with formulas and step ordering.
- **Worked examples** — concrete numbers from my repos.
- **Failure modes** — the wrong turns I've taken and what they cost.
- **Provenance + cross-references** — where the skill was derived, which other repos use it.

The intent is that these files behave like Anthropic-style agent skills (loadable, declarative) while remaining first-rate documentation for a human reader. Stub skills listed above will be extracted into their own files the first time another project needs to reuse them — the rule is *don't extract until reuse forces it.*

A skill's **canonical location** is one repo — typically the one where the methodology was first derived or most deeply documented. Other repos that use the same skill link back to the canonical file rather than duplicating it. If a future `tonykoop-skills` meta-repo emerges, canonical files will migrate there and these per-repo `SKILLS.md` indexes will continue to point at them.
