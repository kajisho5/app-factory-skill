#!/usr/bin/env python3
"""Mechanical checks for SVG mocks (run before the design-check-skill audit).

Checks per SVG:
  - canvas size matches the device in the file name (devices.py)
  - no text smaller than the platform minimum (iOS/iPadOS 11pt, macOS 10pt, watchOS 12pt)
  - text contrast against its background: 4.5:1 under 18pt, 3:1 at 18pt+ or bold (600+)
    Background = nearest ancestor's data-bg, else the root data-bg, else the first
    full-canvas <rect> fill. Put data-bg="#RRGGBB" on a <g> or <text> drawn over
    buttons, cards or images so the check uses the right color.
  - text that probably runs off the canvas (rough width estimate; WARN only)
  - iPhone Duo inner screens drawn partially folded (file name contains "-folded"): text on the
    fold band (centre ±13pt, vertical in landscape, horizontal in portrait). The fold only exists
    when partially folded (zero width when fully open). Mark scrolling text/lists with data-fold-ok
  - <style> blocks (their rules are not checked; WARN only - use attributes instead)
  - every *-light.svg has a *-dark.svg (and vice versa)
  - a PNG exists next to it, is not older than the SVG, and has no alpha channel

Usage: check_mocks.py DIR_OR_FILES...   (exit code 1 if any ERROR)
"""
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from devices import CANVASES, MIN_FONT_PT, canvas_for  # noqa: E402

NAMED = {"white": "#FFFFFF", "black": "#000000"}
FOLD_BAND = 13  # pt either side of the iPhone Duo inner fold (rule of thumb, not an Apple value)


def parse_color(v):
    if not v or v in ("none", "transparent") or v.startswith("url("):
        return None
    v = NAMED.get(v.strip().lower(), v.strip())
    m = re.fullmatch(r"#([0-9a-fA-F]{3}|[0-9a-fA-F]{6})", v)
    if m:
        h = m.group(1)
        if len(h) == 3:
            h = "".join(c * 2 for c in h)
        return tuple(int(h[i:i + 2], 16) / 255 for i in (0, 2, 4))
    m = re.fullmatch(r"rgba?\(([^)]+)\)", v)
    if m:
        p = [float(x) for x in m.group(1).replace("/", ",").split(",")[:3]]
        return tuple(x / 255 for x in p)
    return None


def lum(c):
    def ch(x):
        return x / 12.92 if x <= 0.04045 else ((x + 0.055) / 1.055) ** 2.4
    r, g, b = (ch(x) for x in c)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b


def blend(fg, bg, a):
    return tuple(f * a + b * (1 - a) for f, b in zip(fg, bg))


def ratio(a, b):
    la, lb = sorted((lum(a), lum(b)), reverse=True)
    return (la + 0.05) / (lb + 0.05)


def style_dict(el):
    d = dict(el.attrib)
    for part in el.attrib.get("style", "").split(";"):
        if ":" in part:
            k, v = part.split(":", 1)
            d[k.strip()] = v.strip()
    return d


def local(tag):
    return tag.rsplit("}", 1)[-1]


