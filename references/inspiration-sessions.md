# Colab — Online Inspiration Sessions

A repeatable procedure for finding and ratifying outside design references before building something the skill does not already cover. First run: 2026-09-24, building the pixel/dither poster capability (`references/pixel-dither-posters.md`). This file is the procedure; that session is the worked example.

---

## 1. When to run one

Run a session **before any new design that is not already covered by an existing archetype, slide, or reference.** Concretely:

- A request matches `layout-archetypes.md`'s 22 archetypes, `slide-library.md`'s 36 measured slides, or `report-template.md`'s catalog → build it directly. No session needed.
- A request is a new composition type, a new output format, or an unfamiliar construction (the way "A4 poster" was, before this system existed) → run a session first.
- **For a poster, always.** A poster is enough of a different discipline from a slide (§1 of `pixel-dither-posters.md`) that even a poster which superficially resembles an existing archetype should be checked against the held pool before being built from slide rules alone.

**Check the held pool first.** Before running new queries, read the Held table in `references/approved-inspirations.md`. An idea logged there may already answer the brief, or may need only a small extension (see §5). Re-researching something already held wastes the session; re-proposing it to the client, or adapting it, does not.

---

## 2. Scope and queries

State the objective in one sentence before searching — what kind of composition, at what canvas, for what purpose. Then run a batch of queries covering, in order:

1. **The literal construction** — the technique itself (e.g. "dither poster design pixel grid generative", "halftone gradient poster design studio case study").
2. **The nearest named design-history precedent** — a specific designer, studio, or movement plausibly relevant (e.g. "Müller-Brockmann modular grid poster A4 portrait", "April Greiman pixel poster MoMA").
3. **The nearest generative/algorithmic precedent** — practitioners who have published the actual mechanism (density functions, flow fields, particle systems), not just the look (e.g. "Anders Hoff inconvergent density field generative art", "Tyler Hobbs flow field generative art density algorithm").
4. **The nearest production/output-medium precedent**, if the output has a physical constraint — print, riso, screen (e.g. "riso print dither halftone poster bayer pattern studio").
5. **The nearest shipping comparable**, if one exists — a live product or brand using a related system today (e.g. "Nothing phone dot matrix design language pixel brand identity").

Ten to twenty queries is a normal session (the 2026-09-24 session ran eighteen). Log every query run, in the session file, whether or not it produced a candidate — a negative result is still evidence that the space was searched.

---

## 3. Source quality

- **Primary sources only.** The designer's or studio's own site, a museum or archive collection page, the original publisher. A secondary write-up is acceptable only when it is the best available route to the primary claim, and it must be marked as such in the credit line.
- **Never a guessed URL.** Every link in a candidate entry must either have been fetched directly, or be confirmed via a search index result that quotes or paraphrases it — state which. If a primary source is known to exist but blocks fetching, say so explicitly rather than silently substituting a secondary source (the 2026-09-24 session's Anders Hoff entry does this: "confirmed via search index; site blocks fetch").
- **Credit every candidate.** Name the designer or studio and the year, even for a candidate that ends up held or not pursued. An uncredited "inspired by" is not usable.
- **Log what was not pursued, and why.** A stock pack, a generic marketplace asset, or a reference that conflicts with a standing rule (multicolour where the system requires one colour per instance, a centred composition where the system requires asymmetry) belongs in a "Not pursued" section with a one-line reason — this is what stops the same dead end being searched again next session.

---

## 4. Palette discipline

**Take composition only from off-palette references.** An outside reference contributes *construction* — grid logic, a density algorithm, a template-reuse discipline, a zoning principle — never *colour*. Colab's palette (`references/colors.md`) does not move because a reference used a different one; a reference in full colour, riso multi-ink, or greyscale is read purely for its structural rule, and the resulting rule line must not mention or imply the source's own hues. This is the same discipline the motif rule already states — "one colour per instance" — extended to the research stage: if a reference's hue is doing the compositional work (Greiman's specific pixel-photo colour palette, a riso studio's ink set), extract the structural principle underneath it, not the colour.

---

## 5. Output format

Use the **session log structure** below as the template for every session file (see the 2026-09-24 session for a full worked example, saved under the skill's working notes):

```markdown
# [System] — inspiration session log

**Session date:** YYYY-MM-DD
**Objective:** one sentence — what capability this session is grounding
**Queries run:** the full list, in one paragraph or a bulleted line each

## Candidate directions

### N. [Designer/studio], "[Work]" (year)
One or two sentences describing the work — construction, not opinion.
**Why it fits:** how it answers the objective.
**Source:** URL(s), marked fetched or search-index-confirmed. Credit: name, year, publisher/venue.
**Rule:** one sentence, written as an instruction, ready to become a rule line if approved.

## Not pursued
- Reference — one-line reason

## [A4 portrait grid derivation / other worked arithmetic, if the session produced one]

## Gate [letter] decisions (Jimmy, YYYY-MM-DD)
- Approved → become rules: ...
- Held → reserve pool: ...
- Rejected: ...
```

Every candidate gets a numbered entry with the same five fields (why it fits, source, credit, rule) whether it is ultimately approved, held, or not pursued — the ledger in `references/approved-inspirations.md` is built directly from these entries, so the session log is the source data, not just a record of the conversation.

---

## 6. Feeding decisions back

A session log is a proposal. It becomes part of the skill only after Jimmy reviews it and the decision is captured in the three-state model:

- **Approved** → becomes a rule. Written into the destination reference file per `CONTRIBUTING.md`'s "where new knowledge goes" table (for a poster-construction rule, that is `references/pixel-dither-posters.md` or `layout-archetypes.md` §4, per the rule's actual subject), and logged in the Approved table of `references/approved-inspirations.md` with a pointer to where it now lives.
- **Held** → kept, not discarded. Logged in the Held table of `references/approved-inspirations.md` with the rule line it *would* become and the condition under which it might apply (a different medium, a different content type, a different part of the system). A held idea is checked against, per §1, at the start of every subsequent session — that is what makes it a pool rather than a rejection with a softer name.
- **Rejected** → explicit only. Jimmy states the rejection; nothing defaults to rejected. An idea that is simply not chosen this round is held, never silently dropped.

Once a decision is Approved, it goes through the normal release process exactly as any other new rule would, per `CONTRIBUTING.md`'s release checklist: measure/derive the number if one is needed, write it to the correct destination file with its evidence mark, delete or mark superseded whatever it replaces, record it in `CHANGELOG.md` and add the release-history row, and run the gate before it ships. An inspiration session is a research step upstream of that process, not a shortcut around it.
