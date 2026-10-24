#!/usr/bin/env python3
"""Builds the example mocks for the fictional app 「ひとこと日記」.

All names and entries are fictional. Colors are the approximate values from
references/hig-specs.md (implementation uses system colors).
Run: python3 examples/hitokoto/build.py && python3 scripts/export_png.py examples/hitokoto/mocks
"""
from pathlib import Path
from xml.sax.saxutils import escape

OUT = Path(__file__).resolve().parent / "mocks"
OUT.mkdir(exist_ok=True)
FONT = "-apple-system, 'SF Pro Text', 'Hiragino Sans', 'Noto Sans JP', 'Noto Sans CJK JP', sans-serif"
WATCH_FONT = "'SF Compact Text', 'SF Compact Rounded', 'Hiragino Sans', 'Noto Sans JP', 'Noto Sans CJK JP', sans-serif"

THEMES = {
    "light": dict(bg="#F2F2F7", cell="#FFFFFF", label="#000000", sec="#3C3C43", sec_op=0.8,
                  sep="#C6C6C8", accent="#0088FF", accent_text="#0066CC", glass="#FFFFFF", glass_op=0.82, glass_stroke="#D1D1D6",
                  side="#F2F2F7", desk="#C9D3DF", win="#FFFFFF", bar="#F6F6F6"),
    "dark": dict(bg="#000000", cell="#1C1C1E", label="#FFFFFF", sec="#EBEBF5", sec_op=0.6,
                 sep="#38383A", accent="#0091FF", accent_text="#5CB8FF", glass="#2C2C2E", glass_op=0.82, glass_stroke="#48484A",
                 side="#1C1C1E", desk="#1F2633", win="#1E1E1E", bar="#2A2A2A"),
}

ENTRIES = [
    ("10月24日（土）", "公園の銀杏が色づいてきた。\n帰りにパン屋へ寄った。"),
    ("10月23日（金）", "新しいノートを使い始めた。書き心地がいい。"),
    ("10月22日（木）", "雨。家で本を一冊読み終えた。"),
    ("10月21日（水）", "朝の散歩で猫に会った。"),
    ("10月20日（火）", "久しぶりにカレーを作った。少し辛すぎた。"),
]


def one(s, n):
    """List row: line breaks become spaces, then cut to n characters with an ellipsis."""
    s = s.replace("\n", " ")
    return s[:n].rstrip() + "…" if len(s) > n else s


def T(x, y, s, size, fill, weight=400, anchor="start", op=None, bg=None, font=None):
    o = f' opacity="{op}"' if op is not None else ""
    b = f' data-bg="{bg}"' if bg else ""
    return (f'<text x="{x}" y="{y}" font-family="{font or FONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{o}{b}>{escape(s)}</text>')


def mix(fg, bg, a):
    """Composite colour of fg at opacity a over bg (for data-bg on tinted rows)."""
    f = [int(fg[i:i + 2], 16) for i in (1, 3, 5)]
    g = [int(bg[i:i + 2], 16) for i in (1, 3, 5)]
    return "#" + "".join(f"{round(x * a + y * (1 - a)):02X}" for x, y in zip(f, g))


def chevron(x, cy, c):
    # Disclosure indicator (chevron.forward) for rows that drill into a detail view.
    return (f'<path d="M{x} {cy-6}l6 6-6 6" fill="none" stroke="{c}" stroke-opacity="0.35" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round"/>')


def search_btn(cx, cy, t, fill=None):
    return (f'<circle cx="{cx}" cy="{cy}" r="22" fill="{fill or t["glass"]}" fill-opacity="{1 if fill else t["glass_op"]}" '
            f'stroke="{t["glass_stroke"]}"/><g fill="none" stroke="{t["label"]}" stroke-width="2">'
            f'<circle cx="{cx-2}" cy="{cy-2}" r="7"/><path d="M{cx+3} {cy+3}l5 5"/></g>')


def text_btn(x, y, label, t, fill=None, size=17):
    """Plain text button in a glass capsule (not filled): x = left edge, y = top, height 44."""
    tw = len(label) * size + 32
    f = fill or t["glass"]
    return (f'<rect x="{x}" y="{y}" width="{tw}" height="44" rx="22" fill="{f}" stroke="{t["glass_stroke"]}"/>'
            + T(x + tw / 2, y + 28, label, size, t["label"], 400, "middle", bg=f)), tw




def trash_btn(cx, cy, t, fill=None):
    """Delete (trash) as a plain symbol button; VoiceOver label 「削除」."""
    f = fill or t["glass"]
    c = t["label"]
    return (f'<g aria-label="削除"><circle cx="{cx}" cy="{cy}" r="22" fill="{f}" stroke="{t["glass_stroke"]}"/>'
            f'<g fill="none" stroke="{c}" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round">'
            f'<path d="M{cx-8} {cy-6}h16M{cx-3} {cy-6}v-3h6v3M{cx-6} {cy-6}l1 14h10l1-14"/></g></g>')


def sun(cx, cy, c, filled=False):
    rays = "".join(f'<path d="M{cx + 9 * dx:.1f} {cy + 9 * dy:.1f}l{3 * dx:.1f} {3 * dy:.1f}"/>'
                   for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1), (.7, .7), (-.7, .7), (.7, -.7), (-.7, -.7)))
    body = f'<circle cx="{cx}" cy="{cy}" r="5" fill="{c if filled else "none"}"/>'
    return f'<g stroke="{c}" stroke-width="1.8" fill="none" stroke-linecap="round">{body}{rays}</g>'


def cloud(cx, cy, c, extra=""):
    g = (f'<path d="M{cx-9} {cy+4}a5 5 0 0 1 1-10a7 7 0 0 1 13 1a5 5 0 0 1 4 9z" fill="none" stroke="{c}" '
         f'stroke-width="1.8" stroke-linejoin="round"/>')
    if extra == "rain":
        g += "".join(f'<path d="M{cx-5+5*k} {cy+8}l-2 5" stroke="{c}" stroke-width="1.8" stroke-linecap="round"/>' for k in range(3))
    return g


def snow(cx, cy, c):
    return (f'<g stroke="{c}" stroke-width="1.8" stroke-linecap="round"><path d="M{cx} {cy-10}v20M{cx-9} {cy-5}l18 10'
            f'M{cx-9} {cy+5}l18 -10"/></g>')


def weather_line(x, y, t, size, bg):
    """Weather symbol + text label + time (the label is read; the symbol is decorative)."""
    s = size / 17  # symbol scaled to the text size
    cy = y - size * 0.35
    icon = f'<g transform="translate({x + 12 * s} {cy}) scale({s})">{sun(0, 0, t["sec"])}</g>'
    return icon + T(x + 30 * s, y, "晴れ・午後 5:12", size, t["sec"], 400, op=t["sec_op"], bg=bg)


def svg(w, h, bg, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" '
            f'data-bg="{bg}"><rect width="100%" height="100%" fill="{bg}"/>{body}</svg>\n')


def symbol_pencil(x, y, c, s=1.0):
    # Simple stand-in for the SF Symbol "square.and.pencil" (use the real symbol in the app).
    return (f'<g transform="translate({x},{y}) scale({s})" fill="none" stroke="{c}" stroke-width="2" '
            f'stroke-linecap="round" stroke-linejoin="round"><path d="M3 6h7M3 6v13h13v-7"/>'
            f'<path d="M19 2l3 3-9 9h-3v-3z"/></g>')


