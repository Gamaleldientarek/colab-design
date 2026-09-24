# Poster pair (P1/P2) — inspiration session check

**Session date:** 2026-09-24
**Objective:** Ground the construction of two example A4 posters (EN, AR mirror) — P1 and P2 from `references/pixel-dither-posters.md` §9.1/§9.2 — plus the `extendPastEdge` and per-cell-export additions to `assets/motif/motif.js`, before building anything.

**Held pool checked first**, per `references/inspiration-sessions.md` §1: read `references/approved-inspirations.md` in full (Approved, Held, Rejected). Held entries — April Greiman (portrait-mass posters), RISOTTO (riso/screen print), Zuzana Licko (per-size redrawn pixel type), Nothing Ndot (cross-medium motif logic) — do not apply to this brief: P1/P2 are a type-and-field composition (not imagery-led), a digital export (not riso), use system Display type (not a pixel-drawn numeral face), and stay inside the existing print/poster system (no new medium to unify). None adopted or extended this session.

**Approved rules already cover the brief in full** — no new web search run, per the inspiration-sessions.md §1 rule that a request already covered by an existing reference does not need one:

- Anders Hoff, "Grains of Sand" → `pixel-dither-posters.md` §3.2, per-cell generation, never a blurred gradient standing in for the field. Implemented in `motif.js` by construction (one `hash2` test per cell) and made auditable via the new `modules`/`markers` arrays in the return value.
- Tyler Hobbs, Flow Fields → `pixel-dither-posters.md` §3.1, grid-past-edge sampling. Implemented as the new `extendPastEdge` option.
- Josef Müller-Brockmann, Beethoven poster → `pixel-dither-posters.md` §5, the fixed field-zone/type-zone split on one governing grid. Used directly for both posters' layout.
- Mike Joyce / Swissted → `pixel-dither-posters.md` §4, one fixed template reused; P1 and P2 vary only field anchor, headline and marker, per §6's EN/AR mirror rules.

**Engine addition beyond the four approved rules, and why it did not need its own session:** the poster's corner-anchored field zone (§9.1: "u = 0 at the field zone's inner edge, u = 1 toward the top-right corner") needed a two-axis generalisation of the existing single-axis `p(u) = a·u²` construction, since `layout-archetypes.md` §4.3.1 only derives the edge case. This is engine mechanics — a radial (Euclidean) distance-from-sparse-corner, normalised by the diagonal — not a new design precedent, so it is documented as a judgement call in `assets/motif/motif.js`'s header comment and in the poster render report, rather than logged as a new inspiration-session candidate.

No rejections. No new candidates proposed.
