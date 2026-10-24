#!/usr/bin/env python3
"""Export SVG mocks to opaque PNG previews.

Screen mocks named after a canvas in devices.py (e.g. iphone-S-01-light.svg) are exported
at that canvas's scale, so the PNG matches the App Store screenshot size. Other SVGs
(framed compositions, Duo) are exported at --scale (default 2).
PNGs are flattened onto an opaque background because App Store screenshots must not
contain transparency.

Usage: export_png.py FILE_OR_DIR [...] [--scale 2] [--bg "#FFFFFF"]
Requires: pip install cairosvg pillow
"""
import argparse
import io
import re
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from devices import CANVASES, canvas_for  # noqa: E402

try:
    import cairosvg
    from PIL import Image
except ImportError:
    sys.exit("missing dependency: pip install cairosvg pillow")


_FAMILIES = {}


def families(lang=None):
    """Font families known to fontconfig, optionally only those covering a language."""
    if lang not in _FAMILIES:
        pattern = f":lang={lang}" if lang else ":"
        try:
            out = subprocess.run(["fc-list", pattern, "family"], capture_output=True, text=True).stdout
            _FAMILIES[lang] = {f.strip().lower() for line in out.splitlines() for f in line.split(",")}
        except FileNotFoundError:
            _FAMILIES[lang] = set()
    return _FAMILIES[lang]


CJK = re.compile(r"[\u3040-\u30ff\u3400-\u9fff\uff00-\uffef]")


def resolve_fonts(svg_text: str) -> str:
    """Cairo uses only the first family of a font-family list and does not fall back per
    glyph, so each list is replaced with the first installed family (for documents with
    Japanese text: the first installed family that covers Japanese, e.g. Hiragino Sans on
    a Mac, Noto Sans CJK JP on Linux). Only the render input changes; the SVG keeps its stack."""
    pool = families("ja") if CJK.search(svg_text) else families()
    if not pool:
        return svg_text

    def pick(m):
        quote, value = m.group(1), m.group(2)
        for f in value.split(","):
            f = f.strip().strip("'\"")
            if f.lower() in pool:
                return f"font-family={quote}{f}{quote}"
        return m.group(0)

    return re.sub(r"font-family=(['\"])(.*?)\1", pick, svg_text)


def export(svg: Path, default_scale: float, bg: str):
    name = canvas_for(svg.name)
    scale = CANVASES[name][2] if name and name != "pair" else default_scale
    src = resolve_fonts(svg.read_text(encoding="utf-8"))
    png_bytes = cairosvg.svg2png(bytestring=src.encode("utf-8"), scale=scale)
    img = Image.open(io.BytesIO(png_bytes)).convert("RGBA")
    flat = Image.new("RGB", img.size, bg)
    flat.paste(img, mask=img.split()[3])
    out = svg.with_suffix(".png")
    flat.save(out, optimize=True)
    note = ""
    if name and name != "pair":
        w, h, s, _ = CANVASES[name]
        expected = (round(w * s), round(h * s))
        note = "OK" if flat.size == expected else f"SIZE MISMATCH (expected {expected[0]}x{expected[1]})"
    print(f"{out}  {flat.size[0]}x{flat.size[1]}  @{scale:g}x  {note}")
    return "MISMATCH" not in note


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("paths", nargs="+")
    ap.add_argument("--scale", type=float, default=2)
    ap.add_argument("--bg", default="#FFFFFF", help="color behind transparent areas")
    a = ap.parse_args()
    files = []
    for p in map(Path, a.paths):
        files += sorted(p.rglob("*.svg")) if p.is_dir() else [p]
    if not files:
        sys.exit("no SVG files found")
    ok = all([export(f, a.scale, a.bg) for f in files])
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