def symbol(kind, cx, cy, c):
    if kind == "book":
        # open book (two pages and a centre spine) -- distinct from sidebar.left
        return (f'<g fill="none" stroke="{c}" stroke-width="2" stroke-linejoin="round">'
                f'<path d="M{cx} {cy-6}c-3-3-7-4-11-3v15c4-1 8 0 11 3c3-3 7-4 11-3v-15c-4-1-8 0-11 3z"/>'
                f'<path d="M{cx} {cy-6}v15"/></g>')
    if kind == "cal":
        return (f'<g fill="none" stroke="{c}" stroke-width="2"><rect x="{cx-10}" y="{cy-9}" width="20" '
                f'height="18" rx="3"/><path d="M{cx-10} {cy-3}h20M{cx-5} {cy-12}v5M{cx+5} {cy-12}v5"/></g>')
    if kind == "gear":
        return (f'<g fill="none" stroke="{c}" stroke-width="2"><circle cx="{cx}" cy="{cy}" r="4"/>'
                f'<circle cx="{cx}" cy="{cy}" r="9" stroke-dasharray="4 3"/></g>')
    return ""


def status_bar(w, t):
    # Time on the left, battery on the right; the camera pill area in the middle stays empty.
    return (T(54, 37, "9:41", 17, t["label"], 600, "middle")
            + f'<rect x="{w-62}" y="25" width="26" height="13" rx="4" fill="none" stroke="{t["label"]}" '
              f'stroke-opacity="0.4"/><rect x="{w-60}" y="27" width="20" height="9" rx="2" fill="{t["label"]}"/>')


def symbol_filled(kind, cx, cy, c, cut="#FFFFFF"):
    """Filled stand-ins: iOS tab bars use the .fill variant of SF Symbols.
    `cut` is the colour of the cut-out details (the bar colour behind the symbol)."""
    if kind == "book":
        return (f'<path d="M{cx} {cy-6}c-3-3-7-4-11-3v15c4-1 8 0 11 3c3-3 7-4 11-3v-15c-4-1-8 0-11 3z" fill="{c}"/>'
                f'<rect x="{cx-0.75}" y="{cy-6}" width="1.5" height="15" fill="{cut}"/>')
    if kind == "cal":
        return (f'<rect x="{cx-10}" y="{cy-9}" width="20" height="18" rx="3" fill="{c}"/>'
                f'<rect x="{cx-10}" y="{cy-4}" width="20" height="1.5" fill="{cut}"/>')
    if kind == "gear":
        return (f'<circle cx="{cx}" cy="{cy}" r="9" fill="{c}"/>'
                f'<circle cx="{cx}" cy="{cy}" r="3.5" fill="{cut}"/>')
    return ""


def tab_bar(w, h, t, active=0, maxw=None):
    # Floating Liquid Glass tab bar: navigation only, symbol + one-word label per tab.
    bh = 62
    total = min(w - 2 * 21, maxw or w)
    x0 = (w - total) / 2
    bw = total - bh - 10  # search is its own tab at the trailing end (separate round button)
    x, y = x0, h - 34 - bh
    parts = [f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="31" fill="{t["glass"]}" '
             f'fill-opacity="{t["glass_op"]}" stroke="{t["glass_stroke"]}"/>']
    tabs = [("book", "日記"), ("cal", "カレンダー"), ("gear", "設定")]
    for i, (sym, lab) in enumerate(tabs):
        cx = x + bw * (i + 0.5) / 3
        col = t["accent"] if i == active else t["label"]
        tabbg = mix(t["accent"], t["glass"], 0.12) if i == active else t["glass"]
        if i == active:
            parts.append(f'<rect x="{cx-46}" y="{y+5}" width="92" height="{bh-10}" rx="26" fill="{tabbg}"/>')
        parts.append(symbol_filled(sym, cx, y + 22, col, tabbg))
        parts.append(T(cx, y + 50, lab, 11, col, 600, "middle", bg=tabbg))
    parts.append(search_btn(x0 + total - bh / 2, y + bh / 2, t).replace('r="22"', f'r="{bh/2}"', 1))
    return "".join(parts)


def iphone_list(theme):
    t = THEMES[theme]
    w, h = 402, 874
    b = [status_bar(w, t)]
    # Toolbar button (add) top-right, 44x44 hit area.
    b.append(f'<circle cx="{w-38}" cy="84" r="22" fill="{t["glass"]}" fill-opacity="{t["glass_op"]}" '
             f'stroke="{t["glass_stroke"]}"/>' + symbol_pencil(w - 50, 72, t["label"]))
    b.append(T(20, 150, "日記", 34, t["label"], 700))
    b.append(T(20, 180, "残り 25件（無料版は 30件まで）", 15, t["sec"], 400, op=t["sec_op"]))
    y = 204
    b.append(f'<rect x="16" y="{y}" width="{w-32}" height="{len(ENTRIES)*76}" rx="26" fill="{t["cell"]}"/>')
    for i, (d, s) in enumerate(ENTRIES):
        cy = y + i * 76
        b.append(T(36, cy + 31, d, 15, t["sec"], 400, op=t["sec_op"], bg=t["cell"]))
        b.append(T(36, cy + 56, one(s, 17), 17, t["label"], 400, bg=t["cell"]))
        b.append(chevron(w - 44, cy + 38, t["label"]))
        if i < len(ENTRIES) - 1:
            b.append(f'<rect x="36" y="{cy+75.5}" width="{w-52}" height="0.5" fill="{t["sep"]}"/>')
    b.append(tab_bar(w, h, t))
    b.append(f'<rect x="{w/2-70}" y="{h-13}" width="140" height="5" rx="2.5" fill="{t["label"]}"/>')
    return svg(w, h, t["bg"], "".join(b))


def iphone_detail(theme):
    t = THEMES[theme]
    w, h = 402, 874
    d, s = ENTRIES[0]
    b = [status_bar(w, t)]
    b.append(f'<circle cx="38" cy="84" r="22" fill="{t["glass"]}" fill-opacity="{t["glass_op"]}" '
             f'stroke="{t["glass_stroke"]}"/><path d="M42 74l-10 10 10 10" fill="none" stroke="{t["label"]}" '
             f'stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"/>')
    eb, ew = text_btn(w - 22 - 44 - 8 - 66, 62, "編集", t)
    b.append(eb)
    b.append(trash_btn(w - 44, 84, t))
    b.append(T(20, 150, d, 28, t["label"], 700))
    b.append(f'<rect x="16" y="176" width="{w-32}" height="170" rx="26" fill="{t["cell"]}"/>')
    b.append(T(36, 220, "公園の銀杏が色づいてきた。", 17, t["label"], 400, bg=t["cell"]))
    b.append(T(36, 248, "帰りにパン屋へ寄った。", 17, t["label"], 400, bg=t["cell"]))
    b.append(weather_line(36, 318, t, 15, t["cell"]))
    b.append(tab_bar(w, h, t))
    b.append(f'<rect x="{w/2-70}" y="{h-13}" width="140" height="5" rx="2.5" fill="{t["label"]}"/>')
    return svg(w, h, t["bg"], "".join(b))


