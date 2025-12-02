import sys
import os

sys.path.insert(0, "/system/apps/sf_home")
os.chdir("/system/apps/sf_home")

import math
from badgeware import screen, PixelFont, shapes, brushes, io, run, get_battery_level, is_charging

# Salesforce colors
sf_blue = brushes.color(0, 161, 224)
sf_darker_blue = brushes.color(3, 45, 96)
sf_green = brushes.color(87, 221, 108)
sf_orange = brushes.color(255, 159, 10)
sf_white = brushes.color(255, 255, 255)
sf_gray = brushes.color(120, 120, 120)
sf_background = brushes.color(250, 250, 255)

# Load fonts
title_font = PixelFont.load("/system/assets/fonts/absolute.ppf")
body_font = PixelFont.load("/system/assets/fonts/nope.ppf")
small_font = PixelFont.load("/system/assets/fonts/ark.ppf")

# Mock visitor data
visitor = {
    "name": "Jacob Berry",
    "company": "Salesforce",
    "role": "Solutions Engineer",
    "zone": "Discovery Zone",
    "next_session": "F1 Simulator",
    "next_time": "in 12 min"
}

# Zone colors (simulated BLE proximity)
zones = [
    "Discovery Zone",
    "Retail AI Zone",
    "FINS Zone",
    "Innovation Hub"
]
current_zone = 0


def draw_header():
    """Draw compact gradient header"""
    # Orange to blue gradient
    for y in range(14):
        progress = y / 14
        r = int(255 + (0 - 255) * progress)
        g = int(140 + (161 - 140) * progress)
        b = int(0 + (224 - 0) * progress)
        screen.brush = brushes.color(r, g, b)
        screen.draw(shapes.rectangle(0, y, 160, 1))

    screen.font = body_font
    screen.brush = sf_white
    screen.text("Home", 5, 3)

    # Battery indicator (small)
    battery_level = get_battery_level() if not is_charging() else (io.ticks / 20) % 100
    pos = (140, 4)
    size = (14, 6)

    screen.brush = sf_white
    screen.draw(shapes.rectangle(*pos, *size))

    width = ((size[0] - 2) / 100) * battery_level
    if width > 0:
        if battery_level > 50:
            bar_color = sf_green
        elif battery_level > 20:
            bar_color = brushes.color(255, 220, 100)
        else:
            bar_color = brushes.color(255, 100, 100)
        screen.brush = bar_color
        screen.draw(shapes.rectangle(pos[0] + 1, pos[1] + 1, width, size[1] - 2))


def draw_visitor_card():
    """Draw visitor identity card"""
    # Card shadow
    screen.brush = brushes.color(0, 0, 0, 30)
    screen.draw(shapes.rounded_rectangle(7, 20, 150, 42, 6))

    # Card body
    screen.brush = sf_white
    screen.draw(shapes.rounded_rectangle(5, 18, 150, 42, 6))

    # Gradient accent
    for y in range(4):
        alpha = int(150 - y * 30)
        screen.brush = brushes.color(0, 161, 224, alpha)
        screen.draw(shapes.rectangle(5, 18 + y, 150, 1))

    # Avatar placeholder (circle)
    screen.brush = sf_blue
    screen.draw(shapes.circle(20, 36, 10))
    screen.brush = brushes.color(255, 255, 255, 200)
    screen.draw(shapes.circle(20, 36, 7))

    # Name
    screen.font = title_font
    screen.brush = sf_darker_blue
    screen.text(visitor["name"], 35, 24)

    # Company
    screen.font = small_font
    screen.brush = sf_gray
    screen.text(visitor["company"], 35, 36)

    # Role badge
    screen.font = small_font
    role_w, _ = screen.measure_text(visitor["role"])
    screen.brush = sf_orange
    screen.draw(shapes.rounded_rectangle(35, 46, role_w + 4, 9, 2))
    screen.brush = sf_white
    screen.text(visitor["role"], 37, 47)


def draw_status():
    """Draw current zone and next session"""
    y = 66

    # Current zone with animated glow
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("CURRENT ZONE:", 10, y)

    # Zone badge with pulse
    zone_text = zones[current_zone]
    screen.font = body_font
    zone_w, _ = screen.measure_text(zone_text)

    # Pulsing glow
    pulse = math.sin(io.ticks / 200) * 10 + 20
    screen.brush = brushes.color(0, 161, 224, int(pulse))
    screen.draw(shapes.rounded_rectangle(8, y + 11, zone_w + 6, 11, 3))

    # Zone badge
    screen.brush = sf_blue
    screen.draw(shapes.rounded_rectangle(9, y + 12, zone_w + 4, 9, 2))
    screen.brush = sf_white
    screen.text(zone_text, 11, y + 13)

    # Next session
    y = 88
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("UP NEXT:", 10, y)

    screen.font = body_font
    screen.brush = sf_darker_blue
    screen.text(visitor["next_session"], 10, y + 10)

    screen.font = small_font
    screen.brush = sf_green
    screen.text(visitor["next_time"], 10, y + 20)


def draw_footer():
    """Draw footer with instructions"""
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("A: Change Zone", 10, 110)


def update():
    global current_zone

    # Handle zone cycling
    if io.BUTTON_A in io.pressed:
        current_zone = (current_zone + 1) % len(zones)

    # Clear screen
    screen.brush = sf_background
    screen.clear()

    # Draw UI
    draw_header()
    draw_visitor_card()
    draw_status()
    draw_footer()

    return None


if __name__ == "__main__":
    run(update)
