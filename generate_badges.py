#!/usr/bin/env python3
"""Generate AI Usage Scale badges in flat-square and for-the-badge styles."""

import os

LEVELS = [
    (0, "Human", "#2ecc71"),
    (1, "Assisted", "#27ae60"),
    (2, "Co-created", "#3498db"),
    (3, "Directed", "#9b59b6"),
    (4, "Prompted", "#e67e22"),
    (5, "Automated", "#7f8c8d"),
]

LEFT_TEXT = "AI Usage Scale"
RIGHT_LABELS = {
    0: "Level 0 — Human",
    1: "Level 1 — Assisted",
    2: "Level 2 — Co-created",
    3: "Level 3 — Directed",
    4: "Level 4 — Prompted",
    5: "Level 5 — Automated",
}


def text_width(text, font_size=11):
    """Approximate text width in pixels (Verdana ~0.6em per char)."""
    return len(text) * font_size * 0.6


def make_flat_square(level, name, color):
    """Flat-square style: rounded corners (rx=5), same height as flat."""
    label = RIGHT_LABELS[level]
    left_w = 127
    right_w = int(text_width(label, 11)) + 14
    total_w = left_w + right_w
    rx = 5

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{total_w}" height="20" role="img" aria-label="AI Usage Scale: Level {level} — {name}">
  <title>AI Usage Scale: Level {level} — {name}</title>
  <linearGradient id="a" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-color="#bbb" stop-opacity=".1"/>
  </linearGradient>
  <mask id="m"><rect width="{total_w}" height="20" rx="{rx}" fill="#fff"/></mask>
  <g mask="url(#m)">
    <rect width="{left_w}" height="20" fill="#555"/>
    <rect x="{left_w}" width="{right_w}" height="20" fill="{color}"/>
    <rect width="{total_w}" height="20" fill="url(#a)"/>
  </g>
  <g fill="#fff" text-anchor="start" font-family="Verdana,Genova,Tahoma, sans-serif" font-size="11" text-rendering="geometricPrecision">
    <text x="6" y="15" transform="scale(.97)" aria-hidden="true">{LEFT_TEXT}</text>
    <text x="{left_w + 7}" y="15" transform="scale(.97)" aria-hidden="true">{label}</text>
  </g>
</svg>
'''


def make_for_the_badge(level, name, color):
    """For-the-badge style: taller (30px), wider proportions, bolder look."""
    label = RIGHT_LABELS[level]
    left_w = 150
    right_w = int(text_width(label, 13)) + 20
    total_w = left_w + right_w
    h = 30

    return f'''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{total_w}" height="{h}" role="img" aria-label="AI Usage Scale: Level {level} — {name}">
  <title>AI Usage Scale: Level {level} — {name}</title>
  <linearGradient id="a" x2="0" y2="100%">
    <stop offset="0" stop-color="#bbb" stop-opacity=".1"/>
    <stop offset="1" stop-color="#bbb" stop-opacity=".1"/>
  </linearGradient>
  <mask id="m"><rect width="{total_w}" height="{h}" rx="4" fill="#fff"/></mask>
  <g mask="url(#m)">
    <rect width="{left_w}" height="{h}" fill="#333"/>
    <rect x="{left_w}" width="{right_w}" height="{h}" fill="{color}"/>
    <rect width="{total_w}" height="{h}" fill="url(#a)"/>
  </g>
  <g fill="#fff" text-anchor="start" font-family="Verdana,Genova,Tahoma, sans-serif" font-size="13" font-weight="bold" text-rendering="geometricPrecision">
    <text x="7" y="20" transform="scale(.97)" aria-hidden="true">{LEFT_TEXT}</text>
    <text x="{left_w + 10}" y="20" transform="scale(.97)" aria-hidden="true">{label}</text>
  </g>
</svg>
'''


def main():
    badge_dir = os.path.join(os.path.dirname(__file__), "badges")
    os.makedirs(badge_dir, exist_ok=True)

    for level, name, color in LEVELS:
        # flat-square
        svg = make_flat_square(level, name, color)
        path = os.path.join(badge_dir, f"flat-square-level-{level}-{name.lower().replace(' ', '-')}.svg")
        with open(path, "w") as f:
            f.write(svg)
        print(f"Created {path}")

        # for-the-badge
        svg = make_for_the_badge(level, name, color)
        path = os.path.join(badge_dir, f"for-the-badge-level-{level}-{name.lower().replace(' ', '-')}.svg")
        with open(path, "w") as f:
            f.write(svg)
        print(f"Created {path}")


if __name__ == "__main__":
    main()