def ipad(theme):
    t = THEMES[theme]
    w, h = 1376, 1032
    sw = 320
    b = [T(32, 34, "9:41", 15, t["label"], 600), T(110, 34, "10月24日（土）", 15, t["label"], 600)]
    # Floating sidebar (Liquid Glass) with two levels at most.
    b.append(f'<rect x="12" y="52" width="{sw}" height="{h-64}" rx="26" fill="{t["cell"]}" '
             f'stroke="{t["glass_stroke"]}"/>')
    b.append(f'<g fill="none" stroke="{t["label"]}" stroke-width="2"><rect x="30" y="72" width="22" height="20" rx="3"/>'
             f'<path d="M38 72v20"/></g>')
    items = [("book", "すべての日記", True), ("cal", "カレンダー", False), ("gear", "設定", False)]
    for i, (sym, lab, on) in enumerate(items):
        y = 132 + i * 52
        rowbg = mix(t["accent"], t["cell"], 0.14) if on else t["cell"]
        if on:
            b.append(f'<rect x="24" y="{y}" width="{sw-24}" height="44" rx="12" fill="{rowbg}"/>')
        b.append(symbol(sym, 52, y + 22, t["accent"]))  # sidebar icons use the accent colour
        b.append(T(76, y + 28, lab, 17, t["label"], 600 if on else 400, bg=rowbg))
    # List column + detail.
    lx = sw + 36
    lw = 400
    b.append(T(lx, 104, "すべての日記", 34, t["label"], 700))
    b.append(T(lx, 132, "残り 25件（無料版は 30件まで）", 15, t["sec"], 400, op=t["sec_op"]))
    b.append(f'<rect x="{lx}" y="148" width="{lw}" height="{len(ENTRIES)*76}" rx="26" fill="{t["cell"]}"/>')
    for i, (d, s) in enumerate(ENTRIES):
        cy = 148 + i * 76
        rowbg = mix(t["accent"], t["cell"], 0.14) if i == 0 else t["cell"]
        if i == 0:
            b.append(f'<rect x="{lx+8}" y="{cy+6}" width="{lw-16}" height="64" rx="18" fill="{rowbg}"/>')
        b.append(T(lx + 20, cy + 31, d, 15, t["sec"], 400, op=t["sec_op"], bg=rowbg))
        b.append(T(lx + 20, cy + 56, one(s, 17), 17, t["label"], 400, bg=rowbg))
    dx = lx + lw + 32
    # Toolbar: 編集, 今日を書く, then the search field at the trailing end (⌘F).
    sx = w - 28 - 250
    b.append(f'<circle cx="{sx-34}" cy="76" r="22" fill="{t["cell"]}" stroke="{t["glass_stroke"]}"/>'
             + symbol_pencil(sx - 46, 64, t["label"]))
    b.append(trash_btn(sx - 34 - 22 - 8 - 22, 76, t, fill=t["cell"]))
    eb, ew = text_btn(sx - 34 - 22 - 8 - 44 - 8 - 66, 54, "編集", t, fill=t["cell"])
    b.append(eb)
    b.append(f'<rect x="{sx}" y="54" width="250" height="44" rx="22" fill="{t["cell"]}" stroke="{t["glass_stroke"]}"/>'
             f'<g fill="none" stroke="{t["sec"]}" stroke-width="2"><circle cx="{sx+24}" cy="74" r="7"/>'
             f'<path d="M{sx+29} 79l5 5"/></g>')
    b.append(T(sx + 44, 82, "日記を検索", 17, t["sec"], 400, op=t["sec_op"], bg=t["cell"]))
    d, s = ENTRIES[0]
    b.append(T(dx, 142, d, 28, t["label"], 700))
    b.append(f'<rect x="{dx}" y="160" width="{w-dx-28}" height="180" rx="26" fill="{t["cell"]}"/>')
    b.append(T(dx + 24, 208, "公園の銀杏が色づいてきた。", 17, t["label"], 400, bg=t["cell"]))
    b.append(T(dx + 24, 236, "帰りにパン屋へ寄った。", 17, t["label"], 400, bg=t["cell"]))
    b.append(weather_line(dx + 24, 312, t, 15, t["cell"]))
    return svg(w, h, t["bg"], "".join(b))


def mac_toolbar(wx, wy, ww, t, edit_enabled=True):
    """Mac toolbar shared by all main views: 編集, 今日を書く, search field (⌘F) at the trailing end.
    28pt controls 16pt apart so their 44pt hit areas do not overlap."""
    sx = wx + ww - 196
    ec = t["label"] if edit_enabled else t["sec"]
    return (f'<rect x="{sx-44}" y="{wy+14}" width="28" height="28" rx="6" fill="{t["bar"]}"/>'
            + symbol_pencil(sx - 42, wy + 16, t["label"], 1.0)
            + f'<rect x="{sx-108}" y="{wy+14}" width="48" height="28" rx="6" fill="{t["bar"]}"/>'
            + T(sx - 84, wy + 33, "編集", 13, ec, 400, "middle", bg=t["bar"])
            + f'<rect x="{sx}" y="{wy+14}" width="180" height="28" rx="8" fill="{t["bar"]}"/>'
            f'<g fill="none" stroke="{t["sec"]}" stroke-width="1.6"><circle cx="{sx+16}" cy="{wy+27}" r="5"/>'
            f'<path d="M{sx+20} {wy+31}l4 4"/></g>'
            + T(sx + 30, wy + 32, "日記を検索", 13, t["sec"], 400, op=t["sec_op"], bg=t["bar"]))


def mac(theme):
    t = THEMES[theme]
    w, h = 1440, 900
    b = [f'<rect x="0" y="0" width="{w}" height="26" fill="{t["bar"]}" fill-opacity="0.9"/>',
         T(20, 18, "ひとこと日記", 13, t["label"], 700, bg=t["bar"]),
         T(130, 18, "ファイル", 13, t["label"], 400, bg=t["bar"]),
         T(196, 18, "編集", 13, t["label"], 400, bg=t["bar"]),
         T(240, 18, "表示", 13, t["label"], 400, bg=t["bar"]),
         T(284, 18, "ウインドウ", 13, t["label"], 400, bg=t["bar"]),
         T(364, 18, "ヘルプ", 13, t["label"], 400, bg=t["bar"]),
         T(w - 20, 18, "10月24日(土) 9:41", 13, t["label"], 400, "end", bg=t["bar"])]
    wx, wy, ww, wh = 150, 90, 1140, 720
    b.append(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="16" fill="{t["win"]}" '
             f'stroke="{t["glass_stroke"]}"/>')
    sw = 240
    b.append(f'<rect x="{wx+8}" y="{wy+8}" width="{sw}" height="{wh-16}" rx="12" fill="{t["side"]}"/>')
    for i, c in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        b.append(f'<circle cx="{wx+28+i*20}" cy="{wy+28}" r="6" fill="{c}"/>')
    b.append(f'<g aria-label="サイドバー" fill="none" stroke="{t["label"]}" stroke-width="1.5"><rect x="{wx+sw-30}" y="{wy+20}" width="18" height="16" rx="3"/>'
             f'<path d="M{wx+sw-24} {wy+20}v16"/></g>')
    items = [("book", "すべての日記", True), ("cal", "カレンダー", False)]
    for i, (sym, lab, on) in enumerate(items):
        y = wy + 64 + i * 32
        rowbg = mix(t["accent"], t["side"], 0.16) if on else t["side"]
        if on:
            b.append(f'<rect x="{wx+16}" y="{y}" width="{sw-16}" height="28" rx="6" fill="{rowbg}"/>')
        # Mac sidebar icons use the accent colour whether selected or not.
        b.append(symbol(sym, wx + 34, y + 14, t["accent"]).replace('stroke-width="2"', 'stroke-width="1.6"'))
        b.append(T(wx + 52, y + 19, lab, 13, t["label"], 600 if on else 400, bg=rowbg))
    lx = wx + sw + 24
    b.append(T(lx, wy + 26, "すべての日記", 13, t["label"], 700, bg=t["win"]))
    b.append(T(lx, wy + 43, "残り 25件（無料版は 30件まで）", 11, t["sec"], 400, op=t["sec_op"], bg=t["win"]))
    b.append(mac_toolbar(wx, wy, ww, t))
    b.append(f'<rect x="{lx-8}" y="{wy+52}" width="{ww-sw-32}" height="0.5" fill="{t["sep"]}"/>')
    lw = 320
    for i, (d, s) in enumerate(ENTRIES):
        y = wy + 64 + i * 56
        rowbg = mix(t["accent"], t["win"], 0.16) if i == 0 else t["win"]
        if i == 0:
            b.append(f'<rect x="{lx-8}" y="{y}" width="{lw}" height="52" rx="8" fill="{rowbg}"/>')
        b.append(T(lx, y + 20, d, 11, t["sec"], 400, op=t["sec_op"], bg=rowbg))
        b.append(T(lx, y + 40, one(s, 20), 13, t["label"], 400, bg=rowbg))
    dx = lx + lw + 24
    b.append(f'<rect x="{dx-12}" y="{wy+52}" width="0.5" height="{wh-60}" fill="{t["sep"]}"/>')
    d, s = ENTRIES[0]
    b.append(T(dx, wy + 96, d, 22, t["label"], 700, bg=t["win"]))
    for k, line in enumerate(s.split("\n")):
        b.append(T(dx, wy + 136 + 18 * k, line, 13, t["label"], 400, bg=t["win"]))
    b.append(weather_line(dx, wy + 184, t, 11, t["win"]))
    return svg(w, h, t["desk"], "".join(b))


