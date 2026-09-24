# Colab — Decision Law

Standing client decisions, in force for all Colab work. These override any inference from the Figma file or from older references in this skill. Numbered entries mirror the project's constraint log (C-01…C-17); unnumbered entries are standing rules locked during the report-template build.

---

## Colour

**C-01 · Readability outranks expression — decks go to CEOs.** Default slide grounds are Pine Green `#103A21` or White. Electric Green is never a surface behind body text; as a flood it is limited to covers, dividers, and minimal-text slides, and takes Deep Jade text.

**C-01b · HARD BAN — Electric `#34FF67` and Jade `#33FFC2` never appear on a white or light ground.** Not as text, icons, decorative blocks, rules, number accents, or chip fills. On light grounds the accent role is played by Pine Green, Olive Green `#5B6B3E`, or Leaf Green `#066120` (positive ink). Enforceable check: audit every light-ground frame for fills bound to the Electric or Jade tokens — expected result, zero.

**C-01c · Charcoal Navy is banned.** Removed from the system entirely. The ground family is all-green: Pine `#103A21` (primary dark) · Deep Jade `#011E14` (deepest — high-drama slides; a client favourite) · White · Off-white `#F9FAFB` · Electric flood (covers/dividers only). Decks must rotate grounds, never run one ground throughout.

**Vivid Orange `#FF5A32` floors.** Never body text. As text: ≥20px Bold only (large-text contrast pass on dark grounds). As non-text glyphs/markers: permitted where ≥3:1 on the ground (4.10:1 on Pine, 5.65:1 on Deep Jade). Orange is severity-true — it appears only where something is critical or below target, never as decoration. One orange headline stat per slide maximum.

**Severity is ink-density, not hue.** The palette is green-heavy, so severity encoding survives colour-blindness through form: ring ○ = Positive · outline = Low · checker ▨ = Medium/Major · solid ■ = High · solid+× = Critical. Colour reinforces (Electric positive on dark / Leaf on light · Olive-300 `#A8B294` major on dark / Olive on light · Orange critical), form carries.

## Layout

**C-03 / C-09 · `Advanced Presentation` grid governs new work.** 16:9, 1920×1080. The 37 approved V2 slides stay frozen on their legacy grid as a *style* reference only — never rebuild them from new masters.

**V2 DNA — ⛔ SUPERSEDED 2026-07-27.** The x93 spine, y950 floor, x1880 limit, 100/200px titles, 50px eyebrows and 24px dither module are all retired. See **“V2 DNA (locked visual language, corrected 2026-07-27)”** at the end of this file for the current law, and the slide-anchors material in `references/layout-archetypes.md` §0.5.

**Logo appears in the footer only.** Never a second logo in a header or corner. Footer bar is a component instance at (40, 960), 1840×73, with a Ground variant per slide ground; the page-number layer is named `page-num` everywhere and matches the slide's number prefix.

## Type

**C-11 · `Typography/*` is the canonical scale** (Display **0.90 LH at ≥100px, 0.95 below**; Body **1.35 LH** — ratified 2026-07-27, supersedes 1.16); the old `Font-size/*` groups are deprecated. Weights relaxed: Regular/Medium/SemiBold sanctioned alongside Black/Bold/Light. **C-14 · Inter (EN) and Alexandria (AR) are the only fonts** — Jura, Poppins and other strays are leftovers, never carried forward.

**Tracking system (Inter dynamic metrics):** −2.5% at ≥100px · −2.2% at ≥40px · −1.7% to −2.0% at body sizes · positive tracking on all-caps labels (+4% typical, +6% at 12px). Arabic line-height floor 1.5 — never share a line-height token across EN and AR.

