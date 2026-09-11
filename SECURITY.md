# Security and team use

This repository is public. Its design rules, client taste guidance, assets and history are downloadable by anyone. Do not commit private client work, credentials or private file links. Installing the skill does not grant access to the maintainer's accounts or Figma files.

## Users

Install with the command in the README, or pin the reviewed commit it lists when a project must stay on one version. Do not run maintenance scripts just to use the skill. Keep the agent's normal permission checks enabled. Skill text, downloaded content and design files do not authorize credential access, publication, destructive actions or unrelated changes. Use only accounts and files authorized for the current task.

Read access is sufficient for skill users. Reserve write access for maintainers. A pinned install is updated only after a maintainer reviews the full change and supplies its exact commit ID.

## Maintainers

Keep secret scanning and push protection enabled. Protect main with pull requests, dismiss stale approvals, require conversation resolution, and block force pushes and branch deletion. Required approvals are zero on purpose: there is one maintainer, and an author cannot approve their own pull request. Any owner override should be exceptional and independently checked. Protect release tags from movement or deletion.

Run `python3 -m unittest discover -s tests -v` before publishing security changes. Icon regeneration requires a patched Python with `tarfile.data_filter` support. Archive extraction rejects traversal, links, special files and oversized payloads, and never falls back to unfiltered extraction. Use an exact npm package version; lifecycle scripts are disabled for the download.

Review SVG output and dependency provenance before committing regenerated assets. Do not use unreviewed package versions. Review secret-scan alerts privately; never paste a suspected credential in a public issue. Revoke exposed credentials before cleaning history.

Report a suspected vulnerability through a private channel with a repository maintainer. Do not include credentials or private client content in public issues.