def watch():
    """Apple Watch Ultra (49mm): xLarge is the default size -> Body 17pt, Footnote 1 14pt.
    System font is SF Compact."""
    w, h = 211, 257
    W = dict(font=WATCH_FONT)
    b = [T(w - 18, 28, "9:41", 15, "#FFFFFF", 600, "end", **W),
         T(w - 18, 52, "今日のひとこと", 17, "#0091FF", 600, "end", **W),
         f'<rect x="10" y="66" width="{w-20}" height="108" rx="20" fill="#1C1C1E"/>',
         T(22, 104, "公園の銀杏が", 17, "#FFFFFF", 400, bg="#1C1C1E", **W),
         T(22, 128, "色づいてきた。 帰…", 17, "#FFFFFF", 400, bg="#1C1C1E", **W),
         T(22, 158, "午後 5:12", 14, "#EBEBF5", 400, op=0.6, bg="#1C1C1E", **W),
         f'<rect x="10" y="186" width="{w-20}" height="50" rx="25" fill="#0091FF"/>',
         '<g fill="none" stroke="#FFFFFF" stroke-width="2" stroke-linecap="round"><rect x="34" y="200" width="9" height="15" rx="4.5"/>'
         '<path d="M30 210a8.5 8.5 0 0 0 17 0M38.5 219v3"/></g>',
         T(w / 2 + 12, 217, "音声で書く", 17, "#FFFFFF", 600, "middle", bg="#0091FF", **W)]
    return svg(w, h, "#000000", "".join(b))


def watch_aod():
    """Always On (wrist down): same layout, supporting parts dimmed, the diary text (private)
    hidden, the button kept but shown as non-interactive."""
    w, h = 211, 257
    W = dict(font=WATCH_FONT)
    b = [T(w - 18, 28, "9:41", 15, "#AEAEB2", 600, "end", **W),
         T(w - 18, 52, "今日のひとこと", 17, "#5E9EDB", 600, "end", **W),
         f'<rect x="10" y="66" width="{w-20}" height="108" rx="20" fill="#0D0D0F"/>',
         T(22, 116, "書いた", 20, "#AEAEB2", 600, bg="#0D0D0F", **W),
         T(22, 158, "午後 5:12", 14, "#8E8E93", 400, bg="#0D0D0F", **W),
         f'<rect x="10" y="186" width="{w-20}" height="50" rx="25" fill="none" stroke="#3A3A3C" stroke-width="1.5"/>',
         '<g fill="none" stroke="#8E8E93" stroke-width="2" stroke-linecap="round"><rect x="34" y="200" width="9" height="15" rx="4.5"/>'
         '<path d="M30 210a8.5 8.5 0 0 0 17 0M38.5 219v3"/></g>',
         T(w / 2 + 12, 217, "音声で書く", 17, "#8E8E93", 600, "middle", bg="#000000", **W)]
    return svg(w, h, "#000000", "".join(b))


def iphone_empty(theme):
    t = THEMES[theme]
    w, h = 402, 874
    b = [status_bar(w, t)]
    b.append(f'<circle cx="{w-38}" cy="84" r="22" fill="{t["glass"]}" fill-opacity="{t["glass_op"]}" '
             f'stroke="{t["glass_stroke"]}"/>' + symbol_pencil(w - 50, 72, t["label"]))
    b.append(T(20, 150, "日記", 34, t["label"], 700))
    b.append(T(20, 180, "残り 30件（無料版は 30件まで）", 15, t["sec"], 400, op=t["sec_op"]))
    b.append(symbol("book", w / 2, 330, t["sec"]).replace('stroke-width="2"', 'stroke-width="3"')
             .replace(f'x="{w/2-9}"', f'x="{w/2-9}"'))
    b.append(T(w / 2, 390, "まだ日記がありません", 22, t["label"], 700, "middle"))
    b.append(T(w / 2, 424, "今日のことを、ひとことだけ書いてみましょう。", 15, t["sec"], 400, "middle", op=t["sec_op"]))
    b.append(f'<rect x="{w/2-90}" y="456" width="180" height="50" rx="25" fill="{t["accent"]}"/>')
    b.append(T(w / 2, 488, "今日を書く", 17, "#FFFFFF", 600, "middle", bg=t["accent"]))
    b.append(tab_bar(w, h, t))
    b.append(f'<rect x="{w/2-70}" y="{h-13}" width="140" height="5" rx="2.5" fill="{t["label"]}"/>')
    return svg(w, h, t["bg"], "".join(b))


def iphone_ax5(theme):
    """Largest accessibility text size (AX5): Large Title 60pt, Subhead 49pt, Body 53pt.
    Rows stack and wrap; the body shows up to 4 lines (the full text is on S-02); the bars keep their size."""
    t = THEMES[theme]
    w, h = 402, 874
    b = [status_bar(w, t)]
    b.append(f'<circle cx="{w-38}" cy="84" r="22" fill="{t["glass"]}" fill-opacity="{t["glass_op"]}" '
             f'stroke="{t["glass_stroke"]}"/>' + symbol_pencil(w - 50, 72, t["label"]))
    b.append(T(20, 176, "日記", 60, t["label"], 700))
    b.append(T(20, 236, "残り 25件", 49, t["sec"], 400, op=t["sec_op"]))
    b.append(T(20, 296, "（無料版は", 49, t["sec"], 400, op=t["sec_op"]))
    b.append(T(20, 356, "30件まで）", 49, t["sec"], 400, op=t["sec_op"]))
    b.append(f'<rect x="16" y="380" width="{w-32}" height="520" rx="26" fill="{t["cell"]}"/>')
    b.append(chevron(w - 44, 520, t["label"]))
    lines = [("10月24日", 49, "sec"), ("（土）", 49, "sec"), ("公園の", 53, "label"),
             ("銀杏が色づ", 53, "label"), ("いてきた。", 53, "label"), ("帰りにパ…", 53, "label")]
    y = 444
    for text, size, kind in lines:
        if kind == "sec":
            b.append(T(36, y, text, size, t["sec"], 400, op=t["sec_op"], bg=t["cell"]))
        else:
            b.append(T(36, y, text, size, t["label"], 400, bg=t["cell"]))
        y += 70
    b.append('<g data-overlap-ok="1">' + tab_bar(w, h, t) + '</g>')  # the list scrolls under the bar
    b.append(f'<rect x="{w/2-70}" y="{h-13}" width="140" height="5" rx="2.5" fill="{t["label"]}"/>')
    return svg(w, h, t["bg"], "".join(b))


