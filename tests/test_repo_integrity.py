"""The published skill agrees with itself: links resolve, counts match, assets are inert."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch
import xml.etree.ElementTree as ET

ROOT = Path(__file__).parents[1]
DOCS = sorted([*ROOT.glob("*.md"), *ROOT.glob("references/**/*.md")])
SVGS = sorted(ROOT.glob("assets/**/*.svg"))

def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

class DocumentationTests(unittest.TestCase):
    def test_relative_links_resolve(self):
        for doc in DOCS:
            for target in re.findall(r"\]\(([^)#\s]+)(?:#[^)]*)?\)", doc.read_text()):
                if target.startswith(("http://", "https://", "mailto:")): continue
                with self.subTest(doc=doc.name, target=target):
                    self.assertTrue((doc.parent / target).exists())

    def test_backticked_repo_paths_exist(self):
        for doc in DOCS:
            for path in re.findall(r"`((?:references|assets|scripts|tests)/[^`\s]+)`", doc.read_text()):
                if "<" in path or "*" in path: continue  # a naming pattern, not a file
                with self.subTest(doc=doc.name, path=path):
                    self.assertTrue((ROOT / path.rstrip("/")).exists())

    def test_readme_counts_match_disk(self):
        readme = (ROOT / "README.md").read_text()
        counts = {"logo": len(list(ROOT.glob("assets/logo/*.svg"))),
                  "shapes": len(list(ROOT.glob("assets/shapes/*.svg"))),
                  "icons/stroke-rounded": len(list(ROOT.glob("assets/icons/stroke-rounded/*.svg")))}
        for folder, n in counts.items():
            with self.subTest(folder=folder):
                self.assertRegex(readme, rf"\n  {re.escape(folder)}/\s+{n:,} ")
        for doc in (ROOT / "README.md", ROOT / "SKILL.md"):
            for claimed in re.findall(r"([\d,]{4,}) (?:Hugeicons SVGs|MIT-licensed SVGs|icons are vendored|vendored SVGs)", doc.read_text()):
                with self.subTest(doc=doc.name, claimed=claimed):
                    self.assertEqual(int(claimed.replace(",", "")), counts["icons/stroke-rounded"])

    def test_icon_index_is_regenerated(self):
        index = load("rebuild-icon-index")
        with tempfile.TemporaryDirectory() as out:
            shards = Path(out) / "icon-index"
            with patch.object(index, "REFS", out), patch.object(index, "SHARDS", str(shards)), \
                 contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(index.main(), 0)
            self.assertEqual((Path(out) / "icon-index.md").read_text(), (ROOT / "references/icon-index.md").read_text())
            built = {p.name: p.read_text() for p in shards.glob("*.md")}
            committed = {p.name: p.read_text() for p in (ROOT / "references/icon-index").glob("*.md")}
            self.assertEqual(sorted(built), sorted(committed))
            for name in built:
                with self.subTest(shard=name): self.assertEqual(built[name], committed[name])

class AssetTests(unittest.TestCase):
    def test_svgs_parse_and_are_inert(self):
        active = re.compile(r"<script|<foreignObject|\son[a-z]+\s*=|javascript:|(?:xlink:)?href\s*=\s*[\"'](?!#)", re.I)
        for svg in SVGS:
            text = svg.read_text()
            with self.subTest(svg=str(svg.relative_to(ROOT))):
                self.assertNotRegex(text, r"<!(?:DOCTYPE|ENTITY)")  # checked before parsing: no entity expansion
                self.assertTrue(ET.fromstring(text).tag.endswith("svg"))
                self.assertIsNone(active.search(text))

    def test_export_manifest_matches_files(self):
        manifest = json.loads((ROOT / "assets/figma-export-manifest.json").read_text())
        exported = sorted(p.relative_to(ROOT).as_posix() for p in [*ROOT.glob("assets/logo/*.svg"), *ROOT.glob("assets/shapes/*.svg")])
        self.assertEqual(sorted(e["path"] for e in manifest), exported)
        for entry in manifest:
            data = (ROOT / entry["path"]).read_bytes()
            text = data.decode()
            colours = {h.upper() for h in re.findall(r"#[0-9A-Fa-f]{6}\b", text)}
            root = ET.fromstring(text)
            with self.subTest(path=entry["path"]):
                self.assertEqual(len(data), entry["bytes"])
                self.assertEqual(colours, {h.upper() for h in entry["hexes"]})
                # the manifest records the Figma node size; the export rounds to whole pixels
                self.assertLessEqual(abs(float(root.get("width")) - entry["w"]), 1)
                self.assertLessEqual(abs(float(root.get("height")) - entry["h"]), 1)

    def test_icon_licence_and_pin_ship_with_icons(self):
        self.assertIn("MIT", (ROOT / "assets/icons/LICENSE").read_text())
        self.assertRegex((ROOT / "assets/icons/VERSION").read_text().strip(), r"^@hugeicons/core-free-icons@\d+\.\d+\.\d+$")

def contrast(a, b):
    def luminance(hex_colour):
        rgb = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        r, g, b = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)

class ContrastTests(unittest.TestCase):
    GROUNDS = ("#FFFFFF", "#103A21", "#011E14")  # the verified table's columns: White, Pine, Deep Jade

    def test_verified_table_is_computed(self):
        colours = (ROOT / "references/colors.md").read_text()
        table = colours.split("**Verified — all computed:**", 1)[1].split("\n\n", 2)[1]
        rows = 0
        for line in table.splitlines()[2:]:
            cells = [c.strip() for c in line.strip("|").split("|")]
            found = re.search(r"#[0-9A-Fa-f]{6}", cells[0])
            fg = found.group(0) if found else "#FFFFFF" if cells[0] == "White" else None
            self.assertIsNotNone(fg, line)
            for ground, cell in zip(self.GROUNDS, cells[1:]):
                claimed = re.search(r"\d+\.\d+", cell)
                if not claimed: continue
                rows += 1
                with self.subTest(fg=fg, ground=ground):
                    self.assertAlmostEqual(float(claimed.group(0)), contrast(fg, ground), delta=0.01)
        self.assertGreater(rows, 20)

    def test_quoted_pair_ratios(self):
        """Every `#AAAAAA` on `#BBBBBB` ... N.NN claim in the docs is the computed ratio."""
        pair = re.compile(r"`(#[0-9A-Fa-f]{6})`[^|\n]{0,40}? on [^|\n]{0,40}?`(#[0-9A-Fa-f]{6})`[^|\n]*?\|\s*\**(\d+\.\d\d)")
        for doc in [ROOT / "SKILL.md", *sorted(ROOT.glob("references/*.md"))]:
            for fg, bg, claimed in pair.findall(doc.read_text()):
                with self.subTest(doc=doc.name, pair=f"{fg} on {bg}"):
                    self.assertAlmostEqual(float(claimed), contrast(fg, bg), delta=0.01)

    def test_text_on_electric_flood_ratios(self):
        """Lines about text on an Electric Green flood quote each ground's own ratio against #34FF67."""
        named = {"deep jade": "#011E14", "pine": "#103A21", "pine green": "#103A21", "white": "#FFFFFF"}
        claim = re.compile(r"\b(Deep Jade|Pine Green|Pine|white)\**[^()\n]{0,12}\((\d+\.\d\d)\s?:\s?1\)", re.I)
        checked = 0
        for doc in [ROOT / "SKILL.md", ROOT / "EXAMPLES.md", *sorted(ROOT.glob("references/*.md"))]:
            for line in doc.read_text().splitlines():
                if "Electric" not in line or not re.search(r"flood|badge|fill", line, re.I): continue
                for name, ratio in claim.findall(line):
                    checked += 1
                    with self.subTest(doc=doc.name, ground=name):
                        self.assertAlmostEqual(float(ratio), contrast(named[name.lower()], "#34FF67"), delta=0.01)
        self.assertGreater(checked, 3)

