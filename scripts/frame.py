#!/usr/bin/env python3
"""Wrap screen mocks in simple, generic device frames for presentation.

The frames are neutral rounded shapes, not drawings of a specific Apple product.
Screen SVGs keep their own canvas size (see devices.py); this script nests them.

Name single-device outputs "framed-<screen name>.svg" so the export/check scripts treat
them as presentation images, not screen mocks. Duo outputs use "iphone-duo-...".

Usage:
  frame.py iphone SCREEN.svg -o OUT.svg
  frame.py ipad   SCREEN.svg -o OUT.svg          # landscape or portrait, from the screen size
  frame.py mac    SCREEN.svg -o OUT.svg
  frame.py watch  SCREEN.svg -o OUT.svg
  frame.py duo    LEFT.svg RIGHT.svg -o OUT.svg [--bg "#F2F2F7"] [--caption-left TEXT --caption-right TEXT]
"""
import argparse
import re
import sys
from pathlib import Path
from xml.sax.saxutils import escape

FONT = "-apple-system, 'SF Pro Text', 'Hiragino Sans', 'Noto Sans JP', 'Noto Sans CJK JP', sans-serif"


def load_screen(path):
    text = Path(path).read_text(encoding="utf-8")
    text = re.sub(r"<\?xml[^>]*\?>", "", text).strip()
    m = re.search(r"<svg\b[^>]*>", text)
    if not m:
        sys.exit(f"{path}: no <svg> root found")
    tag = m.group(0)
    vb = re.search(r'viewBox="([^"]+)"', tag)
    if vb:
        _, _, w, h = (float(v) for v in vb.group(1).replace(",", " ").split())
    else:
        w = float(re.search(r'width="([\d.]+)', tag).group(1))
        h = float(re.search(r'height="([\d.]+)', tag).group(1))
    # Drop root width/height/x/y; they are set by the caller.
    inner_tag = re.sub(r'\s(width|height|x|y)="[^"]*"', "", tag)
    if not vb:
        inner_tag = inner_tag[:-1] + f' viewBox="0 0 {w:g} {h:g}">'
    body = text[m.end():]
    return w, h, inner_tag, body


def nest(path, x, y, scale, clip_id, radius):
    w, h, tag, body = load_screen(path)
    sw, sh = w * scale, h * scale
    tag = tag[:-1] + f' x="{x:g}" y="{y:g}" width="{sw:g}" height="{sh:g}">'
    clip = (f'<clipPath id="{clip_id}"><rect x="{x:g}" y="{y:g}" width="{sw:g}" '
            f'height="{sh:g}" rx="{radius * scale:g}"/></clipPath>')
    return clip, f'<g clip-path="url(#{clip_id})">{tag}{body}</g>', sw, sh