def ipad_narrow(theme):
    """Narrow iPad window: the sidebar collapses to a button, the list fills the width."""
    t = THEMES[theme]
    w, h = 600, 1032
    b = [T(24, 34, "9:41", 15, t["label"], 600)]
    # Window controls (approximation) sit at the leading edge of the toolbar when windowed.
    for k, c in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        b.append(f'<circle cx="{30 + k * 20}" cy="80" r="6" fill="{c}"/>')
    b.append(f'<circle cx="120" cy="80" r="22" fill="{t["cell"]}" stroke="{t["glass_stroke"]}"/>'
             f'<g fill="none" stroke="{t["label"]}" stroke-width="2"><rect x="109" y="70" width="22" height="20" rx="3"/>'
             f'<path d="M117 70v20"/></g>')
    b.append(f'<circle cx="{w-96}" cy="80" r="22" fill="{t["cell"]}" stroke="{t["glass_stroke"]}"/>'
             + symbol_pencil(w - 108, 68, t["label"]))
    b.append(search_btn(w - 44, 80, t, fill=t["cell"]))  # search folds into a button at the trailing end
    b.append(T(24, 150, "すべての日記", 34, t["label"], 700))
    b.append(T(24, 180, "残り 25件（無料版は 30件まで）", 15, t["sec"], 400, op=t["sec_op"]))
    b.append(f'<rect x="20" y="204" width="{w-40}" height="{len(ENTRIES)*76}" rx="26" fill="{t["cell"]}"/>')
    for i, (d, s) in enumerate(ENTRIES):
        cy = 204 + i * 76
        b.append(T(40, cy + 31, d, 15, t["sec"], 400, op=t["sec_op"], bg=t["cell"]))
        b.append(T(40, cy + 56, one(s, 27), 17, t["label"], 400, bg=t["cell"]))
        b.append(chevron(w - 52, cy + 38, t["label"]))
        if i < len(ENTRIES) - 1:
            b.append(f'<rect x="40" y="{cy+75.5}" width="{w-60}" height="0.5" fill="{t["sep"]}"/>')
    return svg(w, h, t["bg"], "".join(b))


def iphone_compose(theme):
    """S-03: new entry in a full-height sheet (no grabber; xmark Cancel / filled checkmark Save).
    The input sits above the keyboard so it is never covered (C-16)."""
    t = THEMES[theme]
    w, h = 402, 874
    dim = "#000000"
    b = [status_bar(w, t)]
    b.append(f'<rect width="{w}" height="{h}" fill="{dim}" fill-opacity="{0.25 if theme == "light" else 0.5}"/>')
    sy = 56  # compose sheets use full height only (no medium detent, no grabber)
    sheet = t["cell"] if theme == "light" else "#1C1C1E"   # dark: elevated surface
    field = t["bg"] if theme == "light" else "#2C2C2E"     # dark: elevated secondary
    b.append(f'<path d="M0 {sy+38}a38 38 0 0 1 38 -38h{w-76}a38 38 0 0 1 38 38v{h-sy-38}h-{w}z" fill="{sheet}"/>')
    # iOS 26 sheet buttons are round symbol buttons: xmark (Cancel) leading, filled checkmark (Done) trailing
    cx, cy = 46, sy + 48
    b.append(f'<g aria-label="キャンセル"><circle cx="{cx}" cy="{cy}" r="22" fill="{field}"/>'
             f'<path d="M{cx-7} {cy-7}l14 14M{cx+7} {cy-7}l-14 14" stroke="{t["label"]}" stroke-width="2.4" stroke-linecap="round"/></g>')
    b.append(T(w / 2, sy + 54, "10月24日（土）", 17, t["label"], 600, "middle", bg=sheet))
    cx = w - 46
    b.append(f'<g aria-label="保存"><circle cx="{cx}" cy="{cy}" r="22" fill="{t["accent"]}"/>'
             f'<path d="M{cx-8} {cy+1}l5 6l11 -13" fill="none" stroke="#FFFFFF" stroke-width="2.6" '
             f'stroke-linecap="round" stroke-linejoin="round"/></g>')
    b.append(f'<rect x="24" y="{sy+90}" width="{w-48}" height="120" rx="16" fill="{field}"/>')
    b.append(T(40, sy + 124, "公園の銀杏が色づいてきた。", 17, t["label"], 400, bg=field))
    b.append(f'<rect x="250" y="{sy+108}" width="2" height="22" fill="{t["accent"]}"/>')
    b.append(T(w - 40, sy + 196, "13 / 60文字", 13, t["sec"], 400, "end", op=t["sec_op"], bg=field))
    # Weather (optional): four symbol buttons; the selected one is filled and has a round tint.
    b.append(T(24, sy + 250, "天気", 15, t["sec"], 400, op=t["sec_op"], bg=sheet))
    wy = sy + 290
    sel = t["accent"]  # selected: white filled symbol on an accent circle
    for k in range(4):
        cxk = 46 + k * 60
        b.append(f'<circle cx="{cxk}" cy="{wy}" r="22" fill="{sel if k == 0 else field}"/>')
        col = "#FFFFFF" if k == 0 else t["label"]
        b.append([sun(cxk, wy, col, True), cloud(cxk, wy, col), cloud(cxk, wy - 3, col, "rain"), snow(cxk, wy, col)][k])
    ky = h - 300
    kb = "#D1D3D9" if theme == "light" else "#2C2C2E"
    b.append(f'<rect x="0" y="{ky}" width="{w}" height="300" fill="{kb}"/>')
    b.append(T(w / 2, ky + 150, "（システムのキーボード）", 15, t["label"], 400, "middle", bg=kb))
    return svg(w, h, t["bg"], "".join(b))


def duo_side_column(w, h, t, active=0):
    """Outer display: everything that sits at the top/bottom on other iPhones moves to the
    trailing edge, top to bottom: camera/Dynamic Island, status bar, toolbar, tab bar
    (HIG "Designing for iPhone Duo"). Exact positions are not published: approximation."""
    x = w - 52
    cx = x + 26
    parts = [f'<circle cx="{cx}" cy="34" r="16" fill="#000"/>',
             T(cx, 78, "9:41", 13, t["label"], 600, "middle")]
    # Toolbar: the primary action (symbol only; text buttons stay horizontal).
    parts.append(f'<circle cx="{cx}" cy="112" r="22" fill="{t["glass"]}" fill-opacity="{t["glass_op"]}" '
                 f'stroke="{t["glass_stroke"]}"/>' + symbol_pencil(cx - 12, 100, t["label"]))
    # Tab bar, vertical, at the bottom of the column; the search tab is a separate circle below it
    # (as in Apple's figure).
    th = 3 * 62 + 12
    ty = h - 24 - 54 - th
    parts.append(search_btn(cx, h - 24 - 22, t))
    parts.append(f'<rect x="{x+2}" y="{ty}" width="48" height="{th}" rx="24" fill="{t["glass"]}" '
                 f'fill-opacity="{t["glass_op"]}" stroke="{t["glass_stroke"]}"/>')
    for k, sym in enumerate(("book", "cal", "gear")):
        cy = ty + 6 + 62 * k + 31
        col = t["accent"] if k == active else t["label"]
        if k == active:
            parts.append(f'<rect x="{x+6}" y="{cy-27}" width="40" height="54" rx="20" fill="{t["accent"]}" '
                         f'fill-opacity="0.12"/>')
        parts.append(symbol_filled(sym, cx, cy, col, mix(t["accent"], t["glass"], 0.12) if k == active else t["glass"]))
    return "".join(parts)


