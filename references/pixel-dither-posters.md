# Colab — Pixel / Dither Poster System

**Prescriptive rules for a standalone A4 pixel or dither poster.** This is a distinct output type from the 1920×1080 slide — read this file before building one.

**Evidence key:** `[S]` sourced from published design work · `[D]` derived for this system from a sourced principle or a system constant · `[M]` measured (WCAG formula or grid arithmetic). Same convention as `layout-archetypes.md`.

This file does not restate `layout-archetypes.md` §4 (the pixel/dither motif construction: module math, the decorrelating hash, the density formula, the opacity floor, the placement algorithm). Read that first. Below is only what a **poster** does differently from a **slide**.

---

## 1. A poster composition is not a 16:9 slide

A slide is one frame in a sequence — grounds rotate, archetypes rotate, and a slide is read once at speed by an executive scanning for a decision. A poster is a single, standalone, portrait artifact meant to be read at rest, at arm's length or pinned to a wall, with no neighbouring slide to carry context or contrast.

Three consequences `[D]`:

1. **One artifact, one template.** A deck varies archetype and ground slide to slide (§8.1 of `layout-archetypes.md`, "no more than 4 consecutive slides on one archetype"). A poster series does the opposite: **one fixed template, reused** — see §4.
2. **No footer band, no chrome inheritance.** The 98px footer band and the running eyebrow/title anchors (`layout-archetypes.md` §0.5.1) are slide furniture. A poster has its own anchor set: the field zone and the type zone, defined in §5 below.
3. **Print, not projector.** A poster is evaluated at 300dpi on paper or as a static image, not through a lamp projector or Teams/Zoom compression. The projector caution in `SKILL.md` (chroma-key green degrading under compression) does not apply; the riso/screen-print caution in §7 below does.

---

## 2. The A4 grid

**Canvas: 2480 × 3508 px at 300dpi.** `[D]`

A4 is 210 × 297mm. At 300dpi: 210⁄25.4 × 300 = 2480.3 → **2480px**. 297⁄25.4 × 300 = 3507.9 → **3508px**.

**Module: 20px — the same base module as the slide grid** (`layout-archetypes.md` §4.1). One system, one atom, at two canvas sizes.

| Axis | Arithmetic | Result |
|---|---|---|
| Width in modules | 2480 ÷ 20 | **124 modules, exact** — no residual |
| Height in modules | 3508 ÷ 20 | **175.4** → 175 whole modules (3500px), **8px residual at the foot**, inside the bottom margin |

**Margins (L / T / R / B): 120 / 160 / 120 / 240 px**, i.e. 6 / 8 / 6 / 12 modules. `[D]`

**Live area:**

- Width: 2480 − 120 − 120 = **2240px = 112 modules**, exact. `[D]`
- Height: measured on the module grid, not by naive subtraction. Total module rows are 175 (§ above); top margin takes 8, bottom margin takes 12, leaving **175 − 8 − 12 = 155 modules = 3100px**. `[D]`
  - Note this is **not** 3508 − 160 − 240 = 3108. The 8px foot residual is not a whole module and sits outside the module-addressable live zone, folded into the bottom margin — so the bottom margin's true physical depth is 240 + 8 = **248px**, while its module-grid depth is 12 modules (240px). Both numbers are correct; they answer different questions (physical edge vs. legal module row).

**Live area: 2240 × 3100 px**, top-left corner at **(120, 160)**.

**Columns: 6 × 340px with 40px gutters.** `[D]`

6 × 340 + 5 × 40 = 2040 + 200 = **2240px** — exact fit to the live width.

| Col | C1 | C2 | C3 | C4 | C5 | C6 |
|---|---|---|---|---|---|---|
| x start | 120 | 500 | 880 | 1260 | 1640 | 2020 |
| x end | 460 | 840 | 1220 | 1600 | 1980 | 2360 |

