"""references/approved-inspirations.md keeps its three states honest: sourced, dated, pointed, disjoint."""
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).parents[1]
LEDGER = ROOT / "references/approved-inspirations.md"
DATE = re.compile(r"\b\d{4}-\d{2}-\d{2}\b")
URL = re.compile(r"https?://\S+")

def section(text, heading):
    """Table rows (as cell lists) under `## heading`, header and divider rows dropped."""
    body = text.split(f"\n## {heading}\n", 1)[1].split("\n## ", 1)[0]
    rows = [l for l in body.splitlines() if l.startswith("|")]
    return [[c.strip() for c in r.strip("|").split("|")] for r in rows[2:]]

def idea_key(cells):
    return cells[0].split("—")[0].split(",")[0].strip().lower()

class LedgerTests(unittest.TestCase):
    text = LEDGER.read_text()

    def test_three_states_exist(self):
        for heading in ("Approved", "Held", "Rejected"):
            with self.subTest(state=heading):
                self.assertIn(f"\n## {heading}\n", self.text)

    def test_every_idea_is_sourced_and_dated(self):
        for heading in ("Approved", "Held", "Rejected"):
            for cells in section(self.text, heading):
                row = " | ".join(cells)
                with self.subTest(state=heading, idea=cells[0][:40]):
                    self.assertRegex(row, URL)
                    self.assertRegex(row, DATE)

    def test_approved_rules_point_at_a_real_file(self):
        rows = section(self.text, "Approved")
        self.assertTrue(rows, "an Approved table with at least one row")
        for cells in rows:
            targets = re.findall(r"`(references/[\w.-]+\.md)`", cells[1])
            with self.subTest(idea=cells[0][:40]):
                self.assertTrue(targets, "the rule names where it lives")
                for target in targets:
                    self.assertTrue((ROOT / target).exists(), target)

    def test_states_are_disjoint(self):
        seen = {}
        for heading in ("Approved", "Held", "Rejected"):
            for cells in section(self.text, heading):
                key = idea_key(cells)
                with self.subTest(idea=key):
                    self.assertNotIn(key, seen, f"{key} is both {seen.get(key)} and {heading}")
                seen[key] = heading

    def test_nothing_is_rejected_by_default(self):
        """Rejection is explicit: a rejected row must say who rejected it."""
        for cells in section(self.text, "Rejected"):
            with self.subTest(idea=cells[0][:40]):
                self.assertRegex(" ".join(cells), r"(?i)rejected by")

if __name__ == "__main__": unittest.main()
