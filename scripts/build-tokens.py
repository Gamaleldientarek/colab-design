#!/usr/bin/env python3
"""Generate the web tokens from the single source file, assets/tokens/tokens.json.

Usage:
    python3 scripts/build-tokens.py           # write tokens.css and tokens.js
    python3 scripts/build-tokens.py --check   # exit 1 if either file differs from a fresh build

Outputs, both beside tokens.json and both marked "generated, do not edit":

- tokens.css  CSS custom properties. Primitives, type, grid, motif and poster on :root;
              one [data-ground="light|jade|dark|electric"] block per mode for the
              semantic roles (Light also on :root, so a page without the attribute
              reads as Light); a :lang(ar) block that swaps the families and pins
              every leading to the AR value and every tracking to 0.
- tokens.js   An ES module exporting the same values as plain data.

Output is deterministic: it follows the key order of tokens.json and nothing else.
No dependencies beyond the standard library.
"""
import argparse
import json
import os
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TOKENS = os.path.join(ROOT, "assets", "tokens")
SOURCE = os.path.join(TOKENS, "tokens.json")
HEADER = "Colab design tokens: generated from assets/tokens/tokens.json by scripts/build-tokens.py. Generated, do not edit."
FALLBACK = {"Inter": "sans-serif", "Alexandria": "sans-serif"}


def load(path=SOURCE):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def children(group):
    """(name, node) for every non-$ key, in file order."""
    return [(k, v) for k, v in group.items() if not k.startswith("$")]


def is_token(node):
    return isinstance(node, dict) and "$value" in node


def lookup(tokens, ref):
    """'{typography.leading.body}' -> that token."""
    node = tokens
    for part in ref.strip("{}").split("."):
        node = node[part]
    return node


# ---- value formatting -------------------------------------------------------

def num(v):
    return f"{round(v, 6):g}"


def css_color(v):
    if isinstance(v, dict):  # {"color": "#FFFFFF", "alpha": 0.1}
        h = v["color"]
        r, g, b = (int(h[i:i + 2], 16) for i in (1, 3, 5))
        return f"rgb({r} {g} {b} / {num(v['alpha'])})"
    return v


def css_family(name):
    return f'"{name}", {FALLBACK.get(name, "sans-serif")}'


def em(percent):
    return f"{num(percent / 100)}em"


def css_value(token, path):
    kind, v = token["$type"], token["$value"]
    if kind == "color":
        return css_color(v)
    if kind == "dimension":
        return f"{num(v)}px"
    if kind == "number" and path[:2] == ["typography", "tracking"]:
        return em(v)
    return num(v) if isinstance(v, (int, float)) else str(v)


# ---- CSS -------------------------------------------------------------------

def color_vars(tokens):
    out = []
    for group, node in children(tokens["color"]):
        if group == "ramp":
            for hue, ramp in children(node):
                out += [(f"--colab-color-{hue}-{step}", css_color(t["$value"])) for step, t in children(ramp)]
        else:
            out += [(f"--colab-color-{name}", css_color(t["$value"])) for name, t in children(node)]
    return out


def constant_vars(tokens):
    return [(f"--colab-{group}-{name}", css_color(t["$value"]))
            for group, node in children(tokens["constant"]) for name, t in children(node)]


def ground_vars(tokens, mode):
    return [(f"--colab-{group}-{name}", css_color(t["$value"][mode]))
            for group, node in children(tokens["ground"]) for name, t in children(node)]


def type_vars(tokens, lang):
    """Typography custom properties for one language ('en' or 'ar')."""
    typo = tokens["typography"]
    ar = lang == "ar"
    out = [(f"--colab-font-{name}", css_family(t["$value"][lang])) for name, t in children(typo["family"])]
    if not ar:
        out += [(f"--colab-font-weight-{name}", num(t["$value"])) for name, t in children(typo["weight"])]
    ar_leading = num(typo["leading"]["ar"]["$value"])
    ar_tracking = em(typo["tracking"]["ar"]["$value"])
    out += [(f"--colab-leading-{name}", ar_leading if ar else num(t["$value"]))
            for name, t in children(typo["leading"]) if name != "ar"]
    out += [(f"--colab-tracking-{name}", ar_tracking if ar else em(t["$value"]))
            for name, t in children(typo["tracking"]) if name != "ar"]
    for scale in ("display", "body", "caps"):
        for size, t in children(typo[scale]):
            base = f"--colab-{scale}-{size}"
            if not ar:
                out.append((base, f"{num(t['$value'])}px"))
            if "leading" in t:
                out.append((f"{base}-leading", ar_leading if ar else num(lookup(tokens, t["leading"])["$value"])))
            if "tracking" in t:
                out.append((f"{base}-tracking", ar_tracking if ar else em(lookup(tokens, t["tracking"])["$value"])))
    return out