Each column is 340px = **17 modules**; each gutter is 40px = **2 modules** (matching the slide grid's gutter-equals-2×-module rule). 6×17 + 5×2 = 102 + 10 = **112 modules** — matches the live-width module count exactly. `[M]`

**The grid is symmetric about its centre**, because the left and right margins are equal (120 = 120), so the live area is centred on the canvas: centre x = (120 + 2360) ⁄ 2 = **1240**, which also equals canvas-centre 2480 ⁄ 2. Mirror formula `x' = 2480 − x − w` therefore maps column to column: **C1↔C6, C2↔C5, C3↔C4** — the same relationship the slide grid has (C1↔C8 etc.), just with six columns instead of eight. `[M]`

**Vertical does not mirror** — top margin (160) ≠ bottom margin (240), matching the slide system's own rule that y-anchors are identical EN↔AR (`SKILL.md` Arabic/RTL rule 3). Only x mirrors.

**Zoning:** the field is anchored to a top corner of the live area — **top-right for EN, top-left for AR** (they are each other's mirror under the transform above) — and the type zone sits below it, both on the shared 20px module grid. See §5.

---

## 3. Motif construction — what differs from a slide field

Build the field exactly as `layout-archetypes.md` §4.1–4.6 specify: the 20px module, the `hash2` decorrelating hash (§4.2), `p(u) = 0.70·u²` for an edge-anchored band with `base = 0` (§4.3.1, the correct member of the family for a band that must dissolve rather than terminate in a hard line), the largest-free-rectangle placement discipline (§4.6), and the per-ground opacity floor (§4.4: 40% on Deep Jade, 50% on Pine). None of that changes for a poster. Two things are added, both from the 2026-09-24 inspiration session (`references/approved-inspirations.md`):

### 3.1 The grid extends past the poster edge before evaluating density

**Rule `[S→D]`, source: Tyler Hobbs, flow-field control grids extending roughly −50% to +150% of the visible canvas so marks continue off-frame instead of clipping.**

Sample the density function `p(u)` against a notional grid that extends **20–50% of the field zone's own width or height past each edge it touches** (the top and the dense-corner edge for a top-corner field), then crop to the live canvas. Concretely: if the field zone is 1100px wide, extend the sampling grid 220–550px beyond the canvas's outer edge before computing `u` and `p(u)`, and only render the cells that fall inside the canvas.

**Why:** without the extension, the single densest row of modules sits exactly on the poster's physical edge and is forced to be the `u = 1` maximum — which reads as an algorithmic cap, a visibly flat top to the gradient. With the extension, `u = 1` lies outside the printed sheet, so the visible edge shows a gradient that is still visibly climbing, not capped. Build a poster field once without the extension and once with it, side by side, to confirm the difference — the same verification discipline `layout-archetypes.md` §4.2 used for the decorrelating hash.

### 3.2 Every cell is generated individually — never a blurred gradient standing in for the field

**Rule `[S→D]`, source: Anders Hoff, "Grains of Sand" — density is a side effect of many individually-placed grains, not a rendered gradient.**

This restates, for a print pipeline specifically, what `layout-archetypes.md` §4.2/§4.6 already do on screen: each module is placed by testing `hash2(x, y) < p(u)` at that cell, one call per cell. The poster-specific risk is different from the slide's: at 300dpi a designer under time pressure can approximate the field with a feathered/blurred rectangle or a gradient-mesh fill behind a stencil of squares, which looks similar at a glance but is not the same object — it has no per-cell randomness, no true sparse end, and cannot be re-solved against a different type-zone height the way a real per-cell field can. **A poster field must be exportable as a list of individual module positions**, not a raster gradient. If the output pipeline is a rendering script, this is enforced by construction (§4.6's `placeModule` call per passing cell); if the output pipeline is manual (an artboard built by hand), the check is: can every filled module be selected and counted individually in the source file. If not, it is decoration standing in for a field, not the field.

### 3.3 What the poster grid changes, stated once

`layout-archetypes.md` §4.6's occupancy grid is 96 × 47 cells (1920 × 940px at 20px). The poster occupancy grid is **124 × 175 cells** (2480 × 3508px at 20px, before the live-area/margin mask is applied) — same construction, same `largestFreeRect` and `hash2` functions, different `W`/`H` constants and no y940 ceiling (the poster's own floor is the type zone's top edge, §5).

---

## 4. The fixed template

**Rule `[S→D]`, source: Swissted (Mike Joyce) — one reused International Style A4 template, redrawn per gig with only the content changing, never the system.**

A poster is not a new archetype every time. Define **one fixed A4 template** — the grid (§2), the field-zone/type-zone split (§5), the logo lockup position, and the credit/meta line position all held constant — and vary only three things between instances:

1. **Field placement** — which top corner it anchors to (EN right, AR left; see §6) and how much of the reserved field zone it fills (the field zone's own size is fixed by the template; the field's density and exact occupied rectangle within it, solved per §4.6, is not).
2. **The headline** — the word or short phrase in the type zone.
3. **One accent marker** — a single `+`, `×`, or `o` placed at one field cell intersection, per `layout-archetypes.md`'s existing marker rule (~1 per 8–12 plain modules, never adjacent to another). Exactly one marker may be swapped or repositioned per instance; the rest of the template does not move.

Everything else — grid, margins, column positions, type-zone geometry, logo position, ground family — is identical across every poster built from the template. This is what makes a *series* of posters read as one system rather than one-off compositions, the same discipline that makes Swissted's decades of gig flyers legible as one body of work.

---

## 5. The type zone

**Rule `[S→D]`, source: Josef Müller-Brockmann, Beethoven poster (Zurich Tonhalle, 1955) — a generative mark occupying a fixed field, with type reserved to a separate zone on the same governing grid, never inside the mark's own area.**

The live area (§2) splits into two non-overlapping zones, both bounded on the 20px module grid:

- **Field zone** — anchored to a top corner (§6). Its size is fixed by the template (§4), typically the upper portion of the live area.
- **Type zone** — the remaining live area below the field zone, full live-width (C1–C6), holding the headline, any supporting line, and the logo/credit meta block.

The two zones never overlap, at any density — this is the poster-scale version of the slide rule "the field never underlaps a text bounding box" (`layout-archetypes.md` §4, "never under text"), but formalised as a hard zone boundary fixed by the template rather than solved per-composition via the largest-free-rectangle algorithm. A poster does not need §4.6's free-rectangle solve for the *split* between field and type (the template fixes that); it still uses §4.6-style per-cell construction *inside* the field zone.

The boundary between the two zones is a legal module row (a multiple of 20px from the live-area top), with at least one 40px gutter of clear air between the field zone's lowest occupied cell and the type zone's top edge — the poster equivalent of the slide system's 40px content padding (`layout-archetypes.md` §4.6, `PAD = 40`).

Headline sizing draws from the existing Display type ladder in `SKILL.md` — no new sizes are introduced here. Left/right alignment of the headline follows the system rule "never centre a text block across the full column measure" (`SKILL.md` § Layout, rule 1): align it to the field-adjacent edge of the type zone (left for an EN top-right field, right for an AR top-left field), never centred.

---

## 6. EN/AR mirroring

Full mechanics — the coordinate transform, the vertical re-fit, the auto-layout laws, the motif re-solve order, the bidi traps — live in `references/rtl-arabic.md`. This section states only what is specific to the poster grid; that file governs.

- **Mirror:** `x' = 2480 − x − w`, using the A4 canvas width (§2). Columns swap **C1↔C6, C2↔C5, C3↔C4**.
- **Field anchor swaps corner:** top-right for EN, top-left for AR.
- **Type zone stays below the field in both languages** — only its horizontal alignment mirrors (left-aligned EN ↔ right-aligned AR), per `SKILL.md` Arabic/RTL rule 1 ("RTL is a coordinate transform on x... and not right-alignment [alone]").
- **Vertical does not mirror.** Top margin (160) and bottom margin (240) are identical in both languages; only the type zone's internal rhythm is re-fitted for Arabic's ×1.5 leading floor, exactly as `rtl-arabic.md` §5.2 describes for a slide's stat block. If the Arabic headline needs more height than the English one, that height comes from the type zone growing upward into a shorter field zone, not from breaking the margins.
- **Re-solve the field, never mirror it.** Per `SKILL.md` Arabic/RTL rule 6, solve the field's per-cell density *after* the Arabic headline geometry is final — the field zone's fixed outer box mirrors by construction (§2), but its occupied rectangle within that box is re-solved against Arabic-mode content, not flipped from the English render.
- **Numerals, logo and directional glyphs** follow `SKILL.md` unchanged: numerals stay LTR in Inter (Arabic/RTL rule 8), the logo is never mirrored (§ Logo) (use the Arabic lockup), and only genuinely directional marks (arrows, chevrons) flip — the `+`/`×`/`o` motif markers are not directional and do not flip.

---

## 7. Grounds and contrast

The poster uses the same four grounds as the slide system, as modes, and the same non-negotiable ban: **`SKILL.md`'s "one rule that matters most" applies without exception — Electric Green and Jade Green never appear on a White ground, in any role, including the motif field.** `[M]` A White-ground poster's field and headline ink are **Pine Green** (12.73:1) or, as the second tier, **Olive Green** (5.81:1) — never Electric or Jade, decorative or not.

On a dark ground, the field's opacity must clear the `layout-archetypes.md` §4.4 floor for that specific ground: **40% on Deep Jade (3.15:1), 50% on Pine (2.85:1 at 40% fails; 50% clears at 3.62:1)**. `[M]` Below the floor, per §4.4, the field "is decoration and must never carry data" — this applies even harder to a poster than a slide, because a poster has no accompanying number to carry the meaning if the field itself is illegible.

A poster series does not need the deck-level "rotate grounds, no more than 2 consecutive on one ground" gate (`layout-archetypes.md` §8.1) — there is no sequence — but if a series is produced (a run of posters sharing the template), rotate grounds across the run rather than fixing the whole series to one ground, for the same reason `SKILL.md`'s anti-pattern table gives against "one dark ground everywhere."

---

## 8. When a poster goes to print

If the poster is destined for riso or screen print rather than a digital export, the **held** RISOTTO reference applies — see `references/approved-inspirations.md`. In short: the §4.3.1 sparse-end floor (`base = 0`, dissolving to nothing) is a screen-safe value, not necessarily a press-safe one; confirm the sparse end survives the specific press and screen ruling before finalising, and treat 0–10% tonal values as a checked risk zone rather than an assumed pass. This is a held idea, not yet a ratified rule — apply it as a caution, and record what is learned back into the ledger per `references/inspiration-sessions.md`.

---

## 9. Example poster compositions

Four compositions, given as specs — coordinates on the A4 grid (§2), not finished artwork. Each is one instance of the fixed template (§4).

### 9.1 P1 — EN statement poster, dark ground

| Element | Spec |
|---|---|
| Ground | Pine Green `#103A21` |
| Field zone | Top-right anchor, C4–C6 × y160–1360 (x1260–2360, 1100 × 1200px = 55 × 60 modules) |
| Field construction | Per §3: `hash2` per cell, `p(u) = 0.70·u²`, `base = 0`, `u = 0` at the field zone's inner (bottom-left) edge, `u = 1` toward the top-right corner, sampling grid extended 20–50% past the canvas's top and right edges per §3.1 |
| Field ink | Electric Green `#34FF67` at 100% (solid modules; the §4.4 floor only binds a translucent field) |
| Gutter to type zone | 40px clear air (y1360–1400) |
| Type zone | y1400–3260, x120–2360 (full live width) |
| Headline | Left-aligned to C1 (x120), on the Display ladder, white ink |
| Accent marker | One `o` ring at a field cell intersection near the field's densest corner |
| Logo/credit | `colab.` lockup, White colourway, bottom of the type zone |

### 9.2 P2 — AR mirror of P1

| Element | Spec |
|---|---|
| Ground | Pine Green `#103A21` (unchanged — a controlled A/B against P1) |
| Field zone | Top-**left** anchor, mirrored via `x' = 2480 − x − w`: C1–C3 × y160–1360 (x120–1220) |
| Field construction | Re-solved per §6, not mirrored from P1 — same `p(u)` family, evaluated against the Arabic type zone's final geometry |
| Type zone | Same y-range as P1 (160→3260 boundary unchanged — vertical does not mirror), right-aligned to C6, Alexandria, tracking 0, leading ×1.5 per `SKILL.md` Typography |
| Headline | Right-aligned to C6 (x2360), same message as P1, translated — not transliterated coordinates |
| Logo/credit | Arabic lockup (never a mirrored English lockup), bottom of the type zone, right-aligned |

### 9.3 P3 — Counted-field data poster

| Element | Spec |
|---|---|
| Ground | Deep Jade `#011E14` |
| Field zone | Top-right anchor, full live width behind the count: C1–C6 × y160–2200 (2240 × 2040px), large because the field **is** the dataset, not decoration |
| Field construction | Not `p(u)`-generated — a **counted field** (`layout-archetypes.md` §4.5): one module per unit counted, laid out left-to-right, top-to-bottom inside the zone, at the module grid. Never re-solved or re-densified once the count is final |
| Field ink | Electric Green `#34FF67` at ≥40% (the Deep Jade floor, §4.4/§7) — every unit must individually clear 3:1, because in a counted field the module is the data point |
| Type zone | y2240–3260, holds exactly one numeral (the count) and one benchmark, per `SKILL.md`'s "a numeral alone is incomplete" rule — never a second stat |
| Accent marker | None — a counted field is data; markers are a decorative-field device only (`SKILL.md` Arabic/RTL rule 7, generalised: counted fields are never touched by the decorative marker rule) |

### 9.4 P4 — Light-ground poster (no Electric/Jade)

| Element | Spec |
|---|---|
| Ground | White |
| Field zone | Top-right anchor, C4–C6 × y160–1520 (1100 × 1360px), same construction as P1 |
| Field ink | **Pine Green**, solid modules — never Electric or Jade on White, per §7 |
| Type zone | y1560–3260, headline in Pine Green (12.73:1 on White), left-aligned to C1 |
| Accent marker | One `×` in Pine Green |
| Logo/credit | `colab.` lockup, Pine Green colourway |

This example exists specifically to keep the ban visible at the example layer, not just the rule layer — the same reason `EXAMPLES.md`'s example 1 is a colour check rather than an assertion.
