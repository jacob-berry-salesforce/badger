import sys
import os

sys.path.insert(0, "/system/apps/sf_einstein")
os.chdir("/system/apps/sf_einstein")

import math
import random
from badgeware import screen, PixelFont, shapes, brushes, io, run

# Salesforce colors
sf_blue = brushes.color(0, 112, 210)
sf_darker_blue = brushes.color(3, 45, 96)
sf_purple = brushes.color(110, 68, 255)
sf_white = brushes.color(255, 255, 255)
sf_background = brushes.color(243, 243, 243)

# Load fonts
title_font = PixelFont.load("/system/assets/fonts/absolute.ppf")
body_font = PixelFont.load("/system/assets/fonts/nope.ppf")
small_font = PixelFont.load("/system/assets/fonts/ark.ppf")

# Einstein predictions
predictions = [
    "Your next deal will close successfully!",
    "A major opportunity is coming your way.",
    "Collaborate with your team for best results.",
    "Focus on customer success today.",
    "Innovation is in your future.",
    "Your pipeline looks promising.",
    "A new lead will convert soon.",
    "Trust the AI - it knows best!",
    "Your forecast accuracy will improve.",
    "Expect a productive meeting ahead.",
    "A challenge will become an opportunity.",
    "Your hard work will pay off.",
    "Network with a new contact today.",
    "Review your dashboards for insights.",
    "Success requires persistence.",
]

# State
current_prediction = None
predicting = False
prediction_start = 0
prediction_duration = 2000  # 2 seconds animation


def init():
    global current_prediction
    # Set initial random prediction
    current_prediction = random.choice(predictions)


def draw_header():
    """Draw compact Einstein header"""
    screen.brush = sf_purple
    screen.draw(shapes.rectangle(0, 0, 160, 14))

    screen.font = body_font
    screen.brush = sf_white
    screen.text("Einstein AI", 5, 3)


def draw_einstein_icon(x, y, size=15):
    """Draw a simple Einstein/AI icon (brain/lightbulb)"""
    # Draw lightbulb shape
    screen.brush = brushes.color(255, 220, 100, 200)
    screen.draw(shapes.circle(x, y, size))

    # Add glow effect with animation
    glow_size = size + math.sin(io.ticks / 200) * 3
    screen.brush = brushes.color(255, 220, 100, 50)
    screen.draw(shapes.circle(x, y, glow_size))

    # Lightning bolt in center
    screen.brush = sf_white
    screen.draw(shapes.line(x - 3, y - 4, x, y, 2))
    screen.draw(shapes.line(x, y, x + 3, y + 4, 2))


def draw_prediction_card():
    """Draw the prediction card"""
    # Card background
    screen.brush = sf_white
    screen.draw(shapes.rounded_rectangle(5, 42, 150, 58, 6))

    if predicting:
        # Show animation during prediction
        progress = (io.ticks - prediction_start) / prediction_duration
        if progress < 1:
            # Loading animation
            screen.font = body_font
            screen.brush = sf_purple
            dots = "." * (int(progress * 10) % 4)
            text = f"Analyzing{dots}"
            w, _ = screen.measure_text(text)
            screen.text(text, 80 - w // 2, 64)

            # Progress bar
            screen.brush = sf_blue
            bar_width = max(5, int(130 * progress))  # Ensure minimum width
            screen.draw(shapes.rounded_rectangle(15, 80, bar_width, 5, 2))
    else:
        # Show prediction text (wrapped)
        if current_prediction:
            screen.font = small_font
            screen.brush = sf_darker_blue

            # Simple text wrapping
            words = current_prediction.split()
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

            # Draw lines centered
            y = 52
            for line in lines[:4]:  # Max 4 lines
                w, _ = screen.measure_text(line)
                screen.text(line, 80 - w // 2, y)
                y += 8


def draw_instructions():
    """Draw usage instructions"""
    screen.font = small_font
    screen.brush = sf_darker_blue

    if not predicting:
        text = "B: New"
        screen.text(text, 10, 105)

    screen.text("HOME: Exit", 110, 105)


def update():
    global current_prediction, predicting, prediction_start

    # Clear screen
    screen.brush = sf_background
    screen.clear()

    # Handle button press
    if io.BUTTON_B in io.pressed and not predicting:
        # Start new prediction
        predicting = True
        prediction_start = io.ticks

    # Check if prediction animation is done
    if predicting and (io.ticks - prediction_start) > prediction_duration:
        predicting = False
        current_prediction = random.choice(predictions)

    # Draw UI
    draw_header()

    # Draw animated Einstein icon
    draw_einstein_icon(80, 26, 10)

    draw_prediction_card()
    draw_instructions()

    return None


if __name__ == "__main__":
    run(update)
