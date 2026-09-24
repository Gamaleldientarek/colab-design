# Colab — Inspiration Ledger

Every outside design reference the skill has evaluated, in one of three states: **approved** (became a rule), **held** (kept, may return or be adapted), **rejected** (explicit only — Jimmy states it, nothing defaults here). Procedure for running a session and capturing a decision: `references/inspiration-sessions.md`. **Check this file's Held table before starting a new session** — an idea logged here may already answer the brief.

---

## Approved

| Idea | Rule it became | Source / credit | Date approved | Session |
|---|---|---|---|---|
| Anders Hoff, "Grains of Sand" (2017) — density as a side effect of many individually-placed grains, not a rendered gradient | Every field module is generated individually against `p(d)`/`p(u)`; never approximate the field with a blurred gradient. See `references/pixel-dither-posters.md` §3.2 (extends the existing per-cell construction in `layout-archetypes.md` §4.2/§4.6 to the print pipeline) | https://inconvergent.net/2017/grains-of-sand/ (confirmed via search index; site blocks direct fetch). Credit: Anders Hoff | 2026-09-24 | 2026-09-24, pixel/dither poster session |
| Tyler Hobbs, Flow Fields — the control grid extends roughly −50% to +150% of the visible canvas so marks continue off-frame instead of clipping | The density-sampling grid extends 20–50% past each poster edge it touches before `p(u)` is evaluated, then crops to the canvas. See `references/pixel-dither-posters.md` §3.1 | https://www.tylerxhobbs.com/words/flow-fields (fetched). Credit: Tyler Hobbs | 2026-09-24 | 2026-09-24, pixel/dither poster session |
| Josef Müller-Brockmann, Beethoven poster, Zurich Tonhalle (1955) — a generative mark in an upper field, type reserved to a separate lower zone, both on one governing grid | The A4 template reserves a fixed type zone outside the field zone, on the same 20px module grid, never overlapping at any density. See `references/pixel-dither-posters.md` §5 | https://peoplesgdarchive.org/item/5754/beethoven-poster-for-the-zurich-town-hall (fetched). Credit: Josef Müller-Brockmann, 1955 | 2026-09-24 | 2026-09-24, pixel/dither poster session |
| Swissted, Mike Joyce — gig flyers redrawn as one reused International Style portrait template, only content and field placement changing | The A4 poster is one fixed template, reused; only field placement, the headline, and one accent marker vary per instance. See `references/pixel-dither-posters.md` §4 | https://imjustcreative.com/swissted · https://toolsandtoys.net/swissted-book-mike-joyce/ (search results). Credit: Mike Joyce / Stereotype Design | 2026-09-24 | 2026-09-24, pixel/dither poster session |

---

## Held

Not rejected. Kept with full sources and a draft rule line, and checked at the start of every new session (`references/inspiration-sessions.md` §1) before new queries are run.

| Idea | Rule it would become | When it might apply | Source / credit | Date held |
|---|---|---|---|---|
| April Greiman, "Does It Make Sense?" (*Design Quarterly* #133, 1986) — a coarse, visibly-pixelated collaged self-portrait held off-centre against a separate dense text block | Poster anchor mass sits off-centre, built from visibly coarse pixel modules, never a smoothed gradient; the text block occupies a separate zone, never overlaid on the field | A poster whose dominant mass is imagery or a portrait rather than a pure type-and-field composition | https://www.aprilgreiman.com/does-it-make-sense (fetched) · https://www.moma.org/collection/works/172729 (search result). Credit: April Greiman, 1986, *Design Quarterly* #133 (MIT Press) | 2026-09-24 |
| RISOTTO Studio, riso gradient/dither print documentation — three screen rulings, a randomized "Grain Touch" dither, and a 0–10% tonal failure zone on press | Treat the §4.3 base density floor as a hard *visible* minimum on screen; for riso or screen print, confirm the sparse end survives the specific press and screen ruling before finalising | Any poster going to riso or screen print rather than a digital export | https://risottostudio.com/pages/printing-faq (fetched). Credit: RISOTTO Studio | 2026-09-24 |
| Zuzana Licko, Emigre bitmap typefaces (from 1985) — letterforms drawn on the native pixel grid, a separate grid per point size, never scaled from one master | A pixel-built numeral or logo/lockup is redrawn on the module grid for each size band it is used at, never scaled from one drawing | Whenever pixel numerals or a pixel-built lockup are drawn, at more than one size | https://www.emigre.com/DigitalFontSketches (fetched) · https://www.moma.org/collection/works/139320 (search result). Credit: Zuzana Licko, Emigre | 2026-09-24 |
| Nothing, Ndot type and Glyph Matrix (2020–2026) — one dot-matrix logic carried across type, product surface, and motion on a restrained palette | The module and the `+ × o` marker set carry across UI, poster and motion as one logic; the A4 poster is not a separate system from the rest of the brand | Motion or UI work that needs to share the motif logic with print/poster work | https://design-milk.com/the-nothing-phone-3s-glyph-matrix-turns-notifications-into-pixel-art/ (fetched) · https://crewtangle.com/nothings-carefully-crafted-brand/ (search result). Credit: Nothing Technology Ltd | 2026-09-24 |

---

## Rejected

**Empty.** Rejection happens only when Jimmy explicitly rejects an idea. Nothing has been rejected as of this ledger — every candidate not approved defaults to Held, never here.

---

## Adopted from deck study

A separate 2026-09-24 review (an internal deck audit, not an online inspiration session) proposed eight new layout archetypes plus one variant of an existing archetype. Jimmy adopted all nine the same day. **By name only** — the geometry, anatomy and open questions for each live in `references/layout-archetypes.md` (archetypes 15–22 and §1.1) and `references/slide-library.md` (N1–N11), which are the authority; nothing about the source deck's content is repeated here, per the audit's own confidentiality gate.

Adopted, named exactly as in `layout-archetypes.md`:

1. Framed poster cover (archetype 15; also the mirrored closer)
2. Stacked word column (archetype 16)
3. Statement slide (archetype 17)
4. Card grid (archetype 18; a merge of two originally separate proposals)
5. Detail spread (archetype 19)
6. Metric card panel (archetype 20)
7. Activity matrix (archetype 21)
8. Notice slide (archetype 22)
9. Quiet divider (a variant of existing archetype 2, not a new archetype)

The final names are construction-only. The audit's working names echoed labels from the source deck's content and are not reproduced here or anywhere in the skill.