def check_svg(path: Path, errors, warns):
    name = canvas_for(path.name)
    try:
        root = ET.parse(path).getroot()
    except ET.ParseError as e:
        errors.append(f"{path}: XML parse error: {e}")
        return
    vb = root.get("viewBox")
    if vb:
        _, _, w, h = (float(x) for x in vb.replace(",", " ").split())
    else:
        w, h = float(root.get("width", 0)), float(root.get("height", 0))
    platform = "ios"
    if name:
        cw, ch, _, platform = CANVASES[name]
        if (round(w), round(h)) != (cw, ch):
            errors.append(f"{path}: canvas {w:g}x{h:g} pt, expected {cw}x{ch} for '{name}'")
    elif not path.name.startswith("framed-"):
        warns.append(f"{path}: file name does not start with a device name ({', '.join(CANVASES)}); size not checked")
    min_pt = MIN_FONT_PT[platform]

    if any(local(el.tag) == "style" for el in root.iter()):
        warns.append(f"{path}: <style> rules are not checked (font size, color); write them as attributes")

    page_bg = parse_color(root.get("data-bg"))
    if page_bg is None:
        for el in root.iter():
            if local(el.tag) == "rect":
                s = style_dict(el)
                rw, rh = s.get("width", ""), s.get("height", "")
                full = rw in ("100%", f"{w:g}") and rh in ("100%", f"{h:g}")
                if full and parse_color(s.get("fill")):
                    page_bg = parse_color(s.get("fill"))
                    break
    if page_bg is None:
        page_bg = (1, 1, 1)
        warns.append(f"{path}: no background found (add data-bg on <svg>); assuming white")

    def walk(el, inh):
        s = style_dict(el)
        cur = dict(inh)
        for k in ("fill", "font-size", "font-weight", "opacity", "fill-opacity", "text-anchor"):
            if k in s:
                cur[k] = s[k]
        if "data-bg" in s:
            cur["bg"] = parse_color(s["data-bg"]) or cur["bg"]
        if "data-fold-ok" in s:
            cur["fold_ok"] = True
        if local(el.tag) in ("text", "tspan") and "".join(el.itertext()).strip():
            text = "".join(el.itertext()).strip()[:24]
            fs = cur.get("font-size")
            size = float(re.sub(r"[a-z]+$", "", fs)) if fs else None
            if size is not None and local(el.tag) == "text" and name and el.get("x") and "transform" not in s:
                full = "".join(el.itertext()).strip()
                est = sum(size if ord(ch) > 0x2E7F else size * 0.56 for ch in full)  # rough width
                x = float(re.sub(r"[a-z%]+$", "", el.get("x").split()[0]))
                anchor = cur.get("text-anchor", s.get("text-anchor", "start"))
                left = x - est if anchor == "end" else x - est / 2 if anchor == "middle" else x
                if left < -1 or left + est > w + 1:
                    warns.append(f"{path}: text '{text}' may run off the canvas (estimated width {est:.0f}pt)")
            if size is not None and local(el.tag) == "text" and name and name.startswith("iphone-duo-inner") and "-folded" in path.name \
                    and el.get("x") and el.get("y") and "transform" not in s:
                # Fold band: horizontal across the middle in portrait, vertical in landscape.
                full = "".join(el.itertext()).strip()
                est = sum(size if ord(ch) > 0x2E7F else size * 0.56 for ch in full)
                x = float(re.sub(r"[a-z%]+$", "", el.get("x").split()[0]))
                y = float(re.sub(r"[a-z%]+$", "", el.get("y").split()[0]))
                anchor = cur.get("text-anchor", "start")
                left = x - est if anchor == "end" else x - est / 2 if anchor == "middle" else x
                if h > w:
                    hit = (y - size * 0.85) < h / 2 + FOLD_BAND and y + size * 0.15 > h / 2 - FOLD_BAND
                else:
                    hit = left < w / 2 + FOLD_BAND and left + est > w / 2 - FOLD_BAND
                if hit and "data-fold-ok" not in s and not cur.get("fold_ok"):
                    warns.append(f"{path}: text '{text}' sits on the fold band "
                                 f"(add data-fold-ok on scrolling body text or lists, otherwise move it)")
            if size is not None and size < min_pt:
                errors.append(f"{path}: text '{text}' is {size:g}pt (< {min_pt}pt minimum for {platform})")
            fg = parse_color(cur.get("fill", "#000000"))
            if fg and size and local(el.tag) == "text":
                a = float(cur.get("opacity", 1)) * float(cur.get("fill-opacity", 1))
                fg = blend(fg, cur["bg"], a)
                wt = cur.get("font-weight", "400")
                bold = wt == "bold" or (wt.isdigit() and int(wt) >= 600)
                need = 3.0 if (size >= 18 or bold) else 4.5
                r = ratio(fg, cur["bg"])
                if r < need:
                    errors.append(f"{path}: text '{text}' contrast {r:.2f}:1 < {need}:1 "
                                  f"(set data-bg if it sits on a card/button)")
        for child in el:
            walk(child, cur)

    walk(root, {"bg": page_bg})

    png = path.with_suffix(".png")
    if not png.exists():
        errors.append(f"{path}: PNG preview missing (run export_png.py)")
    else:
        if png.stat().st_mtime + 1 < path.stat().st_mtime:
            errors.append(f"{png}: older than its SVG (re-export)")
        try:
            from PIL import Image
            with Image.open(png) as im:
                if im.mode in ("RGBA", "LA") or "transparency" in im.info:
                    errors.append(f"{png}: has an alpha channel (App Store screenshots must be opaque)")
        except ImportError:
            warns.append("pillow not installed; PNG alpha not checked")


def main():
    files = []
    for p in map(Path, sys.argv[1:] or ["design/mocks"]):
        files += sorted(p.rglob("*.svg")) if p.is_dir() else [p]
    if not files:
        sys.exit("no SVG files found")
    errors, warns = [], []
    names = {f.name for f in files}
    for f in files:
        check_svg(f, errors, warns)
        for a, b in (("-light.svg", "-dark.svg"), ("-dark.svg", "-light.svg")):
            if f.name.endswith(a) and f.name[: -len(a)] + b not in names:
                errors.append(f"{f}: missing pair {f.name[: -len(a)] + b}")
    for w in warns:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"checked {len(files)} SVG(s): {len(errors)} error(s), {len(warns)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
