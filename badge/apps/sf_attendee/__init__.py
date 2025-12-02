import sys
import os

# Set up paths
sys.path.insert(0, "/system/apps/sf_attendee")
os.chdir("/system/apps/sf_attendee")

from badgeware import screen, PixelFont, shapes, brushes, io, run

# Salesforce colors - enhanced vibrant palette
sf_blue = brushes.color(0, 161, 224)  # Brighter Salesforce blue
sf_darker_blue = brushes.color(0, 95, 178)
sf_light_blue = brushes.color(186, 218, 255)
sf_orange = brushes.color(255, 140, 0)  # More vibrant orange
sf_green = brushes.color(87, 221, 108)  # Brighter green
sf_white = brushes.color(255, 255, 255)
sf_gray = brushes.color(120, 120, 120)
sf_background = brushes.color(239, 247, 255)  # Light blue tint

# Load fonts
title_font = PixelFont.load("/system/assets/fonts/absolute.ppf")
body_font = PixelFont.load("/system/assets/fonts/nope.ppf")
small_font = PixelFont.load("/system/assets/fonts/ark.ppf")

# Mock Event Attendee data - key fields only
attendee_data = {
    "Event": "Blue Arrow",
    "Contact": "Jeremy Pritchard",
    "Role": "Attendee",
    "RSVP": "Draft",
    "Status": "Not Checked In",
    "ID": "ATT-00001"
}

def draw_header():
    """Draw vibrant gradient header"""
    # Gradient header (darker to lighter blue)
    for y in range(18):
        progress = y / 18
        r = int(0 + (30 - 0) * progress)
        g = int(80 + (140 - 80) * progress)
        b = int(170 + (210 - 170) * progress)
        screen.brush = brushes.color(r, g, b)
        screen.draw(shapes.rectangle(0, y, 160, 1))

    # Title with shadow for depth
    screen.font = body_font
    screen.brush = brushes.color(0, 0, 0, 100)
    screen.text("Event Attendee", 6, 5)
    screen.brush = sf_white
    screen.text("Event Attendee", 5, 4)

def draw_attendee_card():
    """Draw attendee info with visual depth and color"""
    # Card shadow
    screen.brush = brushes.color(0, 0, 0, 30)
    screen.draw(shapes.rounded_rectangle(7, 22, 150, 85, 6))

    # Main card with subtle gradient
    screen.brush = sf_white
    screen.draw(shapes.rounded_rectangle(5, 20, 150, 85, 6))

    # Top accent bar (colorful)
    screen.brush = sf_blue
    screen.draw(shapes.rounded_rectangle(5, 20, 150, 6, 6))

    y = 30

    # Contact name (larger, bold)
    screen.font = title_font
    screen.brush = sf_darker_blue
    screen.text(attendee_data["Contact"], 10, y)
    y += 14

    # Event name with colored label
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("Event:", 10, y)
    screen.font = body_font
    screen.brush = sf_blue
    screen.text(attendee_data["Event"], 44, y)
    y += 11

    # Role
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("Role:", 10, y)
    screen.font = body_font
    screen.brush = sf_darker_blue
    screen.text(attendee_data["Role"], 44, y)
    y += 11

    # RSVP Status with badge
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("RSVP:", 10, y)

    # RSVP badge background
    rsvp_text = attendee_data["RSVP"]
    screen.font = body_font
    rsvp_w, _ = screen.measure_text(rsvp_text)
    badge_color = sf_orange if attendee_data["RSVP"] == "Draft" else sf_green
    screen.brush = badge_color
    screen.draw(shapes.rounded_rectangle(42, y - 1, rsvp_w + 4, 9, 2))

    # RSVP text
    screen.font = body_font
    screen.brush = sf_white
    screen.text(rsvp_text, 44, y)
    y += 11

    # Attendance Status
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("Status:", 10, y)
    screen.font = body_font
    screen.brush = sf_darker_blue
    # Truncate if needed
    status_text = attendee_data["Status"]
    if len(status_text) > 13:
        status_text = status_text[:13]
    screen.text(status_text, 44, y)
    y += 13

    # ID at bottom with icon
    screen.font = small_font
    screen.brush = sf_blue
    screen.draw(shapes.circle(12, y + 3, 2))
    screen.brush = sf_gray
    screen.text(attendee_data["ID"], 18, y)

def draw_footer():
    """Draw footer with subtle background"""
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
    draw_attendee_card()
    draw_footer()

    return None

if __name__ == "__main__":
    run(update)
