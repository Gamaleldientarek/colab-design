# Contributing and releasing

For maintainers and anyone proposing a change. To use the skill, you need only the [README](README.md). Access and trust rules are in [SECURITY.md](SECURITY.md).

## Where new knowledge goes

| Kind of knowledge | File |
|---|---|
| A client decision, or a rule the client can overrule | `references/decision-law.md` |
| A colour, ramp, or contrast measurement | `references/colors.md` |
| A Figma variable, a token, a mode, or which ground a slide sits on | `references/token-system.md` |
| Why a picker shows the wrong tokens, or an alias needs repairing | `references/variable-architecture.md` |
| Where a *retired* binding used to point (pre-2026-08-08 files) | `references/figma-tokens.md` |
| A typographic technique with a source or a derivation | `references/editorial-technique.md` |
| Where an edge goes on a slide: anchors, gates, motif construction | `references/layout-archetypes.md` |
| A component's anatomy, variants, or legal overrides | `references/components.md` |
| A Plugin API trap or a build-safety rule | `references/figma-workflow.md` |
| A report pattern or a research-reporting convention | `references/report-template.md` |
| Anything Arabic, RTL, mirroring, or bilingual | `references/rtl-arabic.md` |
| A slide layout, its geometry, its motif spec, its ground | `references/slide-library.md` |
| A pixel/dither poster rule: the A4 grid, the template, the field and type zones | `references/pixel-dither-posters.md` |
| How to run an online inspiration session and log its result | `references/inspiration-sessions.md` |
| An outside design reference and its state: approved, held or rejected | `references/approved-inspirations.md` |
| A new kind of request users should know the skill handles | `EXAMPLES.md` |

`SKILL.md` is loaded on **every** invocation. A rule earns a place there only if a designer would produce failing work without it. Everything else goes in a reference and gets a pointer.

## Evidence discipline

`editorial-technique.md` and `layout-archetypes.md` mark every claim:

- `[S]` **sourced**: from published typographic or design literature
- `[D]` **derived**: reasoned from a sourced principle onto this grid
- `[M]` **measured**: computed from the live Figma file or the WCAG formula

Keep the marks. They are why a reader can tell a brand preference from an accessibility fact, and dropping them makes the whole file equally arguable.

## Versioning

| Bump | When |
|---|---|
| **Major** | A published value changes, so work built to the previous release now fails. v3.0.0 changed body leading ×1.16 → ×1.35 and the motif module 24px → 20px |
| **Minor** | New references, new rules, new assets. Nothing previously correct becomes wrong |
| **Patch** | Corrections, typos, broken links, tooling |

The version is set in one place, `version` in `.claude-plugin/plugin.json`. `SKILL.md` carries a copy in `metadata.version`, and the release gate fails if they differ.

## Release checklist

The step that matters most is **4**. Two false statements, "letter-spacing is `0` at every size" and display "×0.95 throughout", survived the v2.0.0 release because the correction was *added* while the falsehood was left in place. A reader hitting the old line first has no way to know it lost. The same thing happened to "Deep Jade on Electric 13.91 : 1" in five files until 4.2.3; a test now recomputes those ratios.

1. **Measure before writing.** A rule without a number is an opinion. Ratios come from the WCAG relative-luminance formula, geometry from `absoluteBoundingBox`, counts from a real traversal
2. **Ratify open conflicts, once.** If two documents disagree, decide and record the decision. Do not restate both and let the reader pick
3. **Write to the destination file** per the table above
4. **⚠️ Delete what the change supersedes.** Grep the whole skill for the old value and remove or explicitly mark every instance. Adding a correction beside a falsehood leaves both true-looking:
   ```bash
   grep -rn "OLD_VALUE" SKILL.md README.md EXAMPLES.md references/*.md
   ```
5. **Sweep for residual contradictions** before tagging: the same grep, expecting zero hits
6. **Update the affected numbers in the Figma file too.** A skill that documents a state the file contradicts recreates the defect it is describing
7. **Record the release in three places, in the same change:**
   - `CHANGELOG.md`: a `## X.Y.Z — YYYY-MM-DD` entry with `Added` / `Changed` / `Fixed` / `Corrected`, the numbers and the reason. `Corrected` is for claims that were previously wrong, and it is not optional
   - `references/release-history.md`: a new top row with commit `pending`, and the previous row's `pending` replaced by the full commit ID its tag points at (`git rev-parse vX.Y.Z^{commit}`)
   - `.claude-plugin/plugin.json` `version` and `SKILL.md` `metadata.version`
8. **Run the gate locally.** Both must pass before a pull request, and CI runs them again on it
   ```bash
   python3 -m unittest discover -s tests -v
   python3 scripts/release-check.py
   ```
9. **Merge the pull request, then tag the merge commit on `main`.** The release workflow re-runs the tests, refuses a tag that is off `main` or does not equal `v` plus the plugin version, and publishes the GitHub release with that version's changelog section as its notes
   ```bash
   git switch main && git pull
   git tag -a vX.Y.Z -m "colab-design X.Y.Z" && git push origin vX.Y.Z
   ```
   Release tags are protected. A bad tag is fixed by releasing the next patch, never by moving the tag
10. **Move the README pin** when a release should become the reviewed snapshot for pinned installs. The gate checks that the pin is an ancestor of `HEAD`

## What the gate checks

`scripts/release-check.py` fails when:

- the newest CHANGELOG heading differs from `plugin.json`, or changelog versions repeat, run out of order, or go back in time
- `SKILL.md` names a different skill, carries a different version, or its description passes 1,024 characters
- `release-history.md` is missing a release, disagrees on a date, labels a bump the version numbers do not imply, leaves an older row `pending`, or names a commit that is not in history or that its tag does not point at
- the README pin is not an ancestor of `HEAD`
- a release tag is not `v` plus the plugin version

`python3 scripts/release-check.py --notes vX.Y.Z` prints one release's changelog section, which the release workflow uses as the GitHub release notes.

The tests in `tests/` also check that links and repo paths resolve, README and SKILL counts match disk, the icon index matches a fresh rebuild, every SVG is inert, the export manifest matches its files, every quoted contrast ratio recomputes, and no credential pattern is committed.

## Regenerating the vendored assets

Design tokens: edit `assets/tokens/tokens.json`, then run `python3 scripts/build-tokens.py` to regenerate `tokens.css` and `tokens.js`. `tests/test_tokens.py` fails if the generated files are stale or if a token disagrees with `SKILL.md`, `colors.md` or `token-system.md`.

```bash
python3 scripts/vendor-hugeicons.py      # re-vendor Hugeicons at a pinned version
python3 scripts/rebuild-icon-index.py    # rebuild the index from assets/icons/
```

The example slides in `assets/examples/` are rendered from `assets/examples/src/`, `assets/examples/archetypes/src/` and `assets/examples/posters/src/`: one HTML page per slide or poster, using `assets/motif/motif.js`, the dither engine (see `assets/motif/README.md`) (20 px module, hashed cell selection, density per §4 of `layout-archetypes.md`, text boxes excluded with 40 px clearance). Open a page in a headless browser after fonts load, screenshot at 1920×1080, and rebuild `strip.png` from the six. Re-render whenever a rule the slides show changes.

Logos and shapes are exported from the Figma component sets by hand. `assets/figma-export-manifest.json` records the source variant, size and colour of every SVG so an export can be verified against its origin. Update the manifest in the same change as the export; the tests compare byte counts and colours.
