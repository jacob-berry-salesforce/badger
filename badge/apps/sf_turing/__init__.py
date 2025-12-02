import sys
import os

sys.path.insert(0, "/system/apps/sf_turing")
os.chdir("/system/apps/sf_turing")

import math
import random
from badgeware import screen, PixelFont, shapes, brushes, io, run

# Salesforce colors
sf_blue = brushes.color(0, 161, 224)
sf_darker_blue = brushes.color(3, 45, 96)
sf_purple = brushes.color(110, 68, 255)
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
STATE_LOBBY = "lobby"
STATE_ASSIGNED = "assigned"
STATE_PLAYING = "playing"
STATE_REVEAL = "reveal"

state = STATE_LOBBY
game_start_time = 0
round_duration = 6000  # 6 seconds
lobby_countdown = 90  # seconds

# Game data
player_role = "Player B"
prompt = "What is the capital of France?"
verdict = None  # Will be "HUMAN" or "AI"
points = 42


def draw_header(title, color=sf_purple):
    """Draw compact Turing header"""
    screen.brush = color
    screen.draw(shapes.rectangle(0, 0, 160, 14))

    screen.font = body_font
    screen.brush = sf_white
    screen.text(title, 5, 3)


def draw_lobby():
    """Draw lobby/waiting screen"""
    draw_header("Turing Test")

    # AI vs Human illustration
    y = 25
    # AI circle
    screen.brush = sf_purple
    screen.draw(shapes.circle(50, y + 15, 18))
    screen.brush = brushes.color(255, 255, 255, 200)
    screen.draw(shapes.circle(50, y + 15, 14))
    screen.font = small_font
    screen.brush = sf_purple
    screen.text("AI", 45, y + 12)

    # VS text
    screen.font = body_font
    screen.brush = sf_gray
    screen.text("VS", 73, y + 10)

    # Human circle
    screen.brush = sf_blue
    screen.draw(shapes.circle(110, y + 15, 18))
    screen.brush = brushes.color(255, 255, 255, 200)
    screen.draw(shapes.circle(110, y + 15, 14))
    screen.font = small_font
    screen.brush = sf_blue
    screen.text("YOU", 102, y + 12)

    # Countdown
    y = 70
    countdown = max(0, lobby_countdown - (io.ticks // 1000) % lobby_countdown)

    screen.font = small_font
    screen.brush = sf_gray
    screen.text("NEXT GAME IN", 50, y)

    screen.font = title_font
    screen.brush = sf_purple
    mins = countdown // 60
    secs = countdown % 60
    time_text = f"{mins}:{secs:02d}"
    w, _ = screen.measure_text(time_text)
    screen.text(time_text, 80 - w // 2, y + 12)

    # Join button
    screen.font = small_font
    screen.brush = sf_green
    screen.text("A: Join Queue", 45, 110)


def draw_assigned():
    """Draw player assignment screen"""
    draw_header("Assigned", sf_purple)

    # Role badge (large)
    y = 35
    screen.font = title_font
    screen.brush = sf_purple
    text = player_role
    w, _ = screen.measure_text(text)
    screen.text(text, 80 - w // 2, y)

    # Role description
    screen.font = small_font
    screen.brush = sf_gray
    desc = "You'll answer as a human"
    w, _ = screen.measure_text(desc)
    screen.text(desc, 80 - w // 2, y + 18)

    # Pulsing circle around role
    pulse = math.sin(io.ticks / 200) * 5 + 40
    screen.brush = brushes.color(110, 68, 255, 50)
    screen.draw(shapes.circle(80, 60, int(pulse)))

    # Instructions
    y = 85
    screen.font = small_font
    screen.brush = sf_darker_blue

    lines = [
        "Game starts in 3s",
        "Answer the prompt",
        "Convince judges you're real"
    ]

    for line in lines:
        w, _ = screen.measure_text(line)
        screen.text(line, 80 - w // 2, y)
        y += 10


def draw_playing():
    """Draw active game screen"""
    draw_header("Round Active", sf_orange)

    # Time remaining
    elapsed = io.ticks - game_start_time
    remaining = max(0, (round_duration - elapsed) // 1000)

    screen.font = title_font
    screen.brush = sf_orange
    time_text = f"{remaining}s"
    w, _ = screen.measure_text(time_text)
    screen.text(time_text, 80 - w // 2, 22)

    # Prompt card
    y = 42
    screen.brush = sf_white
    screen.draw(shapes.rounded_rectangle(10, y, 140, 50, 6))

    screen.font = small_font
    screen.brush = sf_gray
    screen.text("PROMPT:", 15, y + 5)

    # Wrap prompt text
    screen.font = body_font
    screen.brush = sf_darker_blue

    words = prompt.split()
    lines = []
    current_line = ""

    for word in words:
        test_line = current_line + word + " "
        w, _ = screen.measure_text(test_line)
        if w > 130:
            lines.append(current_line.strip())
            current_line = word + " "
        else:
            current_line = test_line

    if current_line:
        lines.append(current_line.strip())

    line_y = y + 18
    for line in lines[:3]:
        screen.text(line, 15, line_y)
        line_y += 10

    # Status
    screen.font = small_font
    screen.brush = sf_green
    screen.text("Answer submitted", 40, 108)


def draw_reveal():
    """Draw verdict reveal screen"""
    if verdict == "HUMAN":
        draw_header("SUCCESS!", sf_green)
        color = sf_green
        icon_text = "✓"
    else:
        draw_header("DETECTED", sf_orange)
        color = sf_orange
        icon_text = "AI"

    # Verdict icon with animation
    pulse = math.sin(io.ticks / 150) * 5 + 35
    screen.brush = brushes.color(*[int(c) for c in [color.r, color.g, color.b]], 50)
    screen.draw(shapes.circle(80, 40, int(pulse)))

    screen.brush = color
    screen.draw(shapes.circle(80, 40, 30))
    screen.brush = brushes.color(255, 255, 255, 200)
    screen.draw(shapes.circle(80, 40, 26))

    screen.font = title_font
    screen.brush = color
    text = icon_text if verdict == "AI" else icon_text
    w, _ = screen.measure_text(text)
    screen.text(text, 80 - w // 2, 35)

    # Verdict text
    y = 75
    screen.font = body_font
    screen.brush = sf_darker_blue
    text = f"Judges: {verdict}"
    w, _ = screen.measure_text(text)
    screen.text(text, 80 - w // 2, y)

    # Points
    y = 90
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("TOTAL POINTS", 55, y)

    screen.font = title_font
    screen.brush = color
    screen.text(str(points), 70, y + 10)

    # Footer
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("A: Play Again", 50, 110)


def update():
    global state, game_start_time, verdict

    # State transitions
    if state == STATE_LOBBY and io.BUTTON_A in io.pressed:
        state = STATE_ASSIGNED
        game_start_time = io.ticks + 3000  # 3 second delay

    elif state == STATE_ASSIGNED:
        if io.ticks >= game_start_time:
            state = STATE_PLAYING
            game_start_time = io.ticks

    elif state == STATE_PLAYING:
        if (io.ticks - game_start_time) > round_duration:
            state = STATE_REVEAL
            verdict = random.choice(["HUMAN", "AI"])

    elif state == STATE_REVEAL and io.BUTTON_A in io.pressed:
        state = STATE_LOBBY

    # Clear screen
    screen.brush = sf_background
    screen.clear()

    # Draw current state
    if state == STATE_LOBBY:
        draw_lobby()
    elif state == STATE_ASSIGNED:
        draw_assigned()
    elif state == STATE_PLAYING:
        draw_playing()
    elif state == STATE_REVEAL:
        draw_reveal()

    return None


if __name__ == "__main__":
    run(update)
