import sys
import os

sys.path.insert(0, "/system/apps/sf_ohana")
os.chdir("/system/apps/sf_ohana")

import math
from badgeware import screen, PixelFont, shapes, brushes, io, run

# Salesforce colors
sf_blue = brushes.color(0, 112, 210)
sf_darker_blue = brushes.color(3, 45, 96)
sf_green = brushes.color(95, 237, 131)
sf_orange = brushes.color(255, 186, 88)
sf_purple = brushes.color(110, 68, 255)
sf_pink = brushes.color(255, 128, 210)
sf_white = brushes.color(255, 255, 255)
sf_background = brushes.color(243, 243, 243)

# Load fonts
title_font = PixelFont.load("/system/assets/fonts/absolute.ppf")
body_font = PixelFont.load("/system/assets/fonts/nope.ppf")
small_font = PixelFont.load("/system/assets/fonts/ark.ppf")

# Salesforce Core Values
values = [
    {
        "name": "Trust",
        "icon_color": sf_blue,
        "description": "We build trusted relationships through transparency and security."
    },
    {
        "name": "Customer Success",
        "icon_color": sf_green,
        "description": "We're committed to the success of our customers."
    },
    {
        "name": "Innovation",
        "icon_color": sf_orange,
        "description": "We pioneer new technologies and embrace change."
    },
    {
        "name": "Equality",
        "icon_color": sf_purple,
        "description": "We create opportunities for everyone to succeed."
    },
]

current_value = 0


def draw_header():
    """Draw compact Ohana header"""
    screen.brush = sf_blue
    screen.draw(shapes.rectangle(0, 0, 160, 14))

    screen.font = body_font
    screen.brush = sf_white
    screen.text("Ohana Values", 5, 3)


def draw_value_card():
    """Draw the current value card with animation"""
    value = values[current_value]

    # Card background
    screen.brush = sf_white
    screen.draw(shapes.rounded_rectangle(5, 18, 150, 85, 6))

    # Value icon (animated circle)
    icon_size = 16 + math.sin(io.ticks / 300) * 2
    screen.brush = value["icon_color"]
    screen.draw(shapes.circle(80, 40, icon_size))

    # Inner circle
    screen.brush = brushes.color(255, 255, 255, 200)
    screen.draw(shapes.circle(80, 40, icon_size - 5))

    # Value name
    screen.font = title_font
    screen.brush = sf_darker_blue
    name_w, _ = screen.measure_text(value["name"])
    screen.text(value["name"], 80 - name_w // 2, 60)

    # Description (wrapped)
    screen.font = small_font
    screen.brush = sf_darker_blue

    words = value["description"].split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        w, _ = screen.measure_text(test_line)
        if w > 135:
            lines.append(current_line.strip())
            current_line = word + " "
        else:
            current_line = test_line

    if current_line:
        lines.append(current_line.strip())

    # Draw description lines
    y = 74
    for line in lines[:3]:  # Max 3 lines
        w, _ = screen.measure_text(line)
        screen.text(line, 80 - w // 2, y)
        y += 8


def draw_navigation():
    """Draw compact navigation indicators"""
    screen.font = small_font
    screen.brush = sf_darker_blue

    # Navigation hints
    if current_value > 0:
        screen.text("< A", 10, 107)

    if current_value < len(values) - 1:
        screen.text("C >", 135, 107)

    # Page dots
    dots_start = 80 - (len(values) * 5)
    for i in range(len(values)):
        if i == current_value:
            screen.brush = sf_blue
            screen.draw(shapes.circle(dots_start + i * 10, 110, 3))
        else:
            screen.brush = brushes.color(200, 200, 200)
            screen.draw(shapes.circle(dots_start + i * 10, 110, 2))


def update():
    global current_value

    # Clear screen
    screen.brush = sf_background
    screen.clear()

    # Handle navigation
    if io.BUTTON_C in io.pressed or io.BUTTON_DOWN in io.pressed:
        current_value = (current_value + 1) % len(values)

    if io.BUTTON_A in io.pressed or io.BUTTON_UP in io.pressed:
        current_value = (current_value - 1) % len(values)

    # Draw UI
    draw_header()
    draw_value_card()
    draw_navigation()

    return None


if __name__ == "__main__":
    run(update)
