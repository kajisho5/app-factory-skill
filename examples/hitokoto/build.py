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

THEMES = {
    "light": dict(bg="#F2F2F7", cell="#FFFFFF", label="#000000", sec="#3C3C43", sec_op=0.8,
                  sep="#C6C6C8", accent="#0088FF", glass="#FFFFFF", glass_op=0.82, glass_stroke="#D1D1D6",
                  side="#F2F2F7", desk="#C9D3DF", win="#FFFFFF", bar="#F6F6F6"),
    "dark": dict(bg="#000000", cell="#1C1C1E", label="#FFFFFF", sec="#EBEBF5", sec_op=0.6,
                 sep="#38383A", accent="#0091FF", glass="#2C2C2E", glass_op=0.82, glass_stroke="#48484A",
                 side="#1C1C1E", desk="#1F2633", win="#1E1E1E", bar="#2A2A2A"),
}

ENTRIES = [
    ("10月24日（土）", "公園の銀杏が色づいてきた。帰りにパン屋へ寄った。"),
    ("10月23日（金）", "新しいノートを使い始めた。書き心地がいい。"),
    ("10月22日（木）", "雨。家で本を一冊読み終えた。"),
    ("10月21日（水）", "朝の散歩で猫に会った。"),
    ("10月20日（火）", "久しぶりにカレーを作った。少し辛すぎた。"),
]


def T(x, y, s, size, fill, weight=400, anchor="start", op=None, bg=None):
    o = f' opacity="{op}"' if op is not None else ""
    b = f' data-bg="{bg}"' if bg else ""
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-size="{size}" font-weight="{weight}" '
            f'fill="{fill}" text-anchor="{anchor}"{o}{b}>{escape(s)}</text>')


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
        return (f'<g fill="none" stroke="{c}" stroke-width="2"><rect x="{cx-9}" y="{cy-10}" width="18" '
                f'height="20" rx="2"/><path d="M{cx-4} {cy-10}v20"/></g>')
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


def tab_bar(w, h, t, active=0):
    # Floating Liquid Glass tab bar: navigation only, symbol + one-word label per tab.
    bw, bh = w - 2 * 21, 62
    x, y = 21, h - 34 - bh
    parts = [f'<rect x="{x}" y="{y}" width="{bw}" height="{bh}" rx="31" fill="{t["glass"]}" '
             f'fill-opacity="{t["glass_op"]}" stroke="{t["glass_stroke"]}"/>']
    tabs = [("book", "日記"), ("cal", "カレンダー"), ("gear", "設定")]
    for i, (sym, lab) in enumerate(tabs):
        cx = x + bw * (i + 0.5) / 3
        col = t["accent"] if i == active else t["label"]
        if i == active:
            parts.append(f'<rect x="{cx-52}" y="{y+5}" width="104" height="{bh-10}" rx="26" '
                         f'fill="{t["accent"]}" fill-opacity="0.12"/>')
        parts.append(symbol(sym, cx, y + 22, col))
        parts.append(T(cx, y + 50, lab, 11, col, 600, "middle", bg=t["glass"]))
    return "".join(parts)


