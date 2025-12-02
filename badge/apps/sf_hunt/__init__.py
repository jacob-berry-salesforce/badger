import sys
import os

sys.path.insert(0, "/system/apps/sf_hunt")
os.chdir("/system/apps/sf_hunt")

import math
import random
from badgeware import screen, PixelFont, shapes, brushes, io, run

# Salesforce colors
sf_blue = brushes.color(0, 161, 224)
sf_darker_blue = brushes.color(3, 45, 96)
sf_green = brushes.color(87, 221, 108)
sf_orange = brushes.color(255, 159, 10)
sf_purple = brushes.color(110, 68, 255)
sf_white = brushes.color(255, 255, 255)
sf_gray = brushes.color(120, 120, 120)
sf_background = brushes.color(250, 250, 255)

# Load fonts
title_font = PixelFont.load("/system/assets/fonts/absolute.ppf")
body_font = PixelFont.load("/system/assets/fonts/nope.ppf")
small_font = PixelFont.load("/system/assets/fonts/ark.ppf")

# Collectibles
collectibles = [
    {"name": "Retail Lightning", "zone": "Retail AI", "collected": True, "points": 10},
    {"name": "FINS Waterfall", "zone": "FINS", "collected": True, "points": 15},
    {"name": "Discovery Beacon", "zone": "Discovery", "collected": False, "points": 10},
    {"name": "Innovation Spark", "zone": "Innovation", "collected": False, "points": 20},
    {"name": "Einstein Brain", "zone": "AI Lab", "collected": False, "points": 25},
]

# State
view = "map"  # "map" or "leaderboard"
nearby_item = None
confetti_time = 0

# Leaderboard
leaderboard = [
    {"name": "Sarah Chen", "points": 85},
    {"name": "Marcus Rivera", "points": 75},
    {"name": "You", "points": 25},
    {"name": "Emma Walsh", "points": 20},
    {"name": "Dev Patel", "points": 15},
]


def draw_header():
    """Draw hunt header"""
    # Gradient header
    for y in range(14):
        progress = y / 14
        r = int(255 + (110 - 255) * progress)
        g = int(159 + (68 - 159) * progress)
        b = int(10 + (255 - 10) * progress)
        screen.brush = brushes.color(r, g, b)
        screen.draw(shapes.rectangle(0, y, 160, 1))

    screen.font = body_font
    screen.brush = sf_white
    screen.text("Scavenger Hunt", 5, 3)


def draw_map():
    """Draw collectibles map/list"""
    draw_header()

    # Progress summary
    collected = sum(1 for item in collectibles if item["collected"])
    total = len(collectibles)
    total_points = sum(item["points"] for item in collectibles if item["collected"])

    y = 18
    screen.font = small_font
    screen.brush = sf_gray
    screen.text(f"COLLECTED: {collected}/{total}", 10, y)

    screen.font = body_font
    screen.brush = sf_green
    screen.text(f"{total_points} pts", 110, y)

    # Collectibles list
    y = 32
    for i, item in enumerate(collectibles[:4]):  # Show 4 items
        # Item card
        card_color = sf_white if not item["collected"] else brushes.color(240, 255, 240)
        screen.brush = card_color
        screen.draw(shapes.rounded_rectangle(10, y, 140, 16, 4))

        # Checkbox
        checkbox_x = 15
        checkbox_y = y + 5
        screen.brush = sf_green if item["collected"] else brushes.color(220, 220, 220)
        screen.draw(shapes.rounded_rectangle(checkbox_x, checkbox_y, 8, 8, 2))

        if item["collected"]:
            # Checkmark
            screen.brush = sf_white
            screen.draw(shapes.line(checkbox_x + 2, checkbox_y + 4, checkbox_x + 3, checkbox_y + 6, 2))
            screen.draw(shapes.line(checkbox_x + 3, checkbox_y + 6, checkbox_x + 6, checkbox_y + 2, 2))

        # Item name
        screen.font = small_font
        screen.brush = sf_darker_blue if not item["collected"] else sf_gray
        screen.text(item["name"], 28, y + 3)

        # Zone + points
        screen.brush = sf_gray
        screen.text(f"{item['zone']} • {item['points']}pts", 28, y + 11)

        y += 18

    # Footer
    screen.font = small_font
    screen.brush = sf_orange
    screen.text("B: Collect", 10, 110)
    screen.brush = sf_gray
    screen.text("C: Leaderboard", 75, 110)


