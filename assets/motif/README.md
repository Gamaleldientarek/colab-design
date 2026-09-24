# Colab dither / pixel motif engine

`motif.js` is the one implementation of the pixel/dither field described in `references/layout-archetypes.md` §4 (the slide motif) and `references/pixel-dither-posters.md` §3 (the poster-specific additions). One engine, any canvas size — a 1920×1080 slide and a 2480×3508 A4 poster both call the same function with canvas-px rectangles.

It is a plain browser global (`window.ColabMotif`), loaded with a `<script>` tag — no build step, no dependency.

---

## What it is

A density field of 20px squares that migrates sparse → dense toward an edge or corner, built the way halftone works: a per-cell density value `p(u)`, tested per cell against a decorrelating hash, never a hand-placed or blurred gradient. Optional `+`/`×`/`o` markers sit at cell intersections. See `SKILL.md` § "The pixel / dither motif" for the one-paragraph version and `layout-archetypes.md` §4 for the full derivation.

---

## API

```js
const result = ColabMotif.renderDitherField(container, box, opts);
```

- `container` — a positioned DOM element; filled cells and markers are appended to it as absolutely-positioned children.
- `box` — `{ x, y, w, h }` in canvas px. The field zone, snapped to the 20px module grid.
- `opts` — see the full option list in the header comment of `motif.js` (kept there, not duplicated here, so there is one place it can go stale). Summary:

