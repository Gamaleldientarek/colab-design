"""The design tokens agree with the docs, and the generated css/js match a fresh build."""
import importlib.util
import json
from pathlib import Path
import re
import unittest

ROOT = Path(__file__).parents[1]
TOKENS = json.loads((ROOT / "assets/tokens/tokens.json").read_text())
SKILL = (ROOT / "SKILL.md").read_text()
COLORS = (ROOT / "references/colors.md").read_text()
SYSTEM = (ROOT / "references/token-system.md").read_text()
MODES = TOKENS["ground"]["$modes"]
BANNED_ON_LIGHT = {"#34FF67": "Electric Green", "#33FFC2": "Jade Green"}

def load(name):
    spec = importlib.util.spec_from_file_location(name.replace("-", "_"), ROOT / "scripts" / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def children(group): return [(k, v) for k, v in group.items() if not k.startswith("$")]

def section(text, heading):
    """Body of the markdown section whose heading starts with `heading`, up to the next heading of its level or above."""
    level, body = re.split(rf"^(#+) {re.escape(heading)}.*$", text, maxsplit=1, flags=re.M)[1:]
    return re.split(rf"^#{{1,{len(level)}}} ", body, maxsplit=1, flags=re.M)[0]

def row(text, label):
    """Cells of the first table row whose first cell is `label`, stars stripped."""
    for line in text.splitlines():
        cells = [c.strip().strip("*") for c in line.strip().strip("|").split("|")]
        if line.startswith("|") and cells[0] == label: return cells[1:]
    raise AssertionError(f"no table row {label!r}")

def doc_colour(cell):
    """'`#34FF67`' -> '#34FF67'; 'white @10%' -> {'color': '#FFFFFF', 'alpha': 0.1}."""
    found = re.search(r"#[0-9A-Fa-f]{6}", cell)
    if found: return found.group(0).upper()
    alpha = re.fullmatch(r"white @(\d+)%", cell)
    if alpha: return {"color": "#FFFFFF", "alpha": int(alpha.group(1)) / 100}
    raise AssertionError(f"unreadable colour cell {cell!r}")

def contrast(a, b):
    def luminance(hex_colour):
        rgb = [int(hex_colour[i:i + 2], 16) / 255 for i in (1, 3, 5)]
        r, g, b = [c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4 for c in rgb]
        return 0.2126 * r + 0.7152 * g + 0.0722 * b
    hi, lo = sorted((luminance(a), luminance(b)), reverse=True)
    return (hi + 0.05) / (lo + 0.05)

def ref(path): return TOKENS if not path else ref(path[:-1])[path[-1]]
def resolve(alias): return ref(alias.strip("{}").split("."))["$value"]

class BuildTests(unittest.TestCase):
    def test_generated_files_match_a_fresh_build(self):
        for name, text in load("build-tokens").build(TOKENS).items():
            with self.subTest(file=name):
                committed = (ROOT / "assets/tokens" / name).read_bytes()
                self.assertEqual(committed, text.encode("utf-8"), f"run python3 scripts/build-tokens.py")
                self.assertIn("Generated, do not edit", text.splitlines()[0])

    def test_every_token_has_a_source(self):
        def walk(node, path, sourced):
            sourced = sourced or "$source" in node
            for name, child in children(node):
                if "$value" in child:
                    with self.subTest(token=".".join(path + [name])): self.assertTrue(sourced)
                else: walk(child, path + [name], sourced)
            for s in node.get("$source", []):
                with self.subTest(source=s["file"]): self.assertTrue((ROOT / s["file"]).exists())
        walk(TOKENS, [], False)

class PaletteTests(unittest.TestCase):
    def test_palette_matches_skill(self):
        palette = section(SKILL, "Palette")
        documented = {name: hexv.upper() for name, hexv in re.findall(r"^\| \*\*([^*]+)\*\* \| `(#[0-9A-Fa-f]{6})`", palette, re.M)}
        tokens = {name.replace("-", " ").title(): t["$value"] for tier in ("primary", "secondary") for name, t in children(TOKENS["color"][tier])}
        self.assertEqual(len(documented), 8)
        self.assertEqual(tokens, documented)

    def test_ramps_match_colors_md(self):
        for hue, ramp in children(TOKENS["color"]["ramp"]):
            table = section(COLORS, hue.replace("-", " ").title())
            documented = {s.strip(" *⭐️\\").lower().replace(" ", "-"): h for s, h in re.findall(r"^\| \**([^|]+?)\** \| \**`(#[0-9A-F]{6})`", table, re.M)}
            with self.subTest(hue=hue):
                self.assertEqual({step: t["$value"] for step, t in children(ramp)}, documented)

    def test_on_ground_variants_match_colors_md(self):
        for name, label in (("olive-green-on-dark", "Olive Green `/onDark`"), ("pale-sky-blue-on-light", "Pale Sky Blue `/onLight`")):
            documented = re.search(rf"\| {re.escape(label)} `(#[0-9A-F]{{6}})`", COLORS).group(1)
            with self.subTest(variant=name): self.assertEqual(TOKENS["color"]["variant"][name]["$value"], documented)

class TypeTests(unittest.TestCase):
    TYPO = TOKENS["typography"]

    def test_scales_match_skill(self):
        for scale in ("Display", "Body"):
            documented = [int(c) for c in row(SKILL, scale)]
            with self.subTest(scale=scale):
                self.assertEqual([t["$value"] for _, t in children(self.TYPO[scale.lower()])], documented)
        pending = [s for s, t in children(self.TYPO["display"]) if t.get("status") == "pending-figma"]
        self.assertEqual(pending, ["280", "120"])

    def test_leading_follows_the_documented_rule(self):
        display = re.search(r"×(\d\.\d+) at ≥(\d+)px · ×(\d\.\d+) below", SKILL).groups()
        large, threshold, small = float(display[0]), int(display[1]), float(display[2])
        body = float(re.search(r"\*\*×(\d\.\d+) throughout\*\*", SKILL).group(1))
        arabic = float(re.search(r"\*\*×(\d\.\d+)\*\* at every size", SKILL).group(1))
        for size, t in children(self.TYPO["display"]):
            with self.subTest(display=size): self.assertEqual(resolve(t["leading"]), large if int(size) >= threshold else small)
        for size, t in children(self.TYPO["body"]):
            with self.subTest(body=size): self.assertEqual(resolve(t["leading"]), body)
        self.assertEqual(self.TYPO["leading"]["ar"]["$value"], arabic)
        self.assertEqual(self.TYPO["tracking"]["ar"]["$value"], 0)

    def test_families_are_inter_and_alexandria(self):
        for role, t in children(self.TYPO["family"]):
            with self.subTest(role=role): self.assertEqual(t["$value"], {"en": "Inter", "ar": "Alexandria"})

class GridTests(unittest.TestCase):
    def test_slide_columns_match_skill(self):
        starts = [int(c) for c in row(section(SKILL, "Grid"), "x start")]
        self.assertEqual([t["$value"] for _, t in children(TOKENS["grid"]["column-x"])], starts)

    def test_poster_columns_match_poster_doc(self):
        starts = [int(c) for c in row((ROOT / "references/pixel-dither-posters.md").read_text(), "x start")]
        self.assertEqual([t["$value"] for _, t in children(TOKENS["poster"]["column-x"])], starts)

class GroundTests(unittest.TestCase):
    GROUND = TOKENS["ground"]

    def test_semantic_values_match_token_system(self):
        """Every mode value in tokens.json is the value token-system.md §5 tabulates."""
        checked = 0
        for group, roles in children(self.GROUND):
            for name, t in children(roles):
                cells = row(SYSTEM, f"`{group}/{name}`")
                colours = [c for c in cells if not re.fullmatch(r"[\d.]+|—|", c)]
                with self.subTest(role=f"{group}/{name}"):
                    self.assertEqual(len(colours), 4)
                    self.assertEqual([t["$value"][m] for m in MODES], [doc_colour(c) for c in colours])
                checked += 1
        self.assertGreater(checked, 20)

    def test_text_contrast_is_what_the_docs_claim(self):
        text = self.GROUND["text"]
        for name, t in children(text):
            cells = row(SYSTEM, f"`text/{name}`")
            for i, mode in enumerate(MODES):
                claimed = cells[2 * i + 1]
                if not re.fullmatch(r"\d+\.\d+", claimed): continue
                ratio = contrast(t["$value"][mode], self.GROUND["surface"]["page"]["$value"][mode])
                with self.subTest(role=f"text/{name}", mode=mode):
                    self.assertAlmostEqual(ratio, float(claimed), delta=0.01)
                    if name in ("primary", "secondary", "muted", "accent"):
                        self.assertGreaterEqual(ratio, 4.5)

    def test_accent_content_reads_on_accent_fill(self):
        accent = self.GROUND["accent"]
        for mode in MODES:
            with self.subTest(mode=mode):
                self.assertGreaterEqual(contrast(accent["content"]["$value"][mode], accent["default"]["$value"][mode]), 4.5)

    def test_no_electric_or_jade_foreground_on_light(self):
        # accent/default and accent/hover are fills, not text, icon or rule colours. token-system.md
        # §5.4 documents Electric there on Light and §14 says the shape then needs border/accent.
        fills = {"accent/default", "accent/hover"}
        for group, roles in children(self.GROUND):
            for name, t in children(roles):
                if f"{group}/{name}" in fills: continue
                value = t["$value"]["light"]
                with self.subTest(role=f"{group}/{name}"):
                    self.assertNotIn(value if isinstance(value, str) else value["color"], BANNED_ON_LIGHT)

if __name__ == "__main__": unittest.main()