**Font variables:** every text node binds fontFamily (Display-Font vs Body-Font), fontStyle (font-weights/*) and — on exact scale matches — fontSize (Typography/*). Display-Font applies at ≥60px, or ≥40px when Bold/SemiBold/Black.

## Components & variables

**C-05 · Variables are the source of truth.** All new work binds fills to colour variables and instantiates components — no raw hex, no detached instances, no loose text.

**C-15 / C-16 · Logo = 7 lockups × 3 colours (Pine, Electric, White); Arabic is one lockup, not an axis. Shapes get a Colour property, no wide variants.** Bounding boxes constant per lockup so colour swaps never shift layout.

**Component variants must share identical geometry.** Inside an instance only text characters and fills can be overridden — child positions and sizes cannot. Variant deltas are therefore paint-only (alpha toggles) or nested-instance swaps. This is the single most important component-design law in the system.

## Icons

**C-04 · Phosphor is the standard for documents and the report template** (client-stated; line/outline style). Phosphor Figma imports are flattened fill paths — bind colour to `fill`. The legacy Brand Book placements are Hugeicons (live strokes — bind `stroke`); both sets coexist in the file. New report-template work uses the `Icon / *` Phosphor-derived masters. Resize icons with the W/H fields (24/28/32/40/48), never the Scale tool; never flatten; never detach.

## Report content

**C-17 · The report template is generic and international-standard.** Exactly the legacy section scope; English first, AR later; Figma-only delivery; master set + one filled example deck. Every real client name, project name and person name is stripped — placeholders are `Client Name`, `Project Name`, `P01`–`P08`, `Task 01`, `Month 2026`.

**Counting law (n<10):** counts before percentages — "6 of 8", never "75%". The disclosure line is non-negotiable on stat-bearing overview slides: *"n = 8 · Counts are reported rather than percentages — a sample this size does not support percentage claims."* SUS reports its grade honestly (69.4 = grade C, marginal); geometric mean — labelled GEO MEAN, not Avg — for time-on-task.

## Taste profile (what the client approves and rejects)

- **Approves:** giant display numerals; editorial full-width ledger rows; data-as-motif (counted fields where every module is a datum); Deep Jade grounds; mixed-ink titles (White + Electric spans in one line); flush baseline stat strips; generous but *filled* space.
- **Rejects:** pastel dashboard tints; uniform card-grid monotony; empty boxes; navy; decoration without data; dead space in the lower third of a slide; duplicated logos; headers carrying project names.

---

Replaces the sentence beginning *"**V2 DNA (locked visual language for the report template):** left spine x93 …"* in full.

**V2 DNA (locked visual language, corrected 2026-07-27):** left spine **x100** · content floor **y≤940** · right limit **x1820** · eyebrow top **y120**, title top **y168** on running slides; **y470 / y518** on statements · titles **Display 60** running, **Display 160** statement (tracking −2.5% at ≥100px, −2.2% at 60, LH 0.90 at ≥100px) · eyebrows **`Caps/M` 24, +4% tracking** · **20px**-module constellation dither, dense edge toward a canvas edge, `p(d) = base + peak·d^γ` with base 0.02–0.04 and γ 2.2–2.6, never below y940 · hairline rules at White@12–30 · radius 0 and zero effects on dark editorial slides.

**Superseded values and why:**

| Was | Now | Reason |
|---|---|---|
| Spine **x93** | **x100** | x93/x97/x973/x1413 are inherited −7px drift, not optical correction. Optical correction applies to the leading glyph, not the whole column |
| Floor **y950** | **y940** | 950 is not on the 4-unit; 940 is, and leaves 42px above the footer band |
| Right limit **x1880** | **x1820** | x1880 is the bleed margin, not a column end. Only grounds and motif may reach it |
| Titles **100 / 200px** | **60 / 160** | 100 and 200 are off the deck ladder (`editorial-technique.md` §2.10.1) |
| Eyebrows **50px Light** | **`Caps/M` 24 +4%** | 50 is off the ladder; a 50px eyebrow against a 100px title is 2.00 dominance against a title that should be 160 |
| Dither module **24px** | **20px** | `180 ÷ 24 = 7.5`. A 24px cell can never land on a column edge — see `layout-archetypes.md` §4.1 |

---

## Open client questions (raised 2026-09-24)

Eight questions surfaced by a construction audit of a client deck against this skill's current rules (Q-1 to Q-8), plus one conflict between the skill's own files that the same audit exposed (Q-9). **Current rules stand until each is ruled on** — new work follows the C-number cited, not the deck's measured value. New layout entries in `layout-archetypes.md` (archetypes 15–22) and `slide-library.md` (N1–N11) that touch these questions carry the deck's value as `[M]`, labelled with the Q-number below, beside the rule-compliant spec.

**Q-1 · Electric flood behind body text on a content-dense slide.** May an Electric Green flood sit behind multi-line body text on a slide that is dense with content — not a cover, divider, or minimal-text slide — the way the Detail spread archetype's (#19) colour panel does?
Rule until ruled: **C-01** — Electric Green is never a surface behind body text; as a flood it is limited to covers, dividers, and minimal-text slides.
Deck: a multi-line body statement sits directly on an Electric flood inside a colour panel, repeated across 5 instances of one template.
Options: (a) hold the line — move the body copy off the flood, the panel carries icon or ≤1 short line only; (b) carve out a bounded "detail panel" exception distinct from the slide's main content column; (c) cap the flood's text to a single short line (≤6 words) so it qualifies as minimal-text.

**Q-2 · Electric chips, icons and pills on light grounds.** Does the Electric-on-light ban extend to small chip fills, icon strokes and pill fills the way it already covers text, large fills and decorative blocks?
Rule until ruled: **C-01b** — Electric and Jade never appear on a white or light ground, in any role; the accent role on light is Pine Green or Olive Green.
Deck: numeral-chip fills, icon strokes, and one solid category-pill fill sampled Electric Green on white or pale cards, across four separate templates.
Options: (a) hold the line — C-01b already covers this; correct every instance to Pine or Olive; (b) allow Electric at small non-text sizes (≤48px chip/icon) where a Pine outline or label still carries the contrast; (c) document a separate "chip-fill" exception distinct from the body/large-fill ban.

**Q-3 · Section-colour grounds (teal, maroon, olive, navy per theme).** Should a per-topic colour-theme system — one dark ground plus a matching pale tint per topic — be adopted as new grounds, or folded into the existing four?
Rule until ruled: **C-01c** — the ground family is all-green (Pine, Deep Jade, White, Off-white, Electric flood); Charcoal Navy is explicitly banned and removed from the system.
Deck: two repeating templates (8 instances total) rotate dark grounds teal `#2A3D43`, maroon `#3F0C00`, olive `#333D21` and navy `#1D2A56`, each with a matching pale tint; only one instance (Pine) is on-palette.
Options: (a) reject — rebuild every instance on Pine/Deep Jade rotation only, losing the per-topic distinction; (b) adopt a small sanctioned theme-accent set built from colours already in the palette (Olive-based variants), rejecting the rest, including navy which is separately named-banned regardless of outcome; (c) accept the full per-topic system as a new axis alongside the four grounds, formalised as its own token tier.

**Q-4 · Pale-pink severity chip and its caption ink.** Is a pink/red-family fill permissible for the highest-severity item in a severity-scored list, and is the caption ink beside it on-palette?
Rule until ruled: **C-05** — variables are the source of truth, no raw hex; the palette has no red, Vivid Orange substitutes for critical severity ("Severity is ink-density, not hue," this file, above).
Deck: the top numeral chip in that list fills `#FCF2F9` (pale pink), a hue absent from the entire palette; the caption beside it sets `#6C737F`.
Options: (a) hold the line — replace the pink chip with Vivid Orange (critical) per the fixed severity scale, unchanged; (b) same, and additionally reserve Orange for true-critical rows only, using Pale Sky Blue for lower-severity items; (c) on the caption specifically — `#6C737F` already resolves from the sanctioned `text/muted` token on Light mode (`token-system.md` §5.2), so this half of the finding may not need a ruling: confirm whether it's meant to read as ordinary muted body text (already compliant) or as a distinct risk-colour cue (not compliant, needs the same fix as the chip).

**Q-5 · Near-black `#0D121C` ink.** Should `#0D121C` be adopted as a sanctioned dark ink for light and Electric grounds, alongside or instead of Pine and Deep Jade?
Rule until ruled: **C-05** — no raw hex; bind to `text/primary` (Pine on Light) or the Electric-flood ink rule (Deep Jade on Electric — SKILL.md "the one rule that matters most").
Deck: `#0D121C` recurs as the default headline/body ink on light and Electric grounds across seven pages spanning three templates, displacing both Pine and Deep Jade in that role.
Options: (a) hold the line — correct every instance to Pine on light, Deep Jade on Electric floods; (b) note that `#0D121C` is already the system's own `text/primary` value on Light mode (`token-system.md` §5.2) — confirm whether the client wants this specific near-black as the default light-ground ink instead of Pine, which would mean re-pointing the token rather than treating every instance as a defect; (c) adopt `#0D121C` only for statement-scale type, leaving Pine for body copy and UI.

**Q-6 · Framed cover inside the bleed-safe margin, logo used as cover art.** Can the cover/closer's framed construction — an asymmetric frame inset, a metadata slate sitting inside the 50px bleed-safe margin, a logo lockup used as the cover's own art — stand as built, or must it snap to the system's margins and footer-only logo rule?
Rule until ruled: **C-03/C-09** — nothing critical sits inside the 50px bleed-safe margin or left of the x100 column start; **C-03** — the logo appears in the footer only, never a second logo in a header or corner.
Deck: the metadata slate sits at x40/y≈37 on both the cover and the closer (inside both the bleed-safe margin and the column grid), and the logo lockup is placed as the cover's own art rather than in a footer band.
Options: (a) hold the line — rebuild on the system's own margins: uniform 50px frame inset, metadata slate at the standard meta-field position, logo confined to the footer band even on statement slides; (b) grant statement slides (cover/closer only) an explicit exception to the bleed-safe and footer-logo rules, since they're the deck's two poster-style pages; (c) keep the 40px side/bottom inset (a smaller breach of the 50px floor) but move the metadata slate and logo fully clear of the bleed-safe zone.

**Q-7 · Six-column activity-matrix grid.** Does a matrix of parallel workstreams get its own column count matched to the workstream count, or does it rebuild on the standard 8-column system?
Rule until ruled: **C-03/C-09** — the `Advanced Presentation` 8-column grid governs new work; every structural left edge lands on a legal column start.
Deck: one repeating template (5 instances) uses 6 evenly-pitched columns (pitch ≈303px), aligned to none of the 8 legal column starts.
Options: (a) hold the line — rebuild on 8 columns as 4-up of 2-column cells per row, a second row for workstreams past 4; (b) rebuild on 8 columns as 2 stacked rows of uneven cell width, keeping all items on one slide; (c) grant this one archetype a documented 6-column sub-grid as a second legal grid, scoped to it alone.

**Q-8 · Vertical anchors — the running eyebrow and divider titles.** Is the deck's own running-eyebrow position, well above the standard anchor, and its dividers' mid-page title placement a deliberate alternate vertical law, or drift to correct?
Rule until ruled: `layout-archetypes.md` §0.5 — eyebrow top y120 and title top y168 on every running slide, deviation 0px; eyebrow y470/title y518 on statement slides (covers, dividers, closing).
Deck: the running eyebrow/breadcrumb sits at y≈39–65 across nearly every page, with no text at the y168 title anchor on most running pages; the two dividers place their eyebrow/title at roughly y410–710 and y320–800, not y470/518.
Options: (a) hold the line — rebuild every running eyebrow at y120 and every divider title at y470/518, matching the Quiet divider variant (`layout-archetypes.md`, under #2; `slide-library.md` N11); (b) adopt the deck's higher eyebrow (y≈39–65) as a second legal running-page anchor, formalised as its own row in §0.5.1; (c) treat the divider's mid-page placement as legitimate only where there's no motif field to visually balance against (the Quiet divider case specifically), keeping y470/518 for every motif-bearing divider.

**Q-9 · Motif on content slides.** `SKILL.md` says **0%** on content slides (decorative motif only on statement slides and counted fields); `layout-archetypes.md` §4 says **≤20% of canvas** on content slides; the 36-slide library measures a median coverage of **0.027**, with a shallow edge band on most content slides (`slide-library.md` §3). Which is law?
Rule until ruled: none. Both texts stand, each flagged "(open: decision-law Q-9)" at the point of use: `SKILL.md`'s motif Coverage row, and `layout-archetypes.md`'s Coverage ceiling row, Discipline row and §4.5 content-slide row. New archetypes 15–22 specify "none, or a shallow edge field, per open Q-9" wherever a content slide would carry a field.
Measured: 31 of 36 library slides carry a field, the dominant shape is a shallow top band h200–360 anchored to the outer canvas edge, and median slide coverage is 0.027 (`layout-archetypes.md` §4.3.1).
Options: (a) **0% strict** — content slides carry no decorative field; the library's content-slide bands are drift to remove; (b) **a shallow edge field, ≤20% of canvas**, anchored to an outer canvas edge, never under text and never inside a chart area, which is what the library already does; (c) other — for example (b) with a lower ceiling set from the measured distribution.

Each Q is cited from its matching entry in `layout-archetypes.md` (archetypes 15–22 and §1.1) and `slide-library.md` (N1–N11), so a reader meets the open question at the point of use rather than only here.