def iphone_list(theme):
    t = THEMES[theme]
    w, h = 402, 874
    b = [status_bar(w, t)]
    # Toolbar button (add) top-right, 44x44 hit area.
    b.append(f'<circle cx="{w-38}" cy="84" r="22" fill="{t["glass"]}" fill-opacity="{t["glass_op"]}" '
             f'stroke="{t["glass_stroke"]}"/>' + symbol_pencil(w - 50, 72, t["accent"]))
    b.append(T(20, 150, "日記", 34, t["label"], 700))
    b.append(T(20, 180, "残り 23 件（無料版は 30 件まで）", 15, t["sec"], 400, op=t["sec_op"]))
    y = 204
    b.append(f'<rect x="16" y="{y}" width="{w-32}" height="{len(ENTRIES)*76}" rx="26" fill="{t["cell"]}"/>')
    for i, (d, s) in enumerate(ENTRIES):
        cy = y + i * 76
        b.append(T(36, cy + 31, d, 15, t["sec"], 400, op=t["sec_op"], bg=t["cell"]))
        b.append(T(36, cy + 56, s[:19] + ("…" if len(s) > 19 else ""), 17, t["label"], 400, bg=t["cell"]))
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
    b.append(f'<rect x="{w-106}" y="62" width="84" height="44" rx="22" fill="{t["accent"]}"/>')
    b.append(T(w - 64, 90, "編集", 17, "#FFFFFF", 600, "middle", bg=t["accent"]))
    b.append(T(20, 150, d, 28, t["label"], 700))
    b.append(f'<rect x="16" y="176" width="{w-32}" height="170" rx="26" fill="{t["cell"]}"/>')
    b.append(T(36, 220, "公園の銀杏が色づいてきた。", 17, t["label"], 400, bg=t["cell"]))
    b.append(T(36, 248, "帰りにパン屋へ寄った。", 17, t["label"], 400, bg=t["cell"]))
    b.append(T(36, 318, "晴れ・午後 5:12 に記録", 15, t["sec"], 400, op=t["sec_op"], bg=t["cell"]))
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
    b.append(T(36, 104, "ひとこと日記", 28, t["label"], 700, bg=t["cell"]))
    items = [("book", "すべての日記", True), ("cal", "カレンダー", False), ("gear", "設定", False)]
    for i, (sym, lab, on) in enumerate(items):
        y = 132 + i * 52
        col = t["accent"] if on else t["label"]
        if on:
            b.append(f'<rect x="24" y="{y}" width="{sw-24}" height="44" rx="12" fill="{t["accent"]}" '
                     f'fill-opacity="0.14"/>')
        b.append(symbol(sym, 52, y + 22, col))
        b.append(T(76, y + 28, lab, 17, col, 600 if on else 400, bg=t["cell"]))
    b.append(T(36, h - 40, "残り 23 件（無料版は 30 件まで）", 13, t["sec"], 400, op=t["sec_op"], bg=t["cell"]))
    # List column + detail.
    lx = sw + 36
    lw = 400
    b.append(T(lx, 104, "すべての日記", 34, t["label"], 700))
    b.append(f'<rect x="{lx}" y="128" width="{lw}" height="{len(ENTRIES)*76}" rx="26" fill="{t["cell"]}"/>')
    for i, (d, s) in enumerate(ENTRIES):
        cy = 128 + i * 76
        if i == 0:
            b.append(f'<rect x="{lx+8}" y="{cy+6}" width="{lw-16}" height="64" rx="18" fill="{t["accent"]}" '
                     f'fill-opacity="0.14"/>')
        b.append(T(lx + 20, cy + 31, d, 15, t["sec"], 400, op=t["sec_op"], bg=t["cell"]))
        b.append(T(lx + 20, cy + 56, s[:17] + ("…" if len(s) > 17 else ""), 17, t["label"], 400, bg=t["cell"]))
    dx = lx + lw + 32
    b.append(f'<circle cx="{w-50}" cy="76" r="22" fill="{t["cell"]}" stroke="{t["glass_stroke"]}"/>'
             + symbol_pencil(w - 62, 64, t["accent"]))
    d, s = ENTRIES[0]
    b.append(T(dx, 104, d, 28, t["label"], 700))
    b.append(f'<rect x="{dx}" y="128" width="{w-dx-28}" height="180" rx="26" fill="{t["cell"]}"/>')
    b.append(T(dx + 24, 176, "公園の銀杏が色づいてきた。帰りにパン屋へ寄った。", 17, t["label"], 400, bg=t["cell"]))
    b.append(T(dx + 24, 280, "晴れ・午後 5:12 に記録", 15, t["sec"], 400, op=t["sec_op"], bg=t["cell"]))
    return svg(w, h, t["bg"], "".join(b))


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
    items = [("book", "すべての日記", True), ("cal", "カレンダー", False)]
    for i, (sym, lab, on) in enumerate(items):
        y = wy + 64 + i * 32
        col = t["accent"] if on else t["label"]
        if on:
            b.append(f'<rect x="{wx+16}" y="{y}" width="{sw-16}" height="28" rx="6" fill="{t["accent"]}" '
                     f'fill-opacity="0.16"/>')
        b.append(T(wx + 32, y + 19, lab, 13, col, 600 if on else 400, bg=t["side"]))
    lx = wx + sw + 24
    b.append(T(lx, wy + 34, "すべての日記", 15, t["label"], 700, bg=t["win"]))
    b.append(f'<rect x="{wx+ww-44}" y="{wy+14}" width="28" height="28" rx="6" fill="{t["bar"]}"/>'
             + symbol_pencil(wx + ww - 42, wy + 16, t["accent"], 1.0))
    # Toolbar search field (⌘F), left of the new-entry button.
    sx = wx + ww - 236
    b.append(f'<rect x="{sx}" y="{wy+14}" width="180" height="28" rx="8" fill="{t["bar"]}"/>'
             f'<g fill="none" stroke="{t["sec"]}" stroke-width="1.6"><circle cx="{sx+16}" cy="{wy+27}" r="5"/>'
             f'<path d="M{sx+20} {wy+31}l4 4"/></g>')
    b.append(T(sx + 30, wy + 32, "検索", 13, t["sec"], 400, op=t["sec_op"], bg=t["bar"]))
    b.append(f'<rect x="{lx-8}" y="{wy+52}" width="{ww-sw-32}" height="0.5" fill="{t["sep"]}"/>')
    lw = 320
    for i, (d, s) in enumerate(ENTRIES):
        y = wy + 64 + i * 56
        if i == 0:
            b.append(f'<rect x="{lx-8}" y="{y}" width="{lw}" height="52" rx="8" fill="{t["accent"]}" '
                     f'fill-opacity="0.16"/>')
        b.append(T(lx, y + 20, d, 11, t["sec"], 400, op=t["sec_op"], bg=t["win"]))
        b.append(T(lx, y + 40, s[:20] + ("…" if len(s) > 20 else ""), 13, t["label"], 400, bg=t["win"]))
    dx = lx + lw + 24
    b.append(f'<rect x="{dx-12}" y="{wy+52}" width="0.5" height="{wh-60}" fill="{t["sep"]}"/>')
    d, s = ENTRIES[0]
    b.append(T(dx, wy + 96, d, 22, t["label"], 700, bg=t["win"]))
    b.append(T(dx, wy + 136, s, 13, t["label"], 400, bg=t["win"]))
    b.append(T(dx, wy + 166, "晴れ・午後 5:12 に記録", 11, t["sec"], 400, op=t["sec_op"], bg=t["win"]))
    return svg(w, h, t["desk"], "".join(b))


