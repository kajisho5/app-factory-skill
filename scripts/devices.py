"""Canvas sizes shared by frame.py / export_png.py / check_mocks.py.

Values come from App Store Connect "Screenshot specifications" (pixels) divided by the
device scale factor. See references/hig-specs.md for sources. Re-check on major OS updates.
"""

# name: (width_pt, height_pt, scale, platform)
CANVASES = {
    "iphone":           (402, 874, 3, "ios"),
    "iphone-small":     (393, 852, 3, "ios"),
    "iphone-large":     (440, 956, 3, "ios"),
    "ipad-landscape":   (1376, 1032, 2, "ios"),
    "ipad-portrait":    (1032, 1376, 2, "ios"),
    "mac":              (1440, 900, 2, "macos"),
    "watch-ultra":      (211, 257, 2, "watchos"),
    "watch":            (198, 242, 2, "watchos"),
    # iPhone Duo (foldable, 2026). Pixel sizes are the App Store screenshot sizes;
    # the @3x scale is an assumption (Apple has not published point sizes).
    "iphone-duo-outer":           (466, 678, 3, "ios"),
    "iphone-duo-outer-landscape": (678, 466, 3, "ios"),
    "iphone-duo-inner":           (669, 951, 3, "ios"),
    "iphone-duo-inner-landscape": (951, 669, 3, "ios"),
    # Two framed phones side by side for marketing images (made by frame.py pair).
    "pair":                       (1600, 1000, 2, "ios"),
    # Not a screenshot size: an example of a narrow iPad window (windows resize freely).
    "ipad-narrow":      (600, 1032, 2, "ios"),
}

# Minimum text size in pt (HIG Accessibility).
MIN_FONT_PT = {"ios": 11, "macos": 10, "watchos": 12}


def canvas_for(filename: str):
    """Pick the canvas from a mock file name such as 'iphone-S-01-light.svg'.

    The longest matching prefix wins, so 'ipad-landscape-...' beats 'ipad'.
    Files starting with 'framed-' (device-frame presentations) have no canvas.
    """
    base = filename.rsplit("/", 1)[-1]
    if base.startswith("framed-"):
        return None  # presentation image made by frame.py, not a screen mock
    best = None
    for name in CANVASES:
        if base.startswith(name + "-"):
            if best is None or len(name) > len(best):
                best = name
    return best
