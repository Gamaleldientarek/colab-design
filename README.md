<p align="center">
  <img src="assets/brand/cover.png" alt="Colab Design Skill — Colab User Experience Laboratory" width="100%">
</p>

# colab-design

[![ci](https://github.com/Gamaleldientarek/colab-design/actions/workflows/ci.yml/badge.svg)](https://github.com/Gamaleldientarek/colab-design/actions/workflows/ci.yml)
[![release](https://img.shields.io/github/v/release/Gamaleldientarek/colab-design?label=release)](references/release-history.md)

The Colab design system as an Agent Skill for [Claude Code](https://claude.com/claude-code), Cursor, Codex and Copilot.

Colab is a bilingual English/Arabic **User Experience Research Lab** working in Saudi Arabia and the wider MENA region. Install this skill and your agent builds Colab decks, reports, pages and Arabic versions to the brand's measured rules, without a re-brief each time.

**[See what you get →](EXAMPLES.md)** Seven real requests with the answers the skill produces: a colour check, a findings slide, a severity scale, web tokens, an Arabic mirror, an icon, and a slide review.

---

## Install

```bash
npx skills@latest add Gamaleldientarek/colab-design -g -a claude-code -y
```

Needs [Node.js](https://nodejs.org). Restart Claude Code. The skill loads on its own for anything Colab-branded, or call it with `/colab-design`.

| Tool | Flag |
|---|---|
| Claude Code | `-a claude-code` |
| Cursor | `-a cursor` |
| Codex | `-a codex` |
| GitHub Copilot | `-a github-copilot` |
| Every tool | `-a '*'` |

Update with `npx skills@latest update -g`, then restart the agent. Step-by-step without a terminal: [INSTALL.md](https://github.com/Gamaleldientarek/azmx/blob/main/INSTALL.md).

<details>
<summary><b>Pinned install</b>, for a project that must stay on a reviewed commit</summary>

```bash
mkdir -p .claude/skills
git clone --no-checkout https://github.com/Gamaleldientarek/colab-design.git .claude/skills/colab-design
git -C .claude/skills/colab-design checkout --detach 20ffe419f8d7cf3a47c695b3de96996447fd86c5
```

Needs Git. Stop if any command fails, and do not overwrite an existing folder. For Codex, use `.agents/skills` in place of `.claude/skills`. Keep your agent's normal permission prompts enabled.

A pinned install never updates on its own. To move it, a maintainer reviews the change and supplies the new full commit ID. Preserve local changes, fetch, inspect the difference from the installed commit, check out the approved commit in detached mode, and restart the agent. Normal design use needs only the bundled rules and assets, never the maintenance scripts. See [SECURITY.md](SECURITY.md) for the trust boundaries.

</details>

---

## What it knows

| Area | In short | Full rules |
|---|---|---|
| **Contrast** | Electric Green is an accent on dark, never a surface behind body text. Every pairing is computed with the WCAG 2.x formula | [`colors.md`](references/colors.md) |
| **Grounds and tokens** | Four grounds, White · Pine · Deep Jade · Electric, set as Figma variable modes. Five collections, 504 variables | [`token-system.md`](references/token-system.md) |
| **Type** | Inter (EN) and Alexandria (AR). Display ×0.90 at 100 px and above, ×0.95 below. Body ×1.35. Arabic ×1.5 with tracking 0, from the AR mode of `04 Typography` | [`editorial-technique.md`](references/editorial-technique.md) |
| **Grid** | 1920×1080, 8 columns of 180 px, 40 px gutters, 100 px margins, 50 px bleed-safe, footer band from y 982 | [`layout-archetypes.md`](references/layout-archetypes.md) |
| **Layouts** | 14 archetypes, fixed vertical anchors, and a per-slide pass gate. 36 measured slides ready to reuse | [`slide-library.md`](references/slide-library.md) |
| **Motif** | A 20 px dither field that migrates toward an edge. None on content slides, never under text | [`layout-archetypes.md`](references/layout-archetypes.md) §4 |
| **Arabic / RTL** | Mirror transform, auto-layout reversal, re-fitted rhythm, bidi traps, 12 verification predicates | [`rtl-arabic.md`](references/rtl-arabic.md) |
| **Icons** | Hugeicons Stroke Rounded only. 5,437 MIT-licensed SVGs vendored, with sizes, strokes and colour law | [`icons.md`](references/icons.md) |
| **Reports** | The componentized 31-slide usability-report system | [`report-template.md`](references/report-template.md) |
| **Client law** | Standing decisions C-01 to C-17 and the client's taste profile. Overrides anything older | [`decision-law.md`](references/decision-law.md) |

### The rule that governs everything

**Electric Green `#34FF67` is an accent on dark. It is never a surface behind body text.**

| Electric Green on | Contrast | |
|---|---|---|
| White `#FFFFFF` | **1.34 : 1** | Fails every threshold, including the 3 : 1 floor for non-text marks |
| Pine Green `#103A21` | **9.49 : 1** | AAA |
| Deep Jade `#011E14` | **13.07 : 1** | AAA, the widest margin in the system |

Decks go to CEOs, so readability outranks expression every time. Electric Green as a surface is reserved for covers, dividers and minimal-text slides.

### Palette

| | Hex | Role |
|---|---|---|
| Electric Green | `#34FF67` | The signature accent |
| Pine Green | `#103A21` | Default dark surface, the logo's default colour |
| Jade Green | `#33FFC2` | Secondary accent, used sparingly |
| Grey | `#BCBEC0` | True neutral, dark grounds only |
| Vivid Orange | `#FF5A32` | Critical severity. The palette has no red |
| Deep Jade | `#011E14` | Deepest ground. White reads 17.54 : 1 on it |
| Olive Green | `#5B6B3E` | Medium severity, the second accent on light |
| Pale Sky Blue | `#B1D9E8` | Low severity |

---

## What's inside

<details>
<summary>Repository map</summary>

```
SKILL.md                          Entry point: the rules needed on every job
EXAMPLES.md                       What the skill produces, by request
CONTRIBUTING.md                   Where knowledge goes, versioning, the release checklist
references/
  decision-law.md                 Standing client decision law C-01…C-17 + taste profile
  colors.md                       Full ramps, the pairing matrix, verified contrast ratios
  token-system.md                 THE token system: 4 grounds as modes, 5 collections, 7 traps
  figma-tokens.md                 ⛔ superseded: the retired collections, for reading old files
  variable-architecture.md        Picker mechanics: scopes, alias repair (layout superseded)
  components.md                   Logo, Shapes, Photo-Effect, slide masters, inventory
  logo-and-shapes.md              Every lockup and shape primitive: files, sizes, usage rules
  layout-archetypes.md            14 slide recipes, vertical anchors, motif construction, pass gate
  report-template.md              The componentized usability-report system
  rtl-arabic.md                   Arabic/RTL build system: mirror law, auto-layout, bidi, motif
  slide-library.md                36 measured EN slides + the AR derivation rules
  icons.md                        Hugeicons house rules, the 43-icon working set, colour + RTL
  icon-index.md                   Every vendored icon with its download link (sharded a–z)
  research-notes.md               Hugeicons, bilingual EN/AR, category conventions
  figma-workflow.md               Working in Figma: safety protocol, plugin API gotchas
  editorial-technique.md          20 named techniques, tracking/leading numbers, 10 archetypes
  release-history.md              Every release with its date, bump, commit and summary
assets/
  logo/                           21 logo SVGs, 7 lockups × 3 colours
  shapes/                         40 shape SVGs, 20 primitives × brand/white
  icons/stroke-rounded/           5,437 Hugeicons SVGs, MIT
  figma-export-manifest.json      Source variant, size and colour for every exported SVG
scripts/
  vendor-hugeicons.py             Re-vendor the icon set at a pinned version
  rebuild-icon-index.py           Regenerate references/icon-index.md and its shards
  release-check.py                The release gate: version, changelog, ledger, skill header, pin
tests/                            Integrity, contrast, release-gate and vendoring-security tests
.github/workflows/                CI on every pull request; release on a version tag
```

</details>

---

## Versions and releases

The installed version is `version` in [`.claude-plugin/plugin.json`](.claude-plugin/plugin.json), mirrored in `SKILL.md`. Every release has a row in **[`references/release-history.md`](references/release-history.md)** with its date, bump, commit and a one-line summary, and a full entry in **[`CHANGELOG.md`](CHANGELOG.md)** with the numbers and the reasons.

A **major** version means a published value changed, so work built to the previous major can now fail. Read that release's changelog entry before reusing older work.

Releases are gated. CI runs the tests and the release check on every pull request. Pushing a `vX.Y.Z` tag on `main` publishes a GitHub release only when the tag, `plugin.json`, the changelog, the ledger and `SKILL.md` all agree.

---

## Contributing

Read **[CONTRIBUTING.md](CONTRIBUTING.md)** before changing anything. It covers where new knowledge goes, the evidence marks, versioning, the release checklist, and regenerating assets. Security and access rules are in [SECURITY.md](SECURITY.md).

---

## Provenance

Derived from the client's Figma file (audited 2026-07-26), its Brand Book, and the 37 client-approved slides in `Design Slides V2`.

Layout archetype coordinates are derived for this grid from sourced composition principles: Swiss/International Typographic Style, Tufte's data-ink discipline, Duarte's single-accent rule, MBB governing-sentence structure, and published research on executive scanning behaviour. They are Colab's own design rules, not external benchmarks. `references/layout-archetypes.md` marks every claim as sourced or derived.

---

## Licence

The tooling and documentation structure are MIT. The Colab brand assets, palette and identity are the property of Colab and are not licensed for reuse.

The icons in `assets/icons/stroke-rounded/` are the Hugeicons free set, **MIT**, redistributed under the terms in `assets/icons/LICENSE`. Only the Stroke Rounded style is MIT. Hugeicons Pro styles (Solid, Duotone, Twotone, Bulk) and Pro types (Sharp, Standard) are **not** included and require a [Hugeicons Pro licence](https://hugeicons.com/license-agreement).