def watch():
    w, h = 211, 257
    b = [T(w - 18, 28, "9:41", 15, "#FFFFFF", 600, "end"),
         T(16, 62, "今日のひとこと", 16, "#0091FF", 600),
         f'<rect x="10" y="76" width="{w-20}" height="96" rx="20" fill="#1C1C1E"/>',
         T(22, 106, "公園の銀杏が", 16, "#FFFFFF", 400, bg="#1C1C1E"),
         T(22, 130, "色づいてきた。", 16, "#FFFFFF", 400, bg="#1C1C1E"),
         T(22, 158, "午後 5:12", 13, "#EBEBF5", 400, op=0.6, bg="#1C1C1E"),
         f'<rect x="10" y="186" width="{w-20}" height="50" rx="25" fill="#0091FF"/>',
         T(w / 2, 217, "音声で書く", 16, "#FFFFFF", 600, "middle", bg="#0091FF")]
    return svg(w, h, "#000000", "".join(b))


def watch_aod():
    """Always On (wrist down): dimmed, no diary text, only whether today is recorded."""
    w, h = 211, 257
    b = [T(w - 18, 28, "9:41", 15, "#AEAEB2", 600, "end"),
         T(16, 62, "今日のひとこと", 16, "#5E9EDB", 600),
         f'<rect x="10" y="76" width="{w-20}" height="96" rx="20" fill="#0D0D0F"/>',
         T(22, 118, "記録済み", 22, "#AEAEB2", 600, bg="#0D0D0F"),
         T(22, 150, "手首を上げると表示", 13, "#8E8E93", 400, bg="#0D0D0F")]
    return svg(w, h, "#000000", "".join(b))


