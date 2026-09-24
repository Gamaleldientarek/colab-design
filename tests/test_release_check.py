"""scripts/release-check.py catches every way a release can disagree with itself."""
import importlib.util
import json
from pathlib import Path
import unittest
from unittest.mock import patch

ROOT = Path(__file__).parents[1]
spec = importlib.util.spec_from_file_location("release_check", ROOT / "scripts/release-check.py")
rc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(rc)

PIN = "20ffe419f8d7cf3a47c695b3de96996447fd86c5"
SHIPPED = "9f1f55d82a95fb2c7f67745d09b5b7c2e6f83267"  # the commit v4.2.2 was tagged on
LEDGER = ("| Version | Date | Bump | Commit | What changed |\n|---|---|---|---|---|\n"
          "| [4.2.3](x) | 2026-09-24 | patch | `pending` | Gate |\n"
          f"| [4.2.2](x) | 2026-09-07 | initial | `{SHIPPED}` | Move |\n")
GOOD = {
    ".claude-plugin/plugin.json": json.dumps({"name": "colab-design", "version": "4.2.3"}),
    "CHANGELOG.md": "# Changelog\n\n## 4.2.3 — 2026-09-24\n\nPatch.\n\n## 4.2.2 — 2026-09-07\n\nOlder.\n",
    "SKILL.md": '---\nname: colab-design\ndescription: "Apply the Colab design system."\nmetadata:\n  version: "4.2.3"\n---\n\n# Colab\n',
    "README.md": f"git -C x checkout --detach {PIN}\n",
    "references/release-history.md": LEDGER,
}

class ReleaseCheckTests(unittest.TestCase):
    def run_check(self, tag=None, **overrides):
        files = {**GOOD, **overrides}
        with patch.object(rc, "read", lambda path: files[path]):
            return rc.check(tag)

    def assertFails(self, needle, **kwargs):
        problems = self.run_check(**kwargs)
        self.assertTrue(any(needle in p for p in problems), problems)

    def test_consistent_release_passes(self):
        self.assertEqual(self.run_check(tag="v4.2.3"), [])

    def test_real_repository_passes(self):
        self.assertEqual(rc.check(), [])

    def test_tag_must_match_version(self):
        self.assertFails("does not match", tag="v4.3.0")

    def test_changelog_must_lead_with_the_version(self):
        self.assertFails("plugin.json says 4.2.2",
                         **{".claude-plugin/plugin.json": json.dumps({"name": "colab-design", "version": "4.2.2"})})
        self.assertFails("newest CHANGELOG entry",
                         **{"CHANGELOG.md": "# Changelog\n\n## 4.2.2 — 2026-09-07\n\nOlder.\n"})

    def test_changelog_order_and_duplicates(self):
        self.assertFails("is not newer", **{"CHANGELOG.md": "## 4.2.3 — 2026-09-24\n\n## 4.3.0 — 2026-09-07\n"})
        self.assertFails("twice", **{"CHANGELOG.md": "## 4.2.3 — 2026-09-24\n\n## 4.2.1 — 2026-09-07\n\n## 4.2.1 — 2026-09-07\n"})
        self.assertFails("dated", **{"CHANGELOG.md": "## 4.2.3 — 2026-09-01\n\n## 4.2.2 — 2026-09-07\n"})

    def test_version_must_be_semver(self):
        self.assertFails("is not X.Y.Z", **{".claude-plugin/plugin.json": json.dumps({"name": "colab-design", "version": "4.2"})})

    def test_skill_frontmatter(self):
        self.assertFails("no frontmatter", **{"SKILL.md": "# Colab\n"})
        self.assertFails("name", **{"SKILL.md": '---\nname: colab\ndescription: "x"\n---\n'})
        self.assertFails("limit 1024", **{"SKILL.md": f'---\nname: colab-design\ndescription: "{"x" * 1025}"\n---\n'})

    def test_skill_version_must_match(self):
        self.assertFails("metadata.version", **{"SKILL.md": '---\nname: colab-design\ndescription: "x"\nmetadata:\n  version: "4.2.2"\n---\n'})

    def test_ledger_must_cover_every_release(self):
        self.assertFails("release-history.md lists", **{"references/release-history.md": LEDGER.replace("4.2.2](x)", "4.2.1](x)")})

    def test_ledger_rows_must_agree(self):
        self.assertFails("CHANGELOG says", **{"references/release-history.md": LEDGER.replace("2026-09-24 |", "2026-09-23 |")})
        self.assertFails("the numbers say patch", **{"references/release-history.md": LEDGER.replace("| patch |", "| minor |")})
        self.assertFails("still pending", **{"references/release-history.md": LEDGER.replace(f"`{SHIPPED}`", "`pending`")})
        self.assertFails("not a full commit", **{"references/release-history.md": LEDGER.replace(SHIPPED, SHIPPED[:7])})
        self.assertFails("not in the history", **{"references/release-history.md": LEDGER.replace(SHIPPED, "1" * 40)})

    def test_pin_must_be_reachable(self):
        self.assertFails("no pinned", **{"README.md": "npx skills add\n"})
        self.assertFails("not a commit", **{"README.md": f"checkout --detach {'0' * 40}\n"})

    def test_notes_extract_one_section(self):
        self.assertEqual(rc.changelog_section(GOOD["CHANGELOG.md"], "4.2.3"), "Patch.")
        self.assertEqual(rc.changelog_section(GOOD["CHANGELOG.md"], "4.2.2"), "Older.")
        self.assertIsNone(rc.changelog_section(GOOD["CHANGELOG.md"], "9.9.9"))

if __name__ == "__main__": unittest.main()
