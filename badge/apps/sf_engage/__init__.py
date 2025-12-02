import sys
import os

sys.path.insert(0, "/system/apps/sf_engage")
os.chdir("/system/apps/sf_engage")

import math
from badgeware import screen, PixelFont, shapes, brushes, io, run

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

# Poll state
STATE_WAITING = "waiting"
STATE_POLL = "poll"
STATE_RESULTS = "results"

state = STATE_POLL  # Start with a poll visible
voted = False
selected_option = None
show_results_at = 0

# Mock poll (only 3 options for 3 buttons)
current_poll = {
    "question": "Which AI feature excites you most?",
    "options": [
        "Agentforce",
        "Einstein AI",
        "Data Cloud"
    ],
    "results": [45, 32, 23]  # percentages
}


def draw_header(color=sf_blue):
    """Draw engage header"""
    screen.brush = color
    screen.draw(shapes.rectangle(0, 0, 160, 14))

    screen.font = body_font
    screen.brush = sf_white
    screen.text("Live Poll", 5, 3)


def draw_waiting():
    """Draw waiting for poll screen"""
    draw_header(sf_gray)

    # Waiting animation
    dots = "." * (int(io.ticks / 300) % 4)

    screen.font = body_font
    screen.brush = sf_gray
    text = f"Waiting for poll{dots}"
    w, _ = screen.measure_text(text)
    screen.text(text, 80 - w // 2, 50)

    # Icon
    pulse = math.sin(io.ticks / 200) * 5 + 25
    screen.brush = brushes.color(0, 161, 224, 50)
    screen.draw(shapes.circle(80, 30, int(pulse)))

    screen.brush = sf_blue
    screen.draw(shapes.circle(80, 30, 20))
    screen.brush = brushes.color(255, 255, 255, 200)
    screen.draw(shapes.circle(80, 30, 16))


def draw_poll():
    """Draw active poll"""
    draw_header(sf_blue)

    # Question
    y = 20
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("QUESTION:", 10, y)

    # Wrap question
    screen.font = body_font
    screen.brush = sf_darker_blue
    words = current_poll["question"].split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        w, _ = screen.measure_text(test_line)
        if w > 140:
            lines.append(current_line.strip())
            current_line = word + " "
        else:
            current_line = test_line

    if current_line:
        lines.append(current_line.strip())

    y = 32
    for line in lines[:2]:
        screen.text(line, 10, y)
        y += 10

    # Options (mapped to buttons)
    y = 54
    button_labels = ["A", "B", "C"]
    button_colors = [sf_blue, sf_green, sf_orange]

    for i, option in enumerate(current_poll["options"]):
        # Option button
        screen.brush = button_colors[i]
        screen.draw(shapes.rounded_rectangle(10, y, 140, 13, 3))

        # Button label
        screen.font = small_font
        screen.brush = sf_white
        screen.text(button_labels[i], 15, y + 3)

        # Option text
        screen.font = small_font
        screen.text(option, 28, y + 3)

        # Checkmark if selected
        if voted and selected_option == i:
            screen.text("✓", 145, y + 2)

        y += 15

    # Status
    if voted:
        screen.font = small_font
        screen.brush = sf_green
        screen.text("Vote submitted!", 50, 110)


def draw_results():
    """Draw poll results"""
    draw_header(sf_green)

    # Title
    y = 20
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("RESULTS:", 10, y)

    # Results bars
    y = 34
    for i, option in enumerate(current_poll["options"]):
        # Option name
        screen.font = small_font
        screen.brush = sf_darker_blue
        screen.text(option, 10, y)

        # Result bar
        bar_y = y + 10
        # Background
        screen.brush = brushes.color(220, 220, 220)
        screen.draw(shapes.rectangle(10, bar_y, 120, 6))

        # Filled portion
        percent = current_poll["results"][i]
        bar_width = int((120 * percent) / 100)
        if bar_width > 0:
            colors = [sf_blue, sf_green, sf_orange, brushes.color(110, 68, 255)]
            screen.brush = colors[i]
            screen.draw(shapes.rectangle(10, bar_y, bar_width, 6))

        # Percentage
        screen.font = small_font
        screen.brush = sf_darker_blue
        screen.text(f"{percent}%", 135, bar_y - 1)

        y += 20

    # Footer
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("Thank you for voting!", 35, 110)


def update():
    global state, voted, selected_option, show_results_at

    # Handle voting (only 3 buttons available: A, B, C)
    if state == STATE_POLL and not voted:
        if io.BUTTON_A in io.pressed:
            voted = True
            selected_option = 0
            show_results_at = io.ticks + 2000
        elif io.BUTTON_B in io.pressed:
            voted = True
            selected_option = 1
            show_results_at = io.ticks + 2000
        elif io.BUTTON_C in io.pressed:
            voted = True
            selected_option = 2
            show_results_at = io.ticks + 2000

    # Transition to results
    if voted and io.ticks >= show_results_at and state == STATE_POLL:
        state = STATE_RESULTS

    # Clear screen
    screen.brush = sf_background
    screen.clear()

    # Draw current state
    if state == STATE_WAITING:
        draw_waiting()
    elif state == STATE_POLL:
        draw_poll()
    elif state == STATE_RESULTS:
        draw_results()

    return None


if __name__ == "__main__":
    run(update)