def duo_outer(theme):
    t = THEMES[theme]
    w, h = 466, 678
    cw = w - 52  # content width left of the side column
    b = [duo_side_column(w, h, t)]
    b.append(T(20, 64, "日記", 34, t["label"], 700))
    b.append(T(20, 94, "残り 25件（無料版は 30件まで）", 15, t["sec"], 400, op=t["sec_op"]))
    y = 116
    rows = ENTRIES
    b.append(f'<rect x="16" y="{y}" width="{cw-24}" height="{len(rows)*76}" rx="26" fill="{t["cell"]}"/>')
    for i, (d, s) in enumerate(rows):
        cy = y + i * 76
        b.append(T(36, cy + 31, d, 15, t["sec"], 400, op=t["sec_op"], bg=t["cell"]))
        b.append(T(36, cy + 56, one(s, 17), 17, t["label"], 400, bg=t["cell"]))
        b.append(chevron(cw - 30, cy + 38, t["label"]))
        if i < len(rows) - 1:
            b.append(f'<rect x="36" y="{cy+75.5}" width="{cw-60}" height="0.5" fill="{t["sep"]}"/>')
    return svg(w, h, t["bg"], "".join(b))


def duo_inner(theme):
    """Inner display, portrait. Standard horizontal bars (the portrait exception), list and
    detail side by side. The fold runs horizontally across the middle (y = h/2): nothing
    fixed sits on the band; the scrolling list may cross it (data-fold-ok)."""
    t = THEMES[theme]
    w, h = 669, 951
    fold = h / 2
    b = [T(32, 34, "9:41", 15, t["label"], 600),
         f'<rect x="{w-58}" y="22" width="26" height="13" rx="4" fill="none" stroke="{t["label"]}" '
         f'stroke-opacity="0.4"/><rect x="{w-56}" y="24" width="20" height="9" rx="2" fill="{t["label"]}"/>']
    lx, lw = 16, 300          # list pane
    dx = lx + lw + 16          # detail pane
    dw = w - dx - 16
    # Top bar over the detail: 編集 (text) and 今日を書く (symbol). Search is a tab.
    btn = lambda cx, cy: (f'<circle cx="{cx}" cy="{cy}" r="22" fill="{t["glass"]}" '
                          f'fill-opacity="{t["glass_op"]}" stroke="{t["glass_stroke"]}"/>')
    b.append(btn(w - 38, 80) + symbol_pencil(w - 50, 68, t["label"]))
    b.append(trash_btn(w - 38 - 22 - 8 - 22, 80, t))
    eb, ew = text_btn(w - 38 - 22 - 8 - 44 - 8 - 66, 58, "編集", t)
    b.append(eb)
    b.append(T(lx + 4, 148, "日記", 28, t["label"], 700))
    b.append(T(lx + 4, 176, "残り 25件（無料版は 30件まで）", 15, t["sec"], 400, op=t["sec_op"]))
    # Scrolling list: allowed to cross the fold.
    rows = ENTRIES
    ly = 196
    b.append(f'<g data-fold-ok="1"><rect x="{lx}" y="{ly}" width="{lw}" height="{len(rows)*76}" rx="24" '
             f'fill="{t["cell"]}"/>')
    for i, (d, s) in enumerate(rows):
        cy = ly + i * 76
        rowbg = mix(t["accent"], t["cell"], 0.14) if i == 0 else t["cell"]
        if i == 0:
            b.append(f'<rect x="{lx+8}" y="{cy+6}" width="{lw-16}" height="64" rx="18" fill="{rowbg}"/>')
        b.append(T(lx + 20, cy + 31, d, 15, t["sec"], 400, op=t["sec_op"], bg=rowbg))
        b.append(T(lx + 20, cy + 56, one(s, 14), 17, t["label"], 400, bg=rowbg))
    b.append('</g>')
    # Detail: the whole card stays above the fold band.
    d, s = ENTRIES[0]
    b.append(T(dx, 148, d, 28, t["label"], 700))
    b.append(f'<rect x="{dx}" y="196" width="{dw}" height="230" rx="24" fill="{t["cell"]}"/>')
    b.append(T(dx + 20, 238, "公園の銀杏が色づいてきた。", 17, t["label"], 400, bg=t["cell"]))
    b.append(T(dx + 20, 266, "帰りにパン屋へ寄った。", 17, t["label"], 400, bg=t["cell"]))
    b.append(weather_line(dx + 20, 400, t, 15, t["cell"]))
    assert 196 + 230 < fold - 12  # keep the card clear of the fold band
    b.append(tab_bar(w, h, t, maxw=420))
    return svg(w, h, t["bg"], "".join(b))


def duo_inner_landscape(theme, folded=False):
    """Inner display, landscape (as in Apple's Mail example): the list pane keeps its own
    controls at its top; the detail pane's controls and the status bar run down the trailing
    edge. Fully open: list narrower than detail. Partially folded: the fold runs vertically
    down the centre, panes become equal and nothing sits on the fold band."""
    t = THEMES[theme]
    w, h = 951, 669
    side = 52
    cx = w - side / 2
    band = 13
    if folded:
        lw = w / 2 - band - 16
        dx = w / 2 + band
    else:
        lw = 330
        dx = 16 + lw + 16
    dw = w - side - dx - 8
    b = [T(cx, 34, "9:41", 13, t["label"], 600, "middle")]
    # Trailing-edge controls for the detail pane: primary action first, then search.
    b.append(f'<circle cx="{cx}" cy="80" r="22" fill="{t["glass"]}" fill-opacity="{t["glass_op"]}" '
             f'stroke="{t["glass_stroke"]}"/>' + symbol_pencil(cx - 12, 68, t["label"]))
    b.append(trash_btn(cx, 130, t))
    # Tab bar stays on the trailing edge, bottom-aligned (symbols only, as in Apple's figure).
    th = 3 * 62 + 12
    ty = h - 24 - 54 - th
    b.append(search_btn(cx, h - 24 - 22, t))
    b.append(f'<rect x="{cx-24}" y="{ty}" width="48" height="{th}" rx="24" fill="{t["glass"]}" '
             f'fill-opacity="{t["glass_op"]}" stroke="{t["glass_stroke"]}"/>')
    for k, sym in enumerate(("book", "cal", "gear")):
        ky = ty + 6 + 62 * k + 31
        if k == 0:
            b.append(f'<rect x="{cx-20}" y="{ky-27}" width="40" height="54" rx="20" fill="{t["accent"]}" '
                     f'fill-opacity="0.12"/>')
        b.append(symbol_filled(sym, cx, ky, t["accent"] if k == 0 else t["label"],
                               mix(t["accent"], t["glass"], 0.12) if k == 0 else t["glass"]))
    # List pane with its own controls at the top of the pane.
    b.append(f'<rect x="8" y="8" width="{lw+16}" height="{h-16}" rx="28" fill="{t["cell"]}"/>')
    b.append(T(24, 98, "日記", 28, t["label"], 700, bg=t["cell"]))
    b.append(T(24, 126, "残り 25件（無料版は 30件まで）", 15, t["sec"], 400, op=t["sec_op"], bg=t["cell"]))
    for i, (d, s) in enumerate(ENTRIES):
        cy = 146 + i * 76
        rowbg = mix(t["accent"], t["cell"], 0.14) if i == 0 else t["cell"]
        if i == 0:
            b.append(f'<rect x="16" y="{cy+6}" width="{lw}" height="64" rx="18" fill="{rowbg}"/>')
        n = 15 if folded else 16
        b.append(T(32, cy + 31, d, 15, t["sec"], 400, op=t["sec_op"], bg=rowbg))
        b.append(T(32, cy + 56, one(s, n), 17, t["label"], 400, bg=rowbg))
    # Detail pane.
    d, s = ENTRIES[0]
    b.append(T(dx + 8, 98, d, 28, t["label"], 700))
    eb, ew = text_btn(dx + dw - 66, 24, "編集", t)  # text buttons stay in the horizontal bar
    b.append(eb)
    b.append(f'<rect x="{dx}" y="120" width="{dw}" height="190" rx="24" fill="{t["cell"]}"/>')
    b.append(T(dx + 20, 162, "公園の銀杏が色づいてきた。", 17, t["label"], 400, bg=t["cell"]))
    b.append(T(dx + 20, 190, "帰りにパン屋へ寄った。", 17, t["label"], 400, bg=t["cell"]))
    b.append(weather_line(dx + 20, 284, t, 15, t["cell"]))
    return svg(w, h, t["bg"], "".join(b))


