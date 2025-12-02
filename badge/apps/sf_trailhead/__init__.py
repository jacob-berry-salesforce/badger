import sys
import os

sys.path.insert(0, "/system/apps/sf_trailhead")
os.chdir("/system/apps/sf_trailhead")

import math
from badgeware import screen, PixelFont, shapes, brushes, io, run

# Salesforce colors - vibrant palette
sf_blue = brushes.color(0, 161, 224)
sf_darker_blue = brushes.color(0, 95, 178)
sf_green = brushes.color(87, 221, 108)
sf_orange = brushes.color(255, 159, 10)
sf_white = brushes.color(255, 255, 255)
sf_gray = brushes.color(120, 120, 120)
sf_background = brushes.color(250, 250, 255)  # Very light blue

# Load fonts
title_font = PixelFont.load("/system/assets/fonts/absolute.ppf")
body_font = PixelFont.load("/system/assets/fonts/nope.ppf")
small_font = PixelFont.load("/system/assets/fonts/ark.ppf")

# Mock Trailhead data
user_data = {
    "name": "Jacob Berry",
    "rank": "Ranger",
    "points": 12750,
    "badges": 47,
    "trails": 8
}

badges_earned = [
    {"name": "Admin Beginner", "type": "Module", "points": 100},
    {"name": "Lightning Basics", "type": "Module", "points": 100},
    {"name": "Data Modeling", "type": "Trail", "points": 450},
    {"name": "Apex Basics", "type": "Module", "points": 100},
    {"name": "Einstein AI", "type": "Trail", "points": 500},
]


def draw_header():
    """Draw vibrant gradient header"""
    # Orange-to-blue gradient for Trailhead
    for y in range(16):
        progress = y / 16
        r = int(255 + (0 - 255) * progress)
        g = int(140 + (140 - 140) * progress)
        b = int(0 + (210 - 0) * progress)
        screen.brush = brushes.color(r, g, b)
        screen.draw(shapes.rectangle(0, y, 160, 1))

    # Title with shadow
    screen.font = body_font
    screen.brush = brushes.color(0, 0, 0, 100)
    screen.text("Trailhead", 6, 4)
    screen.brush = sf_white
    screen.text("Trailhead", 5, 3)


def draw_stats():
    """Draw vibrant stats card"""
    # Card shadow
    screen.brush = brushes.color(0, 0, 0, 30)
    screen.draw(shapes.rounded_rectangle(7, 20, 150, 88, 6))

    # Main card
    screen.brush = sf_white
    screen.draw(shapes.rounded_rectangle(5, 18, 150, 88, 6))

    # Top gradient accent
    for y in range(4):
        alpha = int(150 - y * 30)
        screen.brush = brushes.color(255, 140, 0, alpha)
        screen.draw(shapes.rectangle(5, 18 + y, 150, 1))

    # User name (bold)
    screen.font = title_font
    screen.brush = sf_darker_blue
    screen.text(user_data["name"], 10, 24)

    # Rank badge with glow
    screen.font = small_font
    rank_text = user_data['rank']
    w, _ = screen.measure_text(rank_text)

    # Glow
    screen.brush = brushes.color(255, 159, 10, 80)
    screen.draw(shapes.rounded_rectangle(7, 36, w + 6, 11, 3))

    # Badge
    screen.brush = sf_orange
    screen.draw(shapes.rounded_rectangle(8, 37, w + 4, 9, 2))
    screen.brush = sf_white
    screen.text(rank_text, 10, 38)

    # Stats grid with colors
    y = 52

    # Points (blue)
    screen.font = title_font
    screen.brush = sf_blue
    screen.text(f"{user_data['points']:,}", 10, y)
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("points", 10, y + 11)

    # Badges (green)
    screen.font = title_font
    screen.brush = sf_green
    screen.text(str(user_data['badges']), 90, y)
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("badges", 90, y + 11)

    # Trails (orange)
    screen.font = title_font
    screen.brush = sf_orange
    screen.text(str(user_data['trails']), 130, y)
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("trails", 130, y + 11)

    # Recent section with divider
    y = 78
    screen.brush = brushes.color(0, 161, 224, 50)
    screen.draw(shapes.rectangle(10, y - 2, 135, 1))

    screen.font = small_font
    screen.brush = sf_darker_blue
    screen.text("RECENT:", 10, y + 2)

    # Show 2 recent badges with colored dots
    y = 90
    for i, badge in enumerate(badges_earned[:2]):
        # Colored dot with glow
        if badge["type"] == "Trail":
            screen.brush = brushes.color(255, 159, 10, 60)
        else:
            screen.brush = brushes.color(0, 161, 224, 60)
        screen.draw(shapes.circle(12, y + 3, 4))

        # Solid dot
        screen.brush = sf_orange if badge["type"] == "Trail" else sf_blue
        screen.draw(shapes.circle(12, y + 3, 2))

        # Badge name
        screen.font = small_font
        screen.brush = sf_darker_blue
        name = badge["name"]
        if len(name) > 16:
            name = name[:16] + ".."
        screen.text(name, 18, y)

        y += 8


def draw_footer():
    """Draw footer with gradient"""
    screen.brush = brushes.color(0, 95, 178, 20)
    screen.draw(shapes.rectangle(0, 108, 160, 12))

    screen.font = small_font
    screen.brush = sf_darker_blue
    screen.text("HOME: Exit", 60, 110)


def update():
    # Clear with light background
    screen.brush = sf_background
    screen.clear()

    # Draw UI
    draw_header()
    draw_stats()
    draw_footer()

    return None


if __name__ == "__main__":
    run(update)
