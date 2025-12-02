import sys
import os

sys.path.insert(0, "/system/apps/sf_f1")
os.chdir("/system/apps/sf_f1")

import math
import random
from badgeware import screen, PixelFont, shapes, brushes, io, run

# Salesforce colors
sf_blue = brushes.color(0, 161, 224)
sf_darker_blue = brushes.color(3, 45, 96)
sf_red = brushes.color(234, 0, 23)  # Racing red
sf_green = brushes.color(87, 221, 108)
sf_orange = brushes.color(255, 159, 10)
sf_white = brushes.color(255, 255, 255)
sf_gray = brushes.color(120, 120, 120)
sf_background = brushes.color(250, 250, 255)

# Load fonts
title_font = PixelFont.load("/system/assets/fonts/absolute.ppf")
body_font = PixelFont.load("/system/assets/fonts/nope.ppf")
small_font = PixelFont.load("/system/assets/fonts/ark.ppf")

# State machine
STATE_QUEUE = "queue"
STATE_RACING = "racing"
STATE_RECAP = "recap"

state = STATE_QUEUE
race_started_at = 0
race_duration = 8000  # 8 seconds for demo

# Mock race data
queue_position = 3
estimated_wait = 5  # minutes

race_data = {
    "lap": 1,
    "total_laps": 3,
    "position": 2,
    "delta": "+0.234",
    "best_lap": "1:23.456",
    "current_speed": 0
}

recap_data = {
    "finish_time": "4:12.789",
    "best_lap": "1:21.234",
    "avg_speed": 247,
    "position": 2
}


def draw_header(title, color=sf_red):
    """Draw compact F1 header"""
    screen.brush = color
    screen.draw(shapes.rectangle(0, 0, 160, 14))

    screen.font = body_font
    screen.brush = sf_white
    screen.text(title, 5, 3)


def draw_queue():
    """Draw queue/waiting screen"""
    draw_header("F1 Race Coach")

    # Rig illustration (simple car shape)
    y = 25
    screen.brush = sf_red
    screen.draw(shapes.rounded_rectangle(40, y, 80, 30, 8))
    # Wheels
    screen.brush = sf_darker_blue
    screen.draw(shapes.circle(50, y + 30, 6))
    screen.draw(shapes.circle(110, y + 30, 6))

    # Queue info card
    y = 70
    screen.brush = sf_white
    screen.draw(shapes.rounded_rectangle(10, y, 140, 35, 6))

    screen.font = small_font
    screen.brush = sf_gray
    screen.text("QUEUE POSITION", 15, y + 5)

    screen.font = title_font
    screen.brush = sf_red
    screen.text(f"#{queue_position}", 15, y + 15)

    screen.font = small_font
    screen.brush = sf_gray
    screen.text(f"~{estimated_wait} min wait", 50, y + 18)

    # Ready button hint
    screen.font = small_font
    screen.brush = sf_green
    screen.text("B: Check In (NFC)", 45, 110)


def draw_racing():
    """Draw live race HUD"""
    draw_header("LIVE RACE", sf_red)

    # Simulate race progress
    progress = (io.ticks - race_started_at) / race_duration
    if progress > 1:
        progress = 1

    # Update mock telemetry
    race_data["current_speed"] = int(120 + math.sin(io.ticks / 100) * 100)
    race_data["lap"] = min(3, int(progress * 3) + 1)

    # Speed (large)
    y = 22
    screen.font = title_font
    screen.brush = sf_red
    speed_text = f"{race_data['current_speed']}"
    w, _ = screen.measure_text(speed_text)
    screen.text(speed_text, 80 - w // 2, y)

    screen.font = small_font
    screen.brush = sf_gray
    screen.text("km/h", 90, y + 2)

    # Lap counter
    y = 45
    screen.font = body_font
    screen.brush = sf_darker_blue
    lap_text = f"Lap {race_data['lap']}/{race_data['total_laps']}"
    w, _ = screen.measure_text(lap_text)
    screen.text(lap_text, 80 - w // 2, y)

    # Position badge
    y = 60
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("POSITION", 15, y)

    pos_text = f"P{race_data['position']}"
    screen.font = title_font
    screen.brush = sf_orange
    screen.text(pos_text, 15, y + 10)

    # Delta
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("DELTA", 90, y)

    screen.font = body_font
    screen.brush = sf_red if race_data['delta'].startswith('+') else sf_green
    screen.text(race_data['delta'], 90, y + 10)

    # Best lap
    y = 88
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("BEST LAP", 15, y)

    screen.font = body_font
    screen.brush = sf_darker_blue
    screen.text(race_data['best_lap'], 15, y + 10)

    # Progress bar
    y = 108
    screen.brush = brushes.color(200, 200, 200)
    screen.draw(shapes.rectangle(10, y, 140, 6))

    screen.brush = sf_red
    bar_width = int(140 * progress)
    screen.draw(shapes.rectangle(10, y, bar_width, 6))


def draw_recap():
    """Draw post-race summary"""
    draw_header("RACE COMPLETE", sf_green)

    # Trophy/medal icon
    screen.brush = sf_orange
    screen.draw(shapes.circle(80, 30, 12))
    screen.brush = brushes.color(255, 255, 255, 200)
    screen.draw(shapes.circle(80, 30, 9))

    screen.font = title_font
    screen.brush = sf_orange
    text = f"P{recap_data['position']}"
    w, _ = screen.measure_text(text)
    screen.text(text, 80 - w // 2, 25)

    # Stats card
    y = 50
    screen.brush = sf_white
    screen.draw(shapes.rounded_rectangle(10, y, 140, 50, 6))

    screen.font = small_font
    screen.brush = sf_gray
    screen.text("TIME", 15, y + 5)
    screen.font = body_font
    screen.brush = sf_darker_blue
    screen.text(recap_data['finish_time'], 15, y + 15)

    screen.font = small_font
    screen.brush = sf_gray
    screen.text("BEST LAP", 15, y + 30)
    screen.font = body_font
    screen.brush = sf_darker_blue
    screen.text(recap_data['best_lap'], 15, y + 40)

    screen.font = small_font
    screen.brush = sf_gray
    screen.text("AVG SPEED", 90, y + 30)
    screen.font = body_font
    screen.brush = sf_red
    screen.text(f"{recap_data['avg_speed']}", 90, y + 40)

    # Footer
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("A: New Race", 50, 110)


def update():
    global state, race_started_at

    # State transitions
    if state == STATE_QUEUE and io.BUTTON_B in io.pressed:
        # Simulate NFC check-in
        state = STATE_RACING
        race_started_at = io.ticks

    elif state == STATE_RACING:
        # Check if race finished
        if (io.ticks - race_started_at) > race_duration:
            state = STATE_RECAP

    elif state == STATE_RECAP and io.BUTTON_A in io.pressed:
        # Reset to queue
        state = STATE_QUEUE

    # Clear screen
    screen.brush = sf_background
    screen.clear()

    # Draw current state
    if state == STATE_QUEUE:
        draw_queue()
    elif state == STATE_RACING:
        draw_racing()
    elif state == STATE_RECAP:
        draw_recap()

    return None


if __name__ == "__main__":
    run(update)