class SecretTests(unittest.TestCase):
    PATTERNS = {
        "private key": r"-----BEGIN [A-Z ]*PRIVATE KEY-----",
        "GitHub token": r"\bgh[pousr]_[A-Za-z0-9]{36,}\b|\bgithub_pat_[A-Za-z0-9_]{40,}\b",
        "Figma token": r"\bfigd_[A-Za-z0-9_-]{20,}\b",
        "AWS key": r"\bAKIA[0-9A-Z]{16}\b",
        "npm token": r"\bnpm_[A-Za-z0-9]{36}\b",
        "Anthropic key": r"\bsk-ant-[A-Za-z0-9_-]{20,}\b",
    }

    def test_no_credentials_in_text_files(self):
        skip = {".git", "icons"}
        files = [p for p in ROOT.rglob("*") if p.is_file() and not skip & set(p.relative_to(ROOT).parts)
                 and p.suffix in {".md", ".py", ".json", ".yml", ".yaml", ".svg", ".txt", ""}]
        for path in files:
            text = path.read_text(errors="ignore")
            for label, pattern in self.PATTERNS.items():
                with self.subTest(path=str(path.relative_to(ROOT)), kind=label):
                    self.assertIsNone(re.search(pattern, text))

if __name__ == "__main__": unittest.main()
