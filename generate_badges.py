#!/usr/bin/env python3
"""Generate AI Usage Scale badges matching shields.io's SVG structure.

Styles:
  - flat (existing, rx=3, shadow, gradient)
  - flat-square (rx=5, no shadow, no gradient, crispEdges)
  - for-the-badge (height=28, all-caps, bold message, letter-spacing, crispEdges)
"""

import os
import re

LEVELS = [
    (0, "Human", "#2ecc71"),
    (1, "Assisted", "#27ae60"),
    (2, "Co-created", "#3498db"),
    (3, "Directed", "#9b59b6"),
    (4, "Prompted", "#e67e22"),
    (5, "Automated", "#7f8c8d"),
]

LEFT_LABEL = "AI Usage Scale"
RIGHT_LABELS = {
    0: "Level 0 — Human",
    1: "Level 1 — Assisted",
    2: "Level 2 — Co-created",
    3: "Level 3 — Directed",
    4: "Level 4 — Prompted",
    5: "Level 5 — Automated",
}

# shields.io constants
FONT_FAMILY = "Verdana,Geneva,DejaVu Sans,sans-serif"
FONT_SIZE_PX = 11
FONT_SCALE = 10  # shields.io renders at 10× then scales down
TEXT_Y = 140     # baseline at y=140 in scaled coords
HORIZ_PAD = 5

# for-the-badge constants
FTB_FONT_SIZE = 10
FTB_TEXT_Y = 175
FTB_LETTER_SPACING = 1.25
FTB_TEXT_MARGIN = 12
FTB_HEIGHT = 28


def char_width_verdana_11(s):
    """Approximate pixel width of a string at 11px Verdana."""
    # Verdana ~0.55em per char on average at 11px
    return len(s) * 11 * 0.55


def char_width_verdana_10(s):
    """Approximate pixel width of a string at 10px Verdana (for-the-badge)."""
    return len(s) * 10 * 0.55


def brightness_rgb(hex_color):
    """Relative brightness of a hex color (0-1)."""
    h = hex_color.lstrip("#")
    r, g, b = int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255


def text_fill_color(bg_color):
    """Return #fff for dark backgrounds, #333 for light."""
    return "#fff" if brightness_rgb(bg_color) <= 0.69 else "#333"


# ── Flat (existing style) ──────────────────────────────────────────────

def render_flat(level, name, color):
    """Flat style: rx=3, shadow, gradient overlay."""
    label = RIGHT_LABELS[level]
    left_w = len(LEFT_LABEL) * 11 * 0.55 + 2 * HORIZ_PAD
    right_w = len(label) * 11 * 0.55 + 2 * HORIZ_PAD
    total_w = int(left_w + right_w)
    rx = 3

    text_fill = "#fff"
    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{total_w}" height="20" role="img" aria-label="AI Usage Scale: Level {level} — {name}">
  <title>AI Usage Scale: Level {level} — {name}</title>
  <filter id="shadow" x="-10%" y="-10%" width="120%" height="120%">
    <feGaussianBlur in="SourceAlpha" stdDeviation="1.6"/>
    <feOffset dx="0" dy="1" result="offsetblur"/>
    <feComponentTransfer><feFuncA type="linear" slope="0.3"/></feComponentTransfer>
    <feMerge>
      <feMergeNode/>
      <feMergeNode in="SourceGraphic"/>
    </feMerge>
  </filter>
  <linearGradient id="gradient" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-color="#eee" stop-opacity=".1"/>
  </linearGradient>
  <mask id="mask"><rect width="{total_w}" height="20" rx="{rx}" fill="#fff"/></mask>
  <g mask="url(#mask)" filter="url(#shadow)">
    <rect width="{int(left_w)}" height="20" fill="#555"/>
    <rect x="{int(left_w)}" width="{int(right_w)}" height="20" fill="{color}"/>
    <rect width="{total_w}" height="20" fill="url(#gradient)"/>
  </g>
  <g fill="{text_fill}" text-anchor="middle" font-family="{FONT_FAMILY}" font-size="{FONT_SIZE_PX}" text-rendering="geometricPrecision">
    <text x="{int(left_w / 2)}" y="15" aria-hidden="true">{LEFT_LABEL}</text>
    <text x="{int(left_w + right_w / 2)}" y="15" aria-hidden="true">{label}</text>
  </g>