def iphone_purchase(theme):
    """S-04: Pro purchase sheet, opened when the free limit (30) is reached. Shows the name,
    one-time purchase (no subscription), local price, restore, terms and privacy links."""
    t = THEMES[theme]
    w, h = 402, 874
    sy = 56
    sheet = t["cell"] if theme == "light" else "#1C1C1E"
    field = t["bg"] if theme == "light" else "#2C2C2E"
    b = [status_bar(w, t),
         f'<rect width="{w}" height="{h}" fill="#000000" fill-opacity="{0.25 if theme == "light" else 0.5}"/>',
         f'<path d="M0 {sy+38}a38 38 0 0 1 38 -38h{w-76}a38 38 0 0 1 38 38v{h-sy-38}h-{w}z" fill="{sheet}"/>']
    cx, cy = 46, sy + 48
    b.append(f'<g aria-label="閉じる"><circle cx="{cx}" cy="{cy}" r="22" fill="{field}"/>'
             f'<path d="M{cx-7} {cy-7}l14 14M{cx+7} {cy-7}l-14 14" stroke="{t["label"]}" stroke-width="2.4" stroke-linecap="round"/></g>')
    b.append(T(32, 190, "30件に達しました", 28, t["label"], 700, bg=sheet))
    b.append(T(32, 226, "無料版で書ける日記は 30件までです。", 17, t["label"], 400, bg=sheet))
    b.append(T(32, 252, "これまでの日記はそのまま残ります。", 17, t["label"], 400, bg=sheet))
    b.append(f'<rect x="20" y="290" width="{w-40}" height="150" rx="26" fill="{field}"/>')
    b.append(T(40, 330, "ひとこと日記 Pro", 20, t["label"], 700, bg=field))
    b.append(T(40, 362, "買い切り（定期的な支払いはありません）", 15, t["sec"], 400, op=t["sec_op"], bg=field))
    b.append(T(40, 390, "日記を無制限に書けます", 17, t["label"], 400, bg=field))
    b.append(T(40, 418, "価格：¥480（税込）", 17, t["label"], 400, bg=field))
    b.append(f'<rect x="20" y="{h-230}" width="{w-40}" height="54" rx="27" fill="{t["accent"]}"/>')
    b.append(T(w / 2, h - 196, "¥480 で購入", 17, "#FFFFFF", 600, "middle", bg=t["accent"]))
    b.append(T(w / 2, h - 140, "購入を復元", 17, t["accent_text"], 400, "middle", bg=sheet))
    b.append(T(w / 2, h - 96, "利用規約 ・ プライバシーポリシー", 15, t["accent_text"], 400, "middle", bg=sheet))
    b.append(f'<rect x="{w/2-70}" y="{h-13}" width="140" height="5" rx="2.5" fill="{t["label"]}"/>')
    return svg(w, h, t["bg"], "".join(b))


def iphone_permission(theme):
    """S-06 state: explanation shown before the system notification dialog (one button, no close)."""
    t = THEMES[theme]
    w, h = 402, 874
    b = [status_bar(w, t)]
    # bell symbol (stand-in for bell.badge)
    b.append(f'<g fill="none" stroke="{t["accent"]}" stroke-width="4" stroke-linejoin="round">'
             f'<path d="M{w/2-34} 330c0-40 14-62 34-66v-6h0v6c20 4 34 26 34 66l10 14h-88z"/>'
             f'<path d="M{w/2-10} 356a10 10 0 0 0 20 0"/></g>')
    b.append(f'<circle cx="{w/2+30}" cy="276" r="11" fill="{t["accent"]}" stroke="{t["bg"]}" stroke-width="4"/>')  # badge
    b.append(T(w / 2, 420, "書き忘れをお知らせします", 28, t["label"], 700, "middle"))
    # Wrapped inside the 20pt side margins.
    for k, line in enumerate(("毎晩、その日のひとことがまだの", "ときに1回だけ通知します。", "時刻は設定で変えられます。")):
        b.append(T(w / 2, 462 + 26 * k, line, 17, t["label"], 400, "middle"))
    b.append(f'<rect x="20" y="{h-130}" width="{w-40}" height="54" rx="27" fill="{t["accent"]}"/>')
    b.append(T(w / 2, h - 96, "続ける", 17, "#FFFFFF", 600, "middle", bg=t["accent"]))
    b.append(f'<rect x="{w/2-70}" y="{h-13}" width="140" height="5" rx="2.5" fill="{t["label"]}"/>')
    return svg(w, h, t["bg"], "".join(b))


def watch_ax3():
    """Largest Watch text size (AX3): Body 23pt. The page scrolls; the button follows the text."""
    w, h = 211, 257
    W = dict(font=WATCH_FONT)
    b = [T(w - 18, 28, "9:41", 15, "#FFFFFF", 600, "end", **W),
         T(w - 18, 58, "今日の", 23, "#0091FF", 600, "end", **W),
         T(w - 18, 86, "ひとこと", 23, "#0091FF", 600, "end", **W),
         f'<rect x="10" y="100" width="{w-20}" height="220" rx="20" fill="#1C1C1E"/>',
         T(22, 136, "公園の銀杏", 23, "#FFFFFF", 400, bg="#1C1C1E", **W),
         T(22, 166, "が色づいて", 23, "#FFFFFF", 400, bg="#1C1C1E", **W),
         T(22, 196, "きた。", 23, "#FFFFFF", 400, bg="#1C1C1E", **W),
         T(22, 226, "帰りにパン", 23, "#FFFFFF", 400, bg="#1C1C1E", **W),
         T(22, 256, "屋へ寄った。", 23, "#FFFFFF", 400, bg="#1C1C1E", **W)]
    return svg(w, h, "#000000", "".join(b))


