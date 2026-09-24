#!/usr/bin/env python3
"""Gate a release: the version, the changelog, the skill header and the pin agree.

Usage:
    python3 scripts/release-check.py                 # check the working tree
    python3 scripts/release-check.py --tag v4.2.3    # also require the tag to match
    python3 scripts/release-check.py --notes v4.2.3  # print that release's changelog section

The version lives in exactly one place, `.claude-plugin/plugin.json`. Everything
else is checked against it:

- the newest `## X.Y.Z — YYYY-MM-DD` heading in CHANGELOG.md names the same version
- changelog versions are unique and strictly descending, dates never go forwards
- SKILL.md frontmatter names the skill, carries the same version, and its description
  fits the 1,024-character limit
- references/release-history.md has one row per changelog version, with the same date,
  the bump the version numbers imply, and a commit in history that any local tag agrees with
- the pinned commit in README.md exists and is an ancestor of HEAD
- a release tag, when given, is `v` + the plugin version

Exit status is 0 when every check passes, 1 otherwise. No dependencies beyond
the standard library and git.
"""
import argparse
import json
import os
import re
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

SEMVER = re.compile(r"^(0|[1-9]\d*)\.(0|[1-9]\d*)\.(0|[1-9]\d*)$")
HEADING = re.compile(r"^## (\S+) — (\d{4}-\d{2}-\d{2})\s*$", re.M)
LEDGER = re.compile(r"^\| \[([^\]]+)\]\([^)]*\) \| (\S+) \| \**(\w+)\** \| `([^`]+)` \|", re.M)
PIN = re.compile(r"checkout --detach ([0-9a-f]{40})")
DESCRIPTION_MAX = 1024


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as fh:
        return fh.read()


def plugin():
    return json.loads(read(".claude-plugin/plugin.json"))


def changelog_entries(text):
    """-> [(version, date)] in file order."""
    return HEADING.findall(text)


def changelog_section(text, version):
    """The body under one version's heading, without the heading itself."""
    matches = list(HEADING.finditer(text))
    for i, m in enumerate(matches):
        if m.group(1) == version:
            end = matches[i + 1].start() if i + 1 < len(matches) else len(text)
            return text[m.end():end].strip()
    return None


def frontmatter(text):
    """Flat `key: value` pairs from the leading `---` block, quotes removed."""
    if not text.startswith("---\n"):
        return None
    end = text.find("\n---", 4)
    if end < 0:
        return None
    fields = {}
    for line in text[4:end].splitlines():
        key, sep, value = line.partition(":")
        if sep:
            value = value.strip()
            if len(value) >= 2 and value[0] == value[-1] == '"':
                value = value[1:-1]
            fields[key.strip()] = value
    return fields


def ledger_rows(text):
    """-> [(version, date, bump, commit)] in file order."""
    return LEDGER.findall(text)


def implied_bump(version, previous):
    if previous is None:
        return "initial"
    new, old = as_tuple(version), as_tuple(previous)
    return "major" if new[0] != old[0] else "minor" if new[1] != old[1] else "patch"


def as_tuple(version):
    return tuple(int(p) for p in version.split("."))


def git(*args):
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True, text=True)