| Option | Default | Purpose |
|---|---|---|
| `dir` | `'right'` | Which edge (`right`/`left`/`top`/`bottom`) or corner (`top-right`/`top-left`/`bottom-right`/`bottom-left`) the field migrates toward. Corners are new — see §3.1/§9 below |
| `a` | `3 * targetFill` | Peak coefficient for `p(u) = a·u²` (§4.3.1, `base = 0`) |
| `targetFill` | `0.18` | Mean fill fraction, used to derive `a` when `a` is not given |
| `extendPastEdge` | `0` | Fraction 0.2–0.5. Grid-past-edge sampling, §3.1 |
| `color` | — | One hex colour per field instance |
| `opacity` | `0.6` | Composite alpha — caller clears the §4.4 floor, this function does not |
| `seed` | `0` | Decorrelates independent fields sharing a canvas |
| `markers` | `true` | `false` disables all markers |
| `markerEvery` | `10` | Legacy probabilistic marker density (used when `maxMarkers` is unset) |
| `maxMarkers` | — | Caps the field to N markers, chosen deterministically nearest the dense edge/corner. The poster template's "exactly one marker" |
| `markerShape` | — | `'plus'` \| `'cross'` \| `'ring'`, forces every marker's glyph instead of the legacy random pick |
| `exclude` | `[]` | Array of `{x,y,w,h}` keep-out rects (e.g. a text node's ink box) |
| `excludePad` | `40` | Padding added to every exclude rect, px |

**Return value:** `{ cells, of, fill, modules, markers }` — `modules` and `markers` are arrays of `{x,y}` canvas px, one entry per placed cell. This is what makes a field "exportable as a list of individual module positions" per `pixel-dither-posters.md` §3.2, rather than a raster gradient standing in for one: every filled cell can be counted and audited from the return value alone, without re-parsing the DOM.

Nothing above changes the output of a field that does not pass the new options (`extendPastEdge`, `maxMarkers`, `markerShape`) — every existing slide field renders pixel-identical to before this file changed. Verified by re-rendering all six `assets/examples/0N-*.png` slides and diffing byte-for-byte against a fresh render (see the poster render report for the numbers).

---

## Minimal usage: a slide field (1920×1080)

```html
<div class="motif-field" id="field" style="position:absolute;inset:0;"></div>
<script src="../../motif/motif.js"></script>
<script>
  document.fonts.ready.then(function () {
    ColabMotif.renderDitherField(document.getElementById('field'),
      { x: 1500, y: 0, w: 420, h: 940 },                 // margin strip, C7-C8
      { dir: 'right', targetFill: 0.30, color: '#34FF67', opacity: 0.5,
        seed: 1, markerEvery: 10 });
  });
</script>
```

This is `assets/examples/src/01-cover.html`'s exact call — a single-edge field, the original engine surface, untouched.

## Minimal usage: an A4 poster field (2480×3508)

```html
<div class="motif-field" id="field" style="position:absolute;inset:0;"></div>
<script src="../../../motif/motif.js"></script>
<script>
  document.fonts.ready.then(function () {
    ColabMotif.renderDitherField(document.getElementById('field'),
      { x: 1260, y: 160, w: 1100, h: 1200 },              // field zone, §9.1 (C4-C6 x y160-1360)
      { dir: 'top-right', a: 0.70, extendPastEdge: 0.35,  // §3, §3.1
        color: '#34FF67', opacity: 1, seed: 1,
        maxMarkers: 1, markerShape: 'ring' });             // §4 item 3, §9.1
  });
</script>
```

`assets/examples/posters/src/poster-en.html` and `poster-ar.html` are the full worked examples, including the type zone, logo lockup and grounds.

---

## Which option implements which rule

| Option / behaviour | Rule | Reference |
|---|---|---|
| `hash2` per cell (never linear, never `Math.random()`) | Decorrelated cell selection | `layout-archetypes.md` §4.2 |
| `p(u) = a·u²`, `base = 0` | Edge-anchored dissolve | `layout-archetypes.md` §4.3.1 |
| `extendPastEdge` | Grid extends 20–50% past the dense edge/corner before evaluating density, then crops | `pixel-dither-posters.md` §3.1 |
| corner `dir` values (`top-right` etc.) | Poster field zone anchored to a corner, radial `u` — this engine's documented generalisation of the single-axis §4.3.1 form, not a separately ratified rule | `pixel-dither-posters.md` §5, §9.1 |
| `modules`/`markers` return arrays | Per-cell, list-exportable construction — never a blurred gradient standing in for the field | `pixel-dither-posters.md` §3.2 |
| `exclude`/`excludePad` | Keep-out zone, never under text | `layout-archetypes.md` §4, "never under text"; §4.6 |
| `color` (single hex) | One colour per field instance | `SKILL.md`, `layout-archetypes.md` §4 |
| `opacity` (caller-supplied) | Per-ground opacity floor — 40% Deep Jade, 50% Pine | `layout-archetypes.md` §4.4; `pixel-dither-posters.md` §7 |
| `maxMarkers` | Poster template's "exactly one accent marker" | `pixel-dither-posters.md` §4 item 3, §9.1 |
| `markerShape` | A named marker glyph (`+`/`×`/`o`) at cell intersections | `layout-archetypes.md` §4, "Markers" row |

---

## Rendering to PNG

There is no bundled render script in this repo; any headless Chromium-family browser works. The pattern used for every example in this skill (slides and posters):

```bash
# 1. Wait for fonts, then flag the page ready — every example src/*.html does this:
#    document.fonts.ready.then(function () { ...renderDitherField...; document.body.setAttribute('data-ready', '1'); });

# 2. Screenshot at the canvas's native px size, 1:1 device scale factor.
#    Slide (1920x1080):
chromium --headless=new --disable-gpu --hide-scrollbars \
  --window-size=1920,1080 --force-device-scale-factor=1 \
  --virtual-time-budget=5000 \
  --screenshot=out.png "file:///abs/path/to/slide.html"

# A4 poster at 300dpi (2480x3508):
chromium --headless=new --disable-gpu --hide-scrollbars \
  --window-size=2480,3508 --force-device-scale-factor=1 \
  --virtual-time-budget=5000 \
  --screenshot=out.png "file:///abs/path/to/poster.html"
```

Notes:

- **`--virtual-time-budget`** (or an equivalent explicit wait) matters — Google Fonts (Inter, Alexandria) load asynchronously, and the page's own `document.fonts.ready` gate must resolve before the screenshot fires, or type renders in a fallback face and the motif's `exclude` boxes (sized against the real ink) go stale.
- **`--force-device-scale-factor=1`** keeps the screenshot at exactly the CSS px size declared in the HTML (1920×1080 or 2480×3508) — without it a Retina host can silently double the output.
- A preview (e.g. `poster-en-preview.png` at 1240×1754, half the full A4 size) is a **resample of the full 2480×3508 render**, not a second HTML render at a smaller `--window-size` — the field, type and grid are all authored at fixed canvas px, so a half-size HTML render would need every coordinate in the source halved too. Resampling the finished PNG (Lanczos or equivalent) keeps the preview a faithful, cheap thumbnail of the exact same artifact, then re-compress for the file-size target.
- Any Chromium-family binary works — Google Chrome, Chromium, or a Playwright/Puppeteer-managed Chromium. This repo has no `package.json` browser dependency; use whatever headless Chromium is already on the machine.