def draw_leaderboard():
    """Draw leaderboard"""
    draw_header()

    # Title
    y = 20
    screen.font = small_font
    screen.brush = sf_gray
    text = "TOP HUNTERS"
    w, _ = screen.measure_text(text)
    screen.text(text, 80 - w // 2, y)

    # Leaderboard entries
    y = 32
    for i, entry in enumerate(leaderboard[:5]):
        # Rank badge
        rank = i + 1
        if rank == 1:
            badge_color = brushes.color(255, 215, 0)  # Gold
        elif rank == 2:
            badge_color = brushes.color(192, 192, 192)  # Silver
        elif rank == 3:
            badge_color = brushes.color(205, 127, 50)  # Bronze
        else:
            badge_color = sf_gray

        # Highlight current user
        if entry["name"] == "You":
            screen.brush = brushes.color(240, 255, 240)
            screen.draw(shapes.rounded_rectangle(8, y - 2, 144, 16, 4))

        # Rank
        screen.brush = badge_color
        screen.draw(shapes.circle(18, y + 5, 7))
        screen.font = small_font
        screen.brush = sf_white
        rank_text = str(rank)
        w, _ = screen.measure_text(rank_text)
        screen.text(rank_text, 18 - w // 2, y + 2)

        # Name
        screen.font = small_font
        screen.brush = sf_darker_blue
        screen.text(entry["name"], 30, y + 2)

        # Points
        screen.font = body_font
        screen.brush = sf_orange
        points_text = str(entry["points"])
        w, _ = screen.measure_text(points_text)
        screen.text(points_text, 145 - w, y)

        y += 17

    # Footer
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("A: Back to Map", 45, 110)


def draw_confetti():
    """Draw collection animation"""
    # Simple confetti particles
    for i in range(10):
        x = (io.ticks * 2 + i * 16) % 160
        y = ((io.ticks + i * 100) // 10) % 120
        colors = [sf_blue, sf_green, sf_orange, sf_purple]
        screen.brush = colors[i % len(colors)]
        screen.draw(shapes.circle(x, y, 2))


def update():
    global view, nearby_item, confetti_time

    # Simulate nearby collectible detection (random)
    if view == "map" and random.random() < 0.01:
        uncollected = [item for item in collectibles if not item["collected"]]
        if uncollected:
            nearby_item = uncollected[0]

    # Handle collection
    if view == "map" and io.BUTTON_B in io.pressed and nearby_item:
        nearby_item["collected"] = True
        confetti_time = io.ticks
        nearby_item = None

    # View switching
    if io.BUTTON_C in io.pressed and view == "map":
        view = "leaderboard"
    elif io.BUTTON_A in io.pressed and view == "leaderboard":
        view = "map"

    # Clear screen
    screen.brush = sf_background
    screen.clear()

    # Show confetti animation briefly after collection
    if confetti_time > 0 and (io.ticks - confetti_time) < 1000:
        draw_confetti()

    # Draw current view
    if view == "map":
        draw_map()
        # Show nearby prompt
        if nearby_item:
            screen.font = small_font
            screen.brush = sf_green
            prompt = f"Tap B: {nearby_item['name']}!"
            w, _ = screen.measure_text(prompt)
            screen.text(prompt, 80 - w // 2, 95)
    else:
        draw_leaderboard()

    return None


if __name__ == "__main__":
    run(update)