def check(tag=None):
    problems = []
    meta = plugin()
    version = meta.get("version", "")
    if not SEMVER.match(version):
        problems.append(f"plugin.json version {version!r} is not X.Y.Z")

    entries = changelog_entries(read("CHANGELOG.md"))
    if not entries:
        problems.append("CHANGELOG.md has no '## X.Y.Z — YYYY-MM-DD' headings")
    else:
        if entries[0][0] != version:
            problems.append(f"newest CHANGELOG entry is {entries[0][0]}, plugin.json says {version}")
        seen = set()
        for (v, d), (older_v, older_d) in zip(entries, entries[1:] + [(None, None)]):
            if not SEMVER.match(v):
                problems.append(f"CHANGELOG heading {v!r} is not X.Y.Z")
                continue
            if v in seen:
                problems.append(f"CHANGELOG lists {v} twice")
            seen.add(v)
            if older_v and SEMVER.match(older_v):
                if as_tuple(v) <= as_tuple(older_v):
                    problems.append(f"CHANGELOG {v} sits above {older_v} but is not newer")
                if d < older_d:
                    problems.append(f"CHANGELOG {v} is dated {d}, before {older_v} ({older_d})")

    fm = frontmatter(read("SKILL.md"))
    if fm is None:
        problems.append("SKILL.md has no frontmatter block")
    else:
        if fm.get("name") != meta.get("name"):
            problems.append(f"SKILL.md name {fm.get('name')!r} != plugin.json name {meta.get('name')!r}")
        desc = fm.get("description", "")
        if not desc:
            problems.append("SKILL.md description is empty")
        elif len(desc) > DESCRIPTION_MAX:
            problems.append(f"SKILL.md description is {len(desc)} characters, limit {DESCRIPTION_MAX}")
        if fm.get("version") != version:
            problems.append(f"SKILL.md metadata.version {fm.get('version')!r} != plugin.json version {version!r}")

    problems += check_ledger(entries)

    pins = PIN.findall(read("README.md"))
    if not pins:
        problems.append("README.md has no pinned 'checkout --detach <sha>' commit")
    for sha in pins:
        if git("cat-file", "-e", f"{sha}^{{commit}}").returncode != 0:
            problems.append(f"README pin {sha[:12]} is not a commit in this repository")
        elif git("merge-base", "--is-ancestor", sha, "HEAD").returncode != 0:
            problems.append(f"README pin {sha[:12]} is not an ancestor of HEAD")

    if tag is not None and tag != f"v{version}":
        problems.append(f"tag {tag} does not match plugin.json version v{version}")

    return problems


def check_ledger(entries):
    problems = []
    rows = ledger_rows(read("references/release-history.md"))
    versions = [v for v, _ in entries]
    if [r[0] for r in rows] != versions:
        return [f"release-history.md lists {[r[0] for r in rows]}, CHANGELOG lists {versions}"]
    dates = dict(entries)
    for i, (v, date, bump, commit) in enumerate(rows):
        older = versions[i + 1] if i + 1 < len(versions) else None
        if date != dates[v]:
            problems.append(f"release-history.md dates {v} {date}, CHANGELOG says {dates[v]}")
        if SEMVER.match(v) and (older is None or SEMVER.match(older)) and bump != implied_bump(v, older):
            problems.append(f"release-history.md calls {v} a {bump} bump, the numbers say {implied_bump(v, older)}")
        if commit == "pending":
            if i:
                problems.append(f"release-history.md {v} is still pending; fill in the commit its tag points at")
            continue
        if not re.fullmatch(r"[0-9a-f]{40}", commit):
            problems.append(f"release-history.md {v} commit {commit!r} is not a full commit ID")
        elif git("merge-base", "--is-ancestor", commit, "HEAD").returncode != 0:
            problems.append(f"release-history.md {v} commit {commit[:12]} is not in the history of HEAD")
        else:
            tagged = git("rev-parse", "--verify", "--quiet", f"refs/tags/v{v}^{{commit}}")
            if tagged.returncode == 0 and tagged.stdout.strip() != commit:
                problems.append(f"tag v{v} points at {tagged.stdout.strip()[:12]}, release-history.md says {commit[:12]}")
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--tag", help="release tag that must match the version, e.g. v4.2.3")
    parser.add_argument("--notes", metavar="TAG", help="print the changelog section for TAG and exit")
    args = parser.parse_args(argv)

    if args.notes:
        body = changelog_section(read("CHANGELOG.md"), args.notes.removeprefix("v"))
        if body is None:
            print(f"no CHANGELOG entry for {args.notes}", file=sys.stderr)
            return 1
        print(body)
        return 0

    problems = check(args.tag)
    for p in problems:
        print(f"FAIL  {p}", file=sys.stderr)
    if problems:
        return 1
    print(f"OK    colab-design {plugin()['version']} is releasable")
    return 0


if __name__ == "__main__":
    sys.exit(main())