def mac_calendar(theme):
    """S-05 on Mac (native): UICalendarView is not available on macOS, so a custom month grid.
    Written days have a dot (shape, not colour only); days after today are not selectable."""
    t = THEMES[theme]
    w, h = 1440, 900
    b = [f'<rect x="0" y="0" width="{w}" height="26" fill="{t["bar"]}" fill-opacity="0.9"/>',
         T(20, 18, "ひとこと日記", 13, t["label"], 700, bg=t["bar"])]
    for x, m in ((130, "ファイル"), (196, "編集"), (240, "表示"), (284, "ウインドウ"), (364, "ヘルプ")):
        b.append(T(x, 18, m, 13, t["label"], 400, bg=t["bar"]))
    b.append(T(w - 20, 18, "10月24日(土) 9:41", 13, t["label"], 400, "end", bg=t["bar"]))
    wx, wy, ww, wh = 150, 90, 1140, 720
    b.append(f'<rect x="{wx}" y="{wy}" width="{ww}" height="{wh}" rx="16" fill="{t["win"]}" stroke="{t["glass_stroke"]}"/>')
    sw = 240
    b.append(f'<rect x="{wx+8}" y="{wy+8}" width="{sw}" height="{wh-16}" rx="12" fill="{t["side"]}"/>')
    for i, c in enumerate(("#FF5F57", "#FEBC2E", "#28C840")):
        b.append(f'<circle cx="{wx+28+i*20}" cy="{wy+28}" r="6" fill="{c}"/>')
    b.append(f'<g aria-label="サイドバー" fill="none" stroke="{t["label"]}" stroke-width="1.5"><rect x="{wx+sw-30}" y="{wy+20}" width="18" height="16" rx="3"/>'
             f'<path d="M{wx+sw-24} {wy+20}v16"/></g>')
    for i, (sym, lab, on) in enumerate((("book", "すべての日記", False), ("cal", "カレンダー", True))):
        y = wy + 64 + i * 32
        rowbg = mix(t["accent"], t["side"], 0.16) if on else t["side"]
        if on:
            b.append(f'<rect x="{wx+16}" y="{y}" width="{sw-16}" height="28" rx="6" fill="{rowbg}"/>')
        b.append(symbol(sym, wx + 34, y + 14, t["accent"]).replace('stroke-width="2"', 'stroke-width="1.6"'))
        b.append(T(wx + 52, y + 19, lab, 13, t["label"], 600 if on else 400, bg=rowbg))
    gx = wx + sw + 40
    b.append(T(gx, wy + 26, "カレンダー", 13, t["label"], 700, bg=t["win"]))
    b.append(T(gx, wy + 43, "残り 25件（無料版は 30件まで）", 11, t["sec"], 400, op=t["sec_op"], bg=t["win"]))
    b.append(mac_toolbar(wx, wy, ww, t))  # same toolbar as 「すべての日記」 (a day with an entry is selected)
    b.append(f'<rect x="{gx-8}" y="{wy+52}" width="{ww-sw-56}" height="0.5" fill="{t["sep"]}"/>')
    b.append(T(gx, wy + 100, "2026年10月", 22, t["label"], 700, bg=t["win"]))
    detw = 300  # detail column on the right (S-02 for the selected day)
    cw, ch = (ww - sw - 56 - detw - 24) / 7, 84
    # previous / next month (28pt controls)
    for k, d in enumerate(("M5 -6l-6 6 6 6", "M-5 -6l6 6-6 6")):
        cx = gx + 7 * cw - 58 + k * 44  # 16pt between 28pt buttons so the 44pt hit areas do not overlap
        op = ' stroke-opacity="0.3"' if k == 1 else ""  # next month is disabled in the current month
        b.append(f'<rect x="{cx-14}" y="{wy+78}" width="28" height="28" rx="6" fill="{t["bar"]}"/>'
                 f'<path transform="translate({cx} {wy+92})" d="{d}" fill="none" stroke="{t["label"]}"{op} stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>')
    gy = wy + 130
    for k, d in enumerate("日月火水木金土"):
        b.append(T(gx + k * cw + cw / 2, gy, d, 11, t["sec"], 600, "middle", op=t["sec_op"], bg=t["win"]))
    written = {20, 21, 22, 23, 24}  # 5 entries = 「残り 25件」 (same as the list)
    first = 4  # 1 Oct 2026 is a Thursday
    for day in range(1, 32):
        idx = first + day - 1
        col, row = idx % 7, idx // 7
        cx = gx + col * cw + cw / 2
        cy = gy + 30 + row * ch
        future = day > 24
        selected = day == 20
        if selected:  # selected day: filled accent circle, white Semibold number
            b.append(f'<circle cx="{cx}" cy="{cy}" r="18" fill="{t["accent"]}"/>')
            b.append(T(cx, cy + 5, str(day), 13, "#FFFFFF", 600, "middle", bg=t["accent"]))
        else:
            if day == 24:  # today: accent ring only
                b.append(f'<circle cx="{cx}" cy="{cy}" r="18" fill="none" stroke="{t["accent"]}" stroke-width="1.5"/>')
            b.append(T(cx, cy + 5, str(day), 13, t["sec"] if future else t["label"], 600 if day == 24 else 400,
                       "middle", op=t["sec_op"] if future else None, bg=t["win"]))
        if day in written:
            b.append(f'<circle cx="{cx}" cy="{cy+26}" r="3.5" fill="{t["accent"]}"/>')
    # Detail column: the selected day's entry.
    dxx = wx + ww - detw - 16
    b.append(f'<rect x="{dxx-12}" y="{wy+52}" width="0.5" height="{wh-60}" fill="{t["sep"]}"/>')
    b.append(T(dxx, wy + 96, "10月20日（火）", 22, t["label"], 700, bg=t["win"]))
    b.append(T(dxx, wy + 136, "久しぶりにカレーを作った。", 13, t["label"], 400, bg=t["win"]))
    b.append(T(dxx, wy + 154, "少し辛すぎた。", 13, t["label"], 400, bg=t["win"]))
    b.append(weather_line(dxx, wy + 184, t, 11, t["win"]))
    return svg(w, h, t["desk"], "".join(b))


files = {
    "iphone-S-01-light.svg": iphone_list("light"),
    "iphone-S-01-dark.svg": iphone_list("dark"),
    "iphone-S-02-light.svg": iphone_detail("light"),
    "iphone-S-02-dark.svg": iphone_detail("dark"),
    "ipad-landscape-S-01-light.svg": ipad("light"),
    "ipad-landscape-S-01-dark.svg": ipad("dark"),
    "mac-S-01-light.svg": mac("light"),
    "mac-S-01-dark.svg": mac("dark"),
    "mac-S-05-light.svg": mac_calendar("light"),
    "mac-S-05-dark.svg": mac_calendar("dark"),
    "watch-ultra-S-07.svg": watch(),
    "watch-ultra-S-07-aod.svg": watch_aod(),
    "iphone-duo-outer-S-01-light.svg": duo_outer("light"),
    "iphone-duo-outer-S-01-dark.svg": duo_outer("dark"),
    "iphone-duo-inner-S-01-light.svg": duo_inner("light"),
    "iphone-duo-inner-S-01-dark.svg": duo_inner("dark"),
    "iphone-duo-inner-landscape-S-01-light.svg": duo_inner_landscape("light"),
    "iphone-duo-inner-landscape-S-01-dark.svg": duo_inner_landscape("dark"),
    "iphone-duo-inner-landscape-S-01-folded-light.svg": duo_inner_landscape("light", True),
    "iphone-duo-inner-landscape-S-01-folded-dark.svg": duo_inner_landscape("dark", True),
    "iphone-S-03-light.svg": iphone_compose("light"),
    "iphone-S-03-dark.svg": iphone_compose("dark"),
    "iphone-S-01-empty-light.svg": iphone_empty("light"),
    "iphone-S-01-empty-dark.svg": iphone_empty("dark"),
    "iphone-S-01-ax5-light.svg": iphone_ax5("light"),
    "iphone-S-01-ax5-dark.svg": iphone_ax5("dark"),
    "ipad-narrow-S-01-light.svg": ipad_narrow("light"),
    "ipad-narrow-S-01-dark.svg": ipad_narrow("dark"),
    "iphone-S-04-light.svg": iphone_purchase("light"),
    "iphone-S-04-dark.svg": iphone_purchase("dark"),
    "iphone-S-06-permission-light.svg": iphone_permission("light"),
    "iphone-S-06-permission-dark.svg": iphone_permission("dark"),
    "watch-ultra-S-07-ax3.svg": watch_ax3(),
}
for name, content in files.items():
    (OUT / name).write_text(content, encoding="utf-8")
print(f"wrote {len(files)} SVGs to {OUT}")