</svg>
'''
    return svg


# ── Flat-square ────────────────────────────────────────────────────────

def render_flat_square(level, name, color):
    """Flat-square: rx=5, no shadow, no gradient, crispEdges."""
    label = RIGHT_LABELS[level]
    left_w = len(LEFT_LABEL) * 11 * 0.55 + 2 * HORIZ_PAD
    right_w = len(label) * 11 * 0.55 + 2 * HORIZ_PAD
    total_w = int(left_w + right_w)
    rx = 5
    text_fill = text_fill_color(color)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{total_w}" height="20" role="img" aria-label="AI Usage Scale: Level {level} — {name}">
  <title>AI Usage Scale: Level {level} — {name}</title>
  <g shape-rendering="crispEdges">
    <rect width="{int(left_w)}" height="20" fill="#555"/>
    <rect x="{int(left_w)}" width="{int(right_w)}" height="20" fill="{color}" rx="{rx}"/>
  </g>
  <g fill="{text_fill}" text-anchor="middle" font-family="{FONT_FAMILY}" font-size="{FONT_SIZE_PX}" text-rendering="geometricPrecision">
    <text x="{int(left_w / 2)}" y="15" aria-hidden="true">{LEFT_LABEL}</text>
    <text x="{int(left_w + right_w / 2)}" y="15" aria-hidden="true">{label}</text>
  </g>
</svg>
'''
    return svg


# ── For-the-badge ──────────────────────────────────────────────────────

def render_for_the_badge(level, name, color):
    """For-the-badge: height=28, all-caps, bold message, letter-spacing."""
    label = RIGHT_LABELS[level]
    label_upper = LEFT_LABEL.upper()
    message_upper = label.upper()
    left_w = len(label_upper) * FTB_LETTER_SPACING + 2 * FTB_TEXT_MARGIN
    right_w = len(message_upper) * FTB_LETTER_SPACING + 2 * FTB_TEXT_MARGIN
    total_w = int(left_w + right_w)
    text_fill = text_fill_color(color)

    svg = f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{total_w}" height="{FTB_HEIGHT}" role="img" aria-label="AI Usage Scale: Level {level} — {name}">
  <title>AI Usage Scale: Level {level} — {name}</title>
  <g shape-rendering="crispEdges">
    <rect width="{int(left_w)}" height="{FTB_HEIGHT}" fill="#555"/>
    <rect x="{int(left_w)}" width="{int(right_w)}" height="{FTB_HEIGHT}" fill="{color}"/>
  </g>
  <g fill="{text_fill}" text-anchor="middle" font-family="{FONT_FAMILY}" text-rendering="geometricPrecision" font-size="{FTB_FONT_SIZE * FONT_SCALE}" transform="scale({1/FONT_SCALE})">
    <text x="{int(left_w / 2)}" y="{FTB_TEXT_Y}" aria-hidden="true">{label_upper}</text>
    <text x="{int(left_w + right_w / 2)}" y="{FTB_TEXT_Y}" font-weight="bold" aria-hidden="true">{message_upper}</text>
  </g>
</svg>
'''
    return svg


def main():
    badge_dir = os.path.join(os.path.dirname(__file__), "badges")
    os.makedirs(badge_dir, exist_ok=True)

    for level, name, color in LEVELS:
        # flat-square
        svg = render_flat_square(level, name, color)
        path = os.path.join(badge_dir, f"flat-square-level-{level}-{name.lower().replace(' ', '-')}.svg")
        with open(path, "w") as f:
            f.write(svg)
        print(f"Created {path}")

        # for-the-badge
        svg = render_for_the_badge(level, name, color)
        path = os.path.join(badge_dir, f"for-the-badge-level-{level}-{name.lower().replace(' ', '-')}.svg")
        with open(path, "w") as f:
            f.write(svg)
        print(f"Created {path}")


if __name__ == "__main__":
    main()
