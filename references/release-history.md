# Release history

One row per release: what version you are on, the commit it was cut from, and what it changed. The full notes, with the numbers and the reasons, are in [`CHANGELOG.md`](../CHANGELOG.md). This file is the ledger that ties each of them to a commit.

**Which version is installed.** `version` in `.claude-plugin/plugin.json` and `metadata.version` in `SKILL.md`. They are held equal by `scripts/release-check.py`.

**How to read a row.** *Bump* follows the README versioning table: a **major** release changed a published value, so work built to the previous release can now fail. Before reusing a deliverable built on an older major, read that major's changelog entry. *Commit* is the commit that version shipped from. The newest row reads `pending` until its tag exists. A release's own commit cannot contain its own ID, so the tag records it and the row is filled when the next release is prepared.

**Maintainers.** Add the new row at the top in the same change as the CHANGELOG entry. Replace the previous `pending` with the full commit ID its tag points at. The release gate fails on a missing row, a date that disagrees with the changelog, a bump that disagrees with the version numbers, a commit that is not in history, or a tag that points somewhere else.

| Version | Date | Bump | Commit | What changed |
|---|---|---|---|---|
| [4.2.3](../CHANGELOG.md#423--2026-09-24) | 2026-09-24 | patch | `pending` | Release gate, integrity tests, CI and tagged-release workflow, this ledger, the output examples page. Export manifest corrected for three white markers |
| [4.2.2](../CHANGELOG.md#422--2026-09-07) | 2026-09-07 | patch | `9f1f55d82a95fb2c7f67745d09b5b7c2e6f83267` | Moved to its own repository with full history; every link repointed here |
| [4.2.1](../CHANGELOG.md#421--2026-09-07) | 2026-09-07 | patch | `51b5eced46e3d18a6087169ab3d3ab131acd1a0a` | One-line skills CLI install; SKILL.md description quoted for strict YAML |
| [4.2.0](../CHANGELOG.md#420--2026-08-08) | 2026-08-08 | minor | `de3c0662b01524cb8f9e4a3679f85d45eb42274a` | Token migration finished, zero remote libraries; specimen pages stop at hop 1 |
| [4.1.0](../CHANGELOG.md#410--2026-08-08) | 2026-08-08 | minor | `1a363c8697ad19c5cb35474ef6e0bac5f7c7be03` | Page 03 migrated; `brand/logo/*` constants; slide 14 defect retracted |
| [4.0.0](../CHANGELOG.md#400--2026-08-08) | 2026-08-08 | **major** | `4f8a45e6180f2ee77cca14b1eea370bc6b494203` | Variable layer rebuilt: five collections, the four grounds become modes |
| [3.2.1](../CHANGELOG.md#321--2026-07-28) | 2026-07-28 | patch | `6e09a5133cb762737c3e35c8d2faad5170d336e9` | T-03 characters-per-measure corrected to the measured 40/54/62 |
| [3.2.0](../CHANGELOG.md#320--2026-07-27) | 2026-07-27 | minor | `067ab4629ab1af7d9ff6759b3c61efd0ddc41f57` | Slide library: 36 measured layouts, plus the Arabic review findings |
| [3.1.0](../CHANGELOG.md#310--2026-07-27) | 2026-07-27 | minor | `9fe9275df8cee13214134fdb5f390f76235c2439` | Arabic/RTL build system, measured against a full 36-slide AR build |
| [3.0.0](../CHANGELOG.md#300--2026-07-27) | 2026-07-27 | **major** | `97c3d820f4696202dc2d3ab5e2507c5f8e19bdbf` | Fixed vertical anchors; body leading ×1.16 → ×1.35, motif module 24 → 20px |
| [2.0.0](../CHANGELOG.md#200--2026-07-27) | 2026-07-27 | **major** | `6a3cdb551a63556c1797cc592c5cfca4ed61ece6` | Client decision law, report-template system, Figma build gotchas |
| [0.2.0](../CHANGELOG.md#020--2026-07-26) | 2026-07-26 | minor | `af1c0e71d928ef3e2384694a110ca8a1ce867601` | First tagged cut; bundles 0.1.0 |
| [0.1.0](../CHANGELOG.md#010--2026-07-26) | 2026-07-26 | initial | `16cf9588e789c3a17ce31a23032efe8258065c4e` | Initial release from the Figma file audit |