def device(kind, path, ox, oy, scale, uid):
    w, h, _, _ = load_screen(path)
    if kind == "iphone":
        bezel, r_screen, r_body = 14, 55, 69
    elif kind == "ipad":
        bezel, r_screen, r_body = 22, 18, 40
    elif kind == "watch":
        bezel, r_screen, r_body = 14, 42, 56
    elif kind == "mac":
        bezel, r_screen, r_body = 18, 10, 22
    else:
        sys.exit(f"unknown device {kind}")
    b = bezel * scale
    clip, screen, sw, sh = nest(path, ox + b, oy + b, scale, f"clip{uid}", r_screen)
    bw, bh = sw + 2 * b, sh + 2 * b
    parts = [clip]
    if kind == "watch":
        # Digital Crown and side button on the right edge.
        parts.append(f'<rect x="{ox + bw - 2 * scale:g}" y="{oy + bh * 0.28:g}" width="{9 * scale:g}" '
                     f'height="{bh * 0.16:g}" rx="{3 * scale:g}" fill="#2C2C2E"/>')
        parts.append(f'<rect x="{ox + bw - 2 * scale:g}" y="{oy + bh * 0.52:g}" width="{6 * scale:g}" '
                     f'height="{bh * 0.2:g}" rx="{3 * scale:g}" fill="#2C2C2E"/>')
    parts.append(f'<rect x="{ox:g}" y="{oy:g}" width="{bw:g}" height="{bh:g}" rx="{r_body * scale:g}" '
                 f'fill="#1C1C1E" stroke="#3A3A3C" stroke-width="{1.5 * scale:g}"/>')
    parts.append(screen)
    if kind == "iphone":
        # Generic camera pill. Screens must keep content out of this area (Safe Area).
        pw, ph = 125 * scale, 37 * scale
        parts.append(f'<rect x="{ox + bw / 2 - pw / 2:g}" y="{oy + b + 11 * scale:g}" width="{pw:g}" '
                     f'height="{ph:g}" rx="{ph / 2:g}" fill="#000"/>')
    if kind == "mac":
        # Simple stand under the display.
        parts.append(f'<rect x="{ox + bw * 0.42:g}" y="{oy + bh:g}" width="{bw * 0.16:g}" '
                     f'height="{40 * scale:g}" fill="#3A3A3C"/>')
        parts.append(f'<rect x="{ox + bw * 0.34:g}" y="{oy + bh + 40 * scale:g}" width="{bw * 0.32:g}" '
                     f'height="{8 * scale:g}" rx="{4 * scale:g}" fill="#48484A"/>')
        bh += 48 * scale
    return "\n".join(parts), bw, bh


def wrap(width, height, content, bg=None):
    bg_rect = f'<rect width="100%" height="100%" fill="{bg}"/>' if bg else ""
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" '
            f'width="{width:g}" height="{height:g}" viewBox="0 0 {width:g} {height:g}">'
            f'{bg_rect}{content}</svg>\n')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("kind", choices=["iphone", "ipad", "mac", "watch", "duo"])
    ap.add_argument("screens", nargs="+")
    ap.add_argument("-o", "--out", required=True)
    ap.add_argument("--bg", default=None, help="background color (duo default #F2F2F7)")
    ap.add_argument("--caption-left", default="")
    ap.add_argument("--caption-right", default="")
    a = ap.parse_args()

    if a.kind != "duo":
        if len(a.screens) != 1:
            sys.exit("one screen expected")
        pad = 24
        dev, bw, bh = device(a.kind, a.screens[0], pad, pad, 1, "0")
        Path(a.out).write_text(wrap(bw + 2 * pad, bh + 2 * pad, dev, a.bg), encoding="utf-8")
        return

    if len(a.screens) != 2:
        sys.exit("duo needs exactly two screens: LEFT RIGHT")
    W, H = 1600, 1000
    bg = a.bg or "#F2F2F7"
    w0, h0, _, _ = load_screen(a.screens[0])
    w1, h1, _, _ = load_screen(a.screens[1])
    if (w0, h0) != (w1, h1):
        sys.exit("duo: both screens must use the same canvas (D-03: same size)")
    caption = bool(a.caption_left or a.caption_right)
    avail_h = H - (190 if caption else 110)
    scale = avail_h / (h0 + 28)
    dw = (w0 + 28) * scale
    gap = 120
    x0 = (W - (2 * dw + gap)) / 2
    y0 = 55
    d0, _, dh = device("iphone", a.screens[0], x0, y0, scale, "L")
    d1, _, _ = device("iphone", a.screens[1], x0 + dw + gap, y0, scale, "R")
    caps = ""
    if caption:
        cy = y0 + dh + 58
        label = "#3C3C43" if bg.upper() in ("#F2F2F7", "#FFFFFF") else "#EBEBF5"
        for text, cx in ((a.caption_left, x0 + dw / 2), (a.caption_right, x0 + dw + gap + dw / 2)):
            caps += (f'<text x="{cx:g}" y="{cy:g}" text-anchor="middle" font-family="{FONT}" '
                     f'font-size="34" font-weight="600" fill="{label}">{escape(text)}</text>')
    Path(a.out).write_text(wrap(W, H, d0 + d1 + caps, bg), encoding="utf-8")


if __name__ == "__main__":
    main()