def flat_vars(tokens, group, prefix):
    out = []

    def walk(node, path):
        for name, child in children(node):
            if is_token(child):
                out.append((f"--colab-{prefix}-{'-'.join(path + [name])}", css_value(child, [group] + path + [name])))
            else:
                walk(child, path + [name])
    walk(tokens[group], [])
    return out


def block(selector, pairs, comment=None):
    names = [n for n, _ in pairs]
    dupes = sorted({n for n in names if names.count(n) > 1})
    if dupes:
        raise ValueError(f"duplicate custom properties in {selector}: {dupes}")
    lines = [f"/* {comment} */"] if comment else []
    lines.append(selector + " {")
    lines += [f"  {n}: {v};" for n, v in pairs]
    lines.append("}")
    return "\n".join(lines)


def build_css(tokens):
    root = (color_vars(tokens) + constant_vars(tokens) + type_vars(tokens, "en")
            + flat_vars(tokens, "grid", "grid") + flat_vars(tokens, "motif", "motif")
            + flat_vars(tokens, "poster", "poster"))
    parts = [f"/* {HEADER} */", block(":root", root, "Primitives, constants, type (EN), grid, motif, poster")]
    for mode in tokens["ground"]["$modes"]:
        selector = f'[data-ground="{mode}"]'
        if mode == "light":
            selector = ":root,\n" + selector
        parts.append(block(selector, ground_vars(tokens, mode), f"Ground: {mode}"))
    parts.append(block(":lang(ar)", type_vars(tokens, "ar"), "Arabic: Alexandria, leading x1.5, tracking 0. Sizes do not change"))
    return "\n\n".join(parts) + "\n"


# ---- JS --------------------------------------------------------------------

def js_tree(tokens, node, path):
    out = {}
    for name, child in children(node):
        if not is_token(child):
            out[name] = js_tree(tokens, child, path + [name])
            continue
        v = child["$value"]
        if child["$type"] == "color":
            v = css_color(v)
        extras = {k: child[k] for k in child if not k.startswith("$")}
        if extras:
            entry = {"size" if child["$type"] == "dimension" else "value": v}
            for k, ref in extras.items():
                entry[k] = lookup(tokens, ref)["$value"] if isinstance(ref, str) and ref.startswith("{") else ref
            v = entry
        out[name] = v
    return out


def build_js(tokens):
    data = {}
    for group, node in children(tokens):
        if group == "ground":
            modes = node["$modes"]
            data["ground"] = {"modes": modes}
            for mode in modes:
                data["ground"][mode] = {g: {n: css_color(t["$value"][mode]) for n, t in children(roles)}
                                         for g, roles in children(node)}
        else:
            data[group] = js_tree(tokens, node, [group])
    body = json.dumps(data, indent=2, ensure_ascii=False)
    note = ("Tracking values are % of the font size (divide by 100 for em). "
            "Leading is a unitless multiple. In Arabic use typography.leading.ar and typography.tracking.ar at every size.")
    return f"// {HEADER}\n// {note}\nexport const tokens = {body};\n\nexport default tokens;\n"


def build(tokens=None):
    tokens = tokens or load()
    return {"tokens.css": build_css(tokens), "tokens.js": build_js(tokens)}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    parser.add_argument("--check", action="store_true", help="fail if the committed files differ from a fresh build")
    args = parser.parse_args(argv)
    stale = []
    for name, text in build().items():
        path = os.path.join(TOKENS, name)
        if args.check:
            try:
                with open(path, encoding="utf-8") as fh:
                    current = fh.read()
            except FileNotFoundError:
                current = None
            if current != text:
                stale.append(name)
        else:
            with open(path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write(text)
            print(f"wrote assets/tokens/{name}")
    for name in stale:
        print(f"FAIL  assets/tokens/{name} is stale; run python3 scripts/build-tokens.py", file=sys.stderr)
    return 1 if stale else 0


if __name__ == "__main__":
    sys.exit(main())
