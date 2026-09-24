# Colab design tokens

Ready-to-use values for web and code work, so nothing is copied from the docs by hand.

| File | What it is |
|---|---|
| `tokens.json` | **The source.** Every value, grouped, each group with a `$source` pointer (file and section) |
| `tokens.css` | CSS custom properties, generated from `tokens.json` |
| `tokens.js` | The same values as an ES module, generated from `tokens.json` |

`tokens.css` and `tokens.js` are generated. Never edit them; edit `tokens.json` and rebuild.

## What is in it

- **`color`**: the primary and secondary palette, the on-light and on-dark variants (`olive-green-on-dark #A8B294`, `pale-sky-blue-on-light #3C7E94`), white, and the six 50 to 950 ramps from `references/colors.md` §4.
- **`ground`**: the semantic roles for the four grounds as modes: `light` (White), `jade` (Pine Green), `dark` (Deep Jade), `electric` (Electric Green). Surfaces, text, borders, icons, accent and the dither colour, with the per-mode values from `references/token-system.md` §5.
- **`constant`**: the roles that hold one value on every ground (`text/on-dark`, `text/on-light`, the logo colourways), from `token-system.md` §9.
- **`typography`**: Inter (EN) and Alexandria (AR), the six weights, the Display and Body scales from `SKILL.md`, the leading rules, the tracking values from `references/editorial-technique.md` §2.3 and §2.10.1, and the `Caps/*` sizes. Display 280 and 120 carry `"status": "pending-figma"`: they are specified but not yet built in the Figma file.
- **`grid`**: the 1920 × 1080 Advanced Presentation grid: 8 × 180 columns, 40 gutters, 100 margins, 50 bleed-safe, the footer band at y982, and every column's x.
- **`motif`**: the 20 px module, the 40 px 2× module, the 540 px span limit and the opacity floors (40% on Deep Jade, 50% on Pine).
- **`poster`**: the A4 pixel/dither poster grid from `references/pixel-dither-posters.md` §2.

In `tokens.json` a semantic token's `$value` is keyed by mode (`{"light": ..., "jade": ..., "dark": ..., "electric": ...}`) and a family's by language (`{"en": ..., "ar": ...}`). A translucent colour is `{"color": "#FFFFFF", "alpha": 0.1}`. Tracking is stored as a percentage of the font size, the way Figma states it; the CSS emits it in `em`. Scale entries point at their leading and tracking with an alias such as `"{typography.leading.body}"`.

## Using the CSS

Set the ground and the language on the root, then bind to roles, never to hues:

```html
<html data-ground="dark" lang="en">
<head>
  <link rel="stylesheet" href="tokens.css">
  <style>
    body  { background: var(--colab-surface-page); color: var(--colab-text-primary);
            font-family: var(--colab-font-body); }
    h1    { font-family: var(--colab-font-display); font-weight: var(--colab-font-weight-bold);
            font-size: var(--colab-display-160); line-height: var(--colab-display-160-leading);
            letter-spacing: var(--colab-display-160-tracking); }
    .kicker { color: var(--colab-text-accent); }
  </style>
</head>
```

- **Grounds.** `data-ground` takes `light`, `jade`, `dark` or `electric`. With no attribute a page reads as Light. Put `data-ground` on any element to change the ground for that panel and everything inside it.
- **Arabic.** Set `lang="ar"` (on the root or any element). The `:lang(ar)` block swaps both families to Alexandria, sets every leading to 1.5 and every tracking to 0. Sizes stay the same, as the system requires. Direction is yours to set: add `dir="rtl"`.
- **Names.** Palette and ramps: `--colab-color-pine-green`, `--colab-color-neutral-500`. Roles: `--colab-text-muted`, `--colab-border-accent`. Type: `--colab-display-60`, `--colab-body-24-leading`, `--colab-caps-12-tracking`. Grid, motif and poster: `--colab-grid-gutter`, `--colab-motif-module`, `--colab-poster-live-width`.

`text/accent`, `icon/accent` and `border/accent` already resolve to Pine Green on Light, which is how the Electric ban is kept. `accent/default` is a **fill**: on Light it is Electric Green with no visible edge (1.34:1), so give the shape `--colab-border-accent` (`token-system.md` §14). **Whether Electric may fill anything on a light ground at all is open client question Q-2** (`references/decision-law.md`): `SKILL.md` bans it in every role, while the Figma file and these tokens carry it. Until Q-2 is ruled, prefer Pine or Olive fills on Light.

## Using the JS

```js
import tokens from "./tokens.js";

tokens.ground.dark.text.primary;           // "#FFFFFF"
tokens.typography.display["160"];          // { size: 160, leading: 0.9, tracking: -2.5 }
tokens.typography.leading.ar;              // 1.5, at every size in Arabic
tokens.grid["column-x"].c5;                // 980
```

In the JS, tracking is a percentage (divide by 100 for `em`) and leading is a multiple of the size.

## Regenerating

```bash
python3 scripts/build-tokens.py           # rewrite tokens.css and tokens.js
python3 scripts/build-tokens.py --check   # fail if either is stale
python3 -m unittest tests.test_tokens -v
```

The build is deterministic and uses only the Python standard library.

## Where the truth lives

`tokens.json` is the source for the generated files. **The docs are the authority for the values**: `SKILL.md`, `references/colors.md`, `references/token-system.md`, `references/editorial-technique.md` and `references/pixel-dither-posters.md`. When they disagree, the docs win and `tokens.json` is corrected. `tests/test_tokens.py` enforces the agreement: the palette against `SKILL.md`, the ramps and variants against `colors.md`, every per-mode role against the `token-system.md` tables, every text contrast recomputed against the ratio those tables claim, the scales and leading rule against `SKILL.md`, the column positions against both grids, and no Electric or Jade in a Light foreground role. It also rebuilds the css and js and compares them byte for byte.

Values the docs do not pin down are left out rather than guessed. To add one, document it in the right reference first (see `CONTRIBUTING.md`), then add it here.