def iphone_empty(theme):
    t = THEMES[theme]
    w, h = 402, 874
    b = [status_bar(w, t)]
    b.append(f'<circle cx="{w-38}" cy="84" r="22" fill="{t["glass"]}" fill-opacity="{t["glass_op"]}" '
             f'stroke="{t["glass_stroke"]}"/>' + symbol_pencil(w - 50, 72, t["accent"]))
    b.append(T(20, 150, "日記", 34, t["label"], 700))
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
    Rows stack and wrap instead of truncating; the tab bar keeps its own system size."""
    t = THEMES[theme]
    w, h = 402, 874
    b = [status_bar(w, t)]
    b.append(f'<circle cx="{w-38}" cy="84" r="22" fill="{t["glass"]}" fill-opacity="{t["glass_op"]}" '
             f'stroke="{t["glass_stroke"]}"/>' + symbol_pencil(w - 50, 72, t["accent"]))
    b.append(T(20, 176, "日記", 60, t["label"], 700))
    b.append(f'<rect x="16" y="206" width="{w-32}" height="490" rx="26" fill="{t["cell"]}"/>')
    lines = [("10月24日", 49, "sec"), ("（土）", 49, "sec"), ("公園の", 53, "label"),
             ("銀杏が色づ", 53, "label"), ("いてきた。", 53, "label"), ("帰りに…", 53, "label")]
    y = 270
    for text, size, kind in lines:
        if kind == "sec":
            b.append(T(36, y, text, size, t["sec"], 400, op=t["sec_op"], bg=t["cell"]))
        else:
            b.append(T(36, y, text, size, t["label"], 400, bg=t["cell"]))
        y += 70
    b.append(tab_bar(w, h, t))
    b.append(f'<rect x="{w/2-70}" y="{h-13}" width="140" height="5" rx="2.5" fill="{t["label"]}"/>')
    return svg(w, h, t["bg"], "".join(b))


def ipad_narrow(theme):
    """Narrow iPad window: the sidebar collapses to a button, the list fills the width."""
    t = THEMES[theme]
    w, h = 600, 1032
    b = [T(24, 34, "9:41", 15, t["label"], 600)]
    b.append(f'<circle cx="44" cy="80" r="22" fill="{t["cell"]}" stroke="{t["glass_stroke"]}"/>'
             f'<g fill="none" stroke="{t["label"]}" stroke-width="2"><rect x="33" y="70" width="22" height="20" rx="3"/>'
             f'<path d="M41 70v20"/></g>')
    b.append(f'<circle cx="{w-44}" cy="80" r="22" fill="{t["cell"]}" stroke="{t["glass_stroke"]}"/>'
             + symbol_pencil(w - 56, 68, t["accent"]))
    b.append(T(24, 150, "すべての日記", 34, t["label"], 700))
    b.append(T(24, 180, "残り 23 件（無料版は 30 件まで）", 15, t["sec"], 400, op=t["sec_op"]))
    b.append(f'<rect x="20" y="204" width="{w-40}" height="{len(ENTRIES)*76}" rx="26" fill="{t["cell"]}"/>')
    for i, (d, s) in enumerate(ENTRIES):
        cy = 204 + i * 76
        b.append(T(40, cy + 31, d, 15, t["sec"], 400, op=t["sec_op"], bg=t["cell"]))
        b.append(T(40, cy + 56, s[:28] + ("…" if len(s) > 28 else ""), 17, t["label"], 400, bg=t["cell"]))
        if i < len(ENTRIES) - 1:
            b.append(f'<rect x="40" y="{cy+75.5}" width="{w-60}" height="0.5" fill="{t["sep"]}"/>')
    return svg(w, h, t["bg"], "".join(b))


def iphone_compose(theme):
    """S-03: new entry in a sheet (medium detent, grabber, Cancel / prominent Save).
    The input sits above the keyboard so it is never covered (C-16)."""
    t = THEMES[theme]
    w, h = 402, 874
    dim = "#000000"
    b = [status_bar(w, t)]
    b.append(T(20, 150, "日記", 34, t["label"], 700))
    b.append(f'<rect width="{w}" height="{h}" fill="{dim}" fill-opacity="{0.25 if theme == "light" else 0.5}"/>')
    sy = 300
    b.append(f'<rect x="8" y="{sy}" width="{w-16}" height="{h-sy+40}" rx="38" fill="{t["cell"]}"/>')
    b.append(f'<rect x="{w/2-18}" y="{sy+8}" width="36" height="5" rx="2.5" fill="{t["sep"]}"/>')
    b.append(f'<rect x="24" y="{sy+26}" width="96" height="44" rx="22" fill="{t["bg"]}"/>')
    b.append(T(72, sy + 54, "キャンセル", 15, t["label"], 400, "middle", bg=t["bg"]))
    b.append(T(w / 2, sy + 54, "10月24日（土）", 17, t["label"], 600, "middle", bg=t["cell"]))
    b.append(f'<rect x="{w-104}" y="{sy+26}" width="80" height="44" rx="22" fill="{t["accent"]}"/>')
    b.append(T(w - 64, sy + 54, "保存", 17, "#FFFFFF", 600, "middle", bg=t["accent"]))
    b.append(f'<rect x="24" y="{sy+90}" width="{w-48}" height="120" rx="16" fill="{t["bg"]}"/>')
    b.append(T(40, sy + 124, "公園の銀杏が色づいてきた。", 17, t["label"], 400, bg=t["bg"]))
    b.append(f'<rect x="250" y="{sy+108}" width="2" height="22" fill="{t["accent"]}"/>')
    b.append(T(w - 40, sy + 196, "13 / 60文字", 13, t["sec"], 400, "end", op=t["sec_op"], bg=t["bg"]))
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
    parts = [f'<rect x="{cx-7}" y="16" width="14" height="40" rx="7" fill="#000"/>',
             T(cx, 78, "9:41", 13, t["label"], 600, "middle")]
    # Toolbar: primary action first, then search. Symbols only (text buttons stay horizontal).
    for k, y0 in enumerate((112, 162)):
        parts.append(f'<circle cx="{cx}" cy="{y0}" r="22" fill="{t["glass"]}" fill-opacity="{t["glass_op"]}" '
                     f'stroke="{t["glass_stroke"]}"/>')
        if k == 0:
            parts.append(symbol_pencil(cx - 12, y0 - 12, t["accent"]))
        else:
            parts.append(f'<g fill="none" stroke="{t["label"]}" stroke-width="2"><circle cx="{cx-2}" cy="{y0-2}" r="7"/>'
                         f'<path d="M{cx+3} {y0+3}l5 5"/></g>')
    # Tab bar, vertical, at the bottom of the column.
    th = 3 * 62 + 12
    ty = h - 24 - th
    parts.append(f'<rect x="{x+2}" y="{ty}" width="48" height="{th}" rx="24" fill="{t["glass"]}" '
                 f'fill-opacity="{t["glass_op"]}" stroke="{t["glass_stroke"]}"/>')
    for k, sym in enumerate(("book", "cal", "gear")):
        cy = ty + 6 + 62 * k + 31
        col = t["accent"] if k == active else t["label"]
        if k == active:
            parts.append(f'<rect x="{x+6}" y="{cy-27}" width="40" height="54" rx="20" fill="{t["accent"]}" '
                         f'fill-opacity="0.12"/>')
        parts.append(symbol(sym, cx, cy, col))
    return "".join(parts)


def duo_outer(theme):
    t = THEMES[theme]
    w, h = 466, 678
    cw = w - 52  # content width left of the side column
    b = [duo_side_column(w, h, t)]
    b.append(T(20, 64, "日記", 34, t["label"], 700))
    b.append(T(20, 94, "残り 23 件（無料版は 30 件まで）", 15, t["sec"], 400, op=t["sec_op"]))
    y = 116
    rows = ENTRIES
    b.append(f'<rect x="16" y="{y}" width="{cw-24}" height="{len(rows)*76}" rx="26" fill="{t["cell"]}"/>')
    for i, (d, s) in enumerate(rows):
        cy = y + i * 76
        b.append(T(36, cy + 31, d, 15, t["sec"], 400, op=t["sec_op"], bg=t["cell"]))
        b.append(T(36, cy + 56, s[:19] + ("…" if len(s) > 19 else ""), 17, t["label"], 400, bg=t["cell"]))
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
    # Top bar: sidebar toggle + search over the list, "今日を書く" over the detail.
    btn = lambda cx, cy: (f'<circle cx="{cx}" cy="{cy}" r="22" fill="{t["glass"]}" '
                          f'fill-opacity="{t["glass_op"]}" stroke="{t["glass_stroke"]}"/>')
    b.append(btn(lx + 22, 80) + f'<g fill="none" stroke="{t["label"]}" stroke-width="2">'
             f'<rect x="{lx+11}" y="70" width="22" height="20" rx="3"/><path d="M{lx+19} 70v20"/></g>')
    b.append(btn(lx + 72, 80) + f'<g fill="none" stroke="{t["label"]}" stroke-width="2">'
             f'<circle cx="{lx+70}" cy="78" r="7"/><path d="M{lx+75} 83l5 5"/></g>')
    b.append(f'<rect x="{w-140}" y="58" width="124" height="44" rx="22" fill="{t["accent"]}"/>')
    b.append(T(w - 78, 86, "今日を書く", 17, "#FFFFFF", 600, "middle", bg=t["accent"]))
    b.append(T(lx + 4, 148, "すべての日記", 28, t["label"], 700))
    b.append(T(lx + 4, 176, "残り 23 件", 15, t["sec"], 400, op=t["sec_op"]))
    # Scrolling list: allowed to cross the fold.
    rows = ENTRIES
    ly = 196
    b.append(f'<g data-fold-ok="1"><rect x="{lx}" y="{ly}" width="{lw}" height="{len(rows)*76}" rx="24" '
             f'fill="{t["cell"]}"/>')
    for i, (d, s) in enumerate(rows):
        cy = ly + i * 76
        if i == 0:
            b.append(f'<rect x="{lx+8}" y="{cy+6}" width="{lw-16}" height="64" rx="18" fill="{t["accent"]}" '
                     f'fill-opacity="0.14"/>')
        b.append(T(lx + 20, cy + 31, d, 15, t["sec"], 400, op=t["sec_op"], bg=t["cell"]))
        b.append(T(lx + 20, cy + 56, s[:14] + ("…" if len(s) > 14 else ""), 17, t["label"], 400, bg=t["cell"]))
    b.append('</g>')
    # Detail: the whole card stays above the fold band.
    d, s = ENTRIES[0]
    b.append(T(dx, 148, d, 28, t["label"], 700))
    b.append(f'<rect x="{dx}" y="196" width="{dw}" height="230" rx="24" fill="{t["cell"]}"/>')
    b.append(T(dx + 20, 238, "公園の銀杏が色づいてきた。", 17, t["label"], 400, bg=t["cell"]))
    b.append(T(dx + 20, 266, "帰りにパン屋へ寄った。", 17, t["label"], 400, bg=t["cell"]))
    b.append(T(dx + 20, 400, "晴れ・午後 5:12 に記録", 15, t["sec"], 400, op=t["sec_op"], bg=t["cell"]))
    assert 196 + 230 < fold - 12  # keep the card clear of the fold band
    # Below the fold: a secondary section that starts after the band.
    b.append(T(dx, 540, "1年前の今日", 20, t["label"], 700))
    b.append(f'<rect x="{dx}" y="556" width="{dw}" height="96" rx="24" fill="{t["cell"]}"/>')
    b.append(T(dx + 20, 596, "前年10月24日（架空）", 15, t["sec"], 400, op=t["sec_op"], bg=t["cell"]))
    b.append(T(dx + 20, 624, "雨。駅まで歩いた。", 17, t["label"], 400, bg=t["cell"]))
    return svg(w, h, t["bg"], "".join(b))


files = {
    "iphone-S-01-light.svg": iphone_list("light"),
    "iphone-S-01-dark.svg": iphone_list("dark"),
    "iphone-S-02-light.svg": iphone_detail("light"),
    "iphone-S-02-dark.svg": iphone_detail("dark"),
    "ipad-landscape-S-01-light.svg": ipad("light"),
    "ipad-landscape-S-01-dark.svg": ipad("dark"),
    "mac-S-01-light.svg": mac("light"),
    "mac-S-01-dark.svg": mac("dark"),
    "watch-ultra-S-01.svg": watch(),
    "watch-ultra-S-01-aod.svg": watch_aod(),
    "iphone-duo-outer-S-01-light.svg": duo_outer("light"),
    "iphone-duo-outer-S-01-dark.svg": duo_outer("dark"),
    "iphone-duo-inner-S-01-light.svg": duo_inner("light"),
    "iphone-duo-inner-S-01-dark.svg": duo_inner("dark"),
    "iphone-S-03-light.svg": iphone_compose("light"),
    "iphone-S-03-dark.svg": iphone_compose("dark"),
    "iphone-S-01-empty-light.svg": iphone_empty("light"),
    "iphone-S-01-empty-dark.svg": iphone_empty("dark"),
    "iphone-S-01-light-ax5.svg": iphone_ax5("light"),
    "ipad-narrow-S-01-light.svg": ipad_narrow("light"),
    "ipad-narrow-S-01-dark.svg": ipad_narrow("dark"),
}
for name, content in files.items():
    (OUT / name).write_text(content, encoding="utf-8")
print(f"wrote {len(files)} SVGs to {OUT}")
