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
  - iPhone Duo inner screens drawn partially folded (file name contains "-folded"): text,
    small shapes (buttons, <=60pt) touching the band and larger shapes crossing the fold line are
    errors on the fold band (centre ±13pt, vertical in landscape, horizontal in portrait). The fold only exists
    when partially folded (zero width when fully open). Mark scrolling text/lists with data-fold-ok
  - <style> blocks (their rules are not checked; WARN only - use attributes instead)
  - text inside a semi-transparent rect: data-bg must be the composite colour
  - (warning) text whose estimated box overlaps other text or touches a small button/marker
    (mark a floating bar that scrolling content passes under with data-overlap-ok)
  - every *-light.svg has a *-dark.svg (and vice versa), and the dark one really is different
    (not a byte copy, not the same root background)
  - a PNG exists next to it, is not older than the SVG, has no alpha channel and has a color profile

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

    folded = bool(name and name.startswith("iphone-duo-inner") and "-folded" in path.name)
    tints = []  # filled rects/circles drawn so far: (x, y, w, h, colour, alpha)
    text_boxes = []   # (x, y, w, h, label) estimated
    small_shapes = []  # buttons and markers (<= 200 x 60pt): (x, y, w, h)

    def num(v):
        try:
            return float(re.sub(r"[a-z%]+$", "", str(v).split()[0]))
        except (ValueError, IndexError):
            return None

    def shape_box(el, s):
        tag = local(el.tag)
        if tag == "rect":
            x, y, rw, rh = (num(s.get(k, 0)) for k in ("x", "y", "width", "height"))
            if None in (x, y, rw, rh):
                return None
            return x, y, rw, rh
        if tag == "circle":
            cx, cy, r = (num(s.get(k, 0)) for k in ("cx", "cy", "r"))
            if None in (cx, cy, r):
                return None
            return cx - r, cy - r, 2 * r, 2 * r
        return None

    def walk(el, inh):
        s = style_dict(el)
        cur = dict(inh)
        if "transform" in s:
            cur["xf"] = True
        for k in ("fill", "font-size", "font-weight", "opacity", "fill-opacity", "text-anchor"):
            if k in s:
                cur[k] = s[k]
        if "data-bg" in s:
            cur["bg"] = parse_color(s["data-bg"]) or cur["bg"]
        if "data-fold-ok" in s:
            cur["fold_ok"] = True
        if "data-overlap-ok" in s:
            cur["overlap_ok"] = True  # e.g. scrolling content passing under a floating bar
        box = shape_box(el, s) if not cur.get("xf") else None
        if box and not (box[2] >= w - 1 and box[3] >= h - 1):
            fc = parse_color(s.get("fill", cur.get("fill")))
            a = float(s.get("fill-opacity", 1)) * float(s.get("opacity", 1))
            if fc:
                tints.append((*box, fc, a))  # every filled shape, in drawing order
            if (box[2] <= 200 and box[3] <= 60 and min(box[2], box[3]) >= 4 and local(el.tag) in ("rect", "circle")
                    and not cur.get("overlap_ok")):
                small_shapes.append(box)
            if folded and not cur.get("fold_ok"):
                bx, by, bw, bh = box
                small = bw <= 60 and bh <= 60
                if h > w:
                    lo, hi, c = by, by + bh, h / 2
                else:
                    lo, hi, c = bx, bx + bw, w / 2
                hit = (lo < c + FOLD_BAND and hi > c - FOLD_BAND) if small else (lo < c < hi)
                if hit:
                    errors.append(f"{path}: {local(el.tag)} at ({bx:g},{by:g}) {bw:g}x{bh:g} sits on the fold band "
                                  f"(move buttons, images and cards off the fold; mark scrolling lists data-fold-ok)")
        if local(el.tag) in ("text", "tspan") and "".join(el.itertext()).strip():
            text = "".join(el.itertext()).strip()[:24]
            fs = cur.get("font-size")
            size = float(re.sub(r"[a-z]+$", "", fs)) if fs else None
            if size is not None and local(el.tag) == "text" and name and el.get("x") and "transform" not in s:
                full = "".join(el.itertext()).strip()
                est = sum(size if ord(ch) >= 0x2000 else size * 0.56 for ch in full)  # rough width
                x = float(re.sub(r"[a-z%]+$", "", el.get("x").split()[0]))
                anchor = cur.get("text-anchor", s.get("text-anchor", "start"))
                left = x - est if anchor == "end" else x - est / 2 if anchor == "middle" else x
                if left < -1 or left + est > w + 1:
                    warns.append(f"{path}: text '{text}' may run off the canvas (estimated width {est:.0f}pt)")
            if size is not None and local(el.tag) == "text" and name and name.startswith("iphone-duo-inner") and "-folded" in path.name \
                    and el.get("x") and el.get("y") and "transform" not in s:
                # Fold band: horizontal across the middle in portrait, vertical in landscape.
                full = "".join(el.itertext()).strip()
                est = sum(size if ord(ch) >= 0x2000 else size * 0.56 for ch in full)
                x = float(re.sub(r"[a-z%]+$", "", el.get("x").split()[0]))
                y = float(re.sub(r"[a-z%]+$", "", el.get("y").split()[0]))
                anchor = cur.get("text-anchor", "start")
                left = x - est if anchor == "end" else x - est / 2 if anchor == "middle" else x
                if h > w:
                    hit = (y - size * 0.85) < h / 2 + FOLD_BAND and y + size * 0.15 > h / 2 - FOLD_BAND
                else:
                    hit = left < w / 2 + FOLD_BAND and left + est > w / 2 - FOLD_BAND
                if hit and "data-fold-ok" not in s and not cur.get("fold_ok"):
                    errors.append(f"{path}: text '{text}' sits on the fold band "
                                 f"(add data-fold-ok on scrolling body text or lists, otherwise move it)")
            if size is not None and size < min_pt:
                errors.append(f"{path}: text '{text}' is {size:g}pt (< {min_pt}pt minimum for {platform})")
            fg = parse_color(cur.get("fill", "#000000"))
            if fg and size and local(el.tag) == "text" and el.get("x") and el.get("y") and not cur.get("xf"):
                # Text on a translucent tint: data-bg must be the composite colour, not the colour underneath.
                full = "".join(el.itertext()).strip()
                est = sum(size if ord(ch) >= 0x2000 else size * 0.56 for ch in full)
                tx, ty = num(el.get("x")), num(el.get("y"))
                anchor = cur.get("text-anchor", "start")
                mx = tx - est / 2 if anchor == "end" else tx if anchor == "middle" else tx + est / 2
                my = ty - size * 0.35
                text_boxes.append((mx - est / 2, ty - size * 0.85, est, size, full[:16]))
                under = [tb for tb in tints if tb[0] <= mx <= tb[0] + tb[2] and tb[1] <= my <= tb[1] + tb[3]]
                if under and under[-1][5] < 1:  # the topmost shape under the text is translucent
                    rx, ry, rw_, rh_, tc, ta = under[-1]
                    comp = blend(tc, cur["bg"], ta)
                    if max(abs(x - y) for x, y in zip(comp, cur["bg"])) > 2 / 255:
                        hexc = "#" + "".join(f"{round(v * 255):02X}" for v in comp)
                        errors.append(f"{path}: text '{text}' sits on a translucent shape; data-bg should be the "
                                      f"composite colour {hexc}, not the colour underneath")
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

    def overlap(a, b, m=1):
        return a[0] + m < b[0] + b[2] and b[0] + m < a[0] + a[2] and a[1] + m < b[1] + b[3] and b[1] + m < a[1] + a[3]

    if name and not path.name.startswith(("framed-", "pair-")):
        for i, a in enumerate(text_boxes):
            for b in text_boxes[i + 1:]:
                if overlap(a, b, 2):
                    warns.append(f"{path}: text '{a[4]}' may overlap text '{b[4]}' (estimated boxes)")
            for s in small_shapes:
                inside = (s[0] - 2 <= a[0] and a[0] + a[2] <= s[0] + s[2] + 2
                          and s[1] - 2 <= a[1] and a[1] + a[3] <= s[1] + s[3] + 2)  # a label on its own button
                if overlap(a, s, 2) and not inside:
                    warns.append(f"{path}: text '{a[4]}' may touch a button or marker at ({s[0]:g},{s[1]:g}); "
                                 f"truncate earlier or move it (estimated width)")

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
                if "icc_profile" not in im.info:
                    warns.append(f"{png}: no embedded color profile (HIG: Images); re-export with export_png.py")
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
        if f.name.endswith("-dark.svg"):
            lf = f.with_name(f.name[: -len("-dark.svg")] + "-light.svg")
            if lf.exists():
                try:
                    bl, bd = ET.parse(lf).getroot().get("data-bg"), ET.parse(f).getroot().get("data-bg")
                except ET.ParseError:
                    bl = bd = None
                if lf.read_bytes() == f.read_bytes():
                    errors.append(f"{f}: identical to {lf.name} (draw the dark version with dark colours)")
                elif bl and bd and bl.lower() == bd.lower():
                    errors.append(f"{f}: same background {bd} as {lf.name} (dark mode needs dark backgrounds)")
    for w in warns:
        print("WARN ", w)
    for e in errors:
        print("ERROR", e)
    print(f"checked {len(files)} SVG(s): {len(errors)} error(s), {len(warns)} warning(s)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
