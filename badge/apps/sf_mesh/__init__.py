import sys
import os

sys.path.insert(0, "/system/apps/sf_mesh")
os.chdir("/system/apps/sf_mesh")

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

# View state
view = "people"  # "people" or "demos"

# Mock nearby data
nearby_people = [
    {"role": "Solutions Engineer", "company": "Acme Corp", "rssi": -45},
    {"role": "Data Architect", "company": "TechStart", "rssi": -58},
    {"role": "VP Engineering", "company": "BuildCo", "rssi": -62},
]

nearby_demos = [
    {"name": "Retail AI Mirror", "zone": "Retail", "wait": 2},
    {"name": "F1 Simulator", "zone": "Discovery", "wait": 5},
    {"name": "Turing Test", "zone": "Innovation", "wait": 1},
]


def draw_header():
    """Draw mesh header"""
    # Purple gradient
    for y in range(14):
        progress = y / 14
        r = int(110 + (0 - 110) * progress)
        g = int(68 + (161 - 68) * progress)
        b = int(255 + (224 - 255) * progress)
        screen.brush = brushes.color(r, g, b)
        screen.draw(shapes.rectangle(0, y, 160, 1))

    screen.font = body_font
    screen.brush = sf_white
    screen.text("Nearby", 5, 3)

    # Tab indicators
    screen.font = small_font
    if view == "people":
        screen.brush = sf_white
    else:
        screen.brush = brushes.color(255, 255, 255, 128)
    screen.text("People", 95, 4)

    if view == "demos":
        screen.brush = sf_white
    else:
        screen.brush = brushes.color(255, 255, 255, 128)
    screen.text("Demos", 130, 4)


def draw_people():
    """Draw nearby people"""
    draw_header()

    # Count
    y = 20
    screen.font = small_font
    screen.brush = sf_gray
    screen.text(f"{len(nearby_people)} people nearby", 10, y)

    # People list
    y = 34
    for i, person in enumerate(nearby_people[:3]):
        # Card
        screen.brush = sf_white
        screen.draw(shapes.rounded_rectangle(10, y, 140, 22, 4))

        # Avatar circle
        screen.brush = sf_purple
        screen.draw(shapes.circle(22, y + 11, 8))
        screen.brush = brushes.color(255, 255, 255, 200)
        screen.draw(shapes.circle(22, y + 11, 6))

        # Role
        screen.font = small_font
        screen.brush = sf_darker_blue
        screen.text(person["role"], 35, y + 4)

        # Company
        screen.brush = sf_gray
        screen.text(person["company"], 35, y + 13)

        # Signal strength indicator
        rssi = person["rssi"]
        signal_bars = 3 if rssi > -50 else (2 if rssi > -60 else 1)
        for bar in range(signal_bars):
            height = (bar + 1) * 3
            screen.brush = sf_green
            screen.draw(shapes.rectangle(130 + bar * 5, y + 18 - height, 3, height))

        y += 25

    # Footer
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("C: Demos", 10, 110)
    screen.brush = sf_orange
    screen.text("B: Connect", 80, 110)


def draw_demos():
    """Draw nearby demos"""
    draw_header()

    # Count
    y = 20
    screen.font = small_font
    screen.brush = sf_gray
    screen.text(f"{len(nearby_demos)} demos nearby", 10, y)

    # Demos list
    y = 34
    for i, demo in enumerate(nearby_demos[:3]):
        # Card
        screen.brush = sf_white
        screen.draw(shapes.rounded_rectangle(10, y, 140, 22, 4))

        # Demo icon
        screen.brush = sf_blue
        screen.draw(shapes.rounded_rectangle(16, y + 6, 10, 10, 2))
        screen.brush = brushes.color(255, 255, 255, 200)
        screen.draw(shapes.rounded_rectangle(17, y + 7, 8, 8, 2))

        # Demo name
        screen.font = small_font
        screen.brush = sf_darker_blue
        screen.text(demo["name"], 32, y + 4)

        # Zone
        screen.brush = sf_gray
        screen.text(demo["zone"], 32, y + 13)

        # Wait time badge
        wait_text = f"~{demo['wait']} min"
        w, _ = screen.measure_text(wait_text)

        wait_color = sf_green if demo['wait'] <= 2 else (sf_orange if demo['wait'] <= 5 else sf_gray)
        screen.brush = wait_color
        screen.draw(shapes.rounded_rectangle(145 - w - 4, y + 7, w + 4, 9, 2))

        screen.brush = sf_white
        screen.text(wait_text, 147 - w, y + 8)

        y += 25

    # Footer
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("A: People", 10, 110)
    screen.brush = sf_blue
    screen.text("B: Navigate", 75, 110)


def update():
    global view

    # View switching
    if io.BUTTON_A in io.pressed and view == "demos":
        view = "people"
    elif io.BUTTON_C in io.pressed and view == "people":
        view = "demos"

    # Clear screen
    screen.brush = sf_background
    screen.clear()

    # Draw current view
    if view == "people":
        draw_people()
    else:
        draw_demos()

    return None


if __name__ == "__main__":
    run(update)
