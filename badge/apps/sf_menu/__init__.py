import sys
import os

sys.path.insert(0, "/system/apps/sf_menu")
os.chdir("/system/apps/sf_menu")

import math
from badgeware import screen, PixelFont, Image, SpriteSheet, is_dir, file_exists, shapes, brushes, io, run
from icon import Icon
import ui

# Load font
screen.font = PixelFont.load("/system/assets/fonts/ark.ppf")

# Auto-discover Salesforce apps (those starting with sf_)
apps = []
try:
    for entry in os.listdir("/system/apps"):
        app_path = f"/system/apps/{entry}"
        if is_dir(app_path):
            has_init = file_exists(f"{app_path}/__init__.py")
            if has_init:
                # Only load apps starting with "sf_" but not the menu itself
                if entry.startswith("sf_") and entry != "sf_menu":
                    # Use directory name as display name (remove sf_ prefix for display)
                    display_name = entry.replace("sf_", "").replace("_", " ").title()
                    apps.append((display_name, entry))
except Exception as e:
    print(f"Error discovering apps: {e}")

# Sort apps alphabetically
apps.sort(key=lambda x: x[0])

# Pagination constants
APPS_PER_PAGE = 6
current_page = 0
total_pages = max(1, math.ceil(len(apps) / APPS_PER_PAGE))


def load_page_icons(page):
    """Load icons for the current page of apps"""
    icons = []
    start_idx = page * APPS_PER_PAGE
    end_idx = min(start_idx + APPS_PER_PAGE, len(apps))

    for i in range(start_idx, end_idx):
        app = apps[i]
        name, path = app[0], app[1]

        if is_dir(f"/system/apps/{path}"):
            icon_idx = i - start_idx
            x = icon_idx % 3
            y = math.floor(icon_idx / 3)
            pos = (x * 48 + 33, y * 48 + 42)

            try:
                # Try to load app-specific icon, fall back to default
                icon_path = f"/system/apps/{path}/icon.png"
                if not file_exists(icon_path):
                    icon_path = "/system/apps/sf_menu/default_icon.png"
                sprite = Image.load(icon_path)
                icons.append(Icon(pos, name, icon_idx % APPS_PER_PAGE, sprite))
            except Exception as e:
                print(f"Error loading icon for {path}: {e}")

    return icons


icons = load_page_icons(current_page)
active = 0

# Fade in effect
MAX_ALPHA = 255
alpha = 30


def update():
    global active, icons, alpha, current_page, total_pages

    # Process button inputs to switch between icons
    if io.BUTTON_C in io.pressed:
        active += 1
    if io.BUTTON_A in io.pressed:
        active -= 1
    if io.BUTTON_UP in io.pressed:
        active -= 3
    if io.BUTTON_DOWN in io.pressed:
        active += 3

    # Handle wrapping and page changes
    if active >= len(icons):
        if current_page < total_pages - 1:
            # Move to next page
            current_page += 1
            icons = load_page_icons(current_page)
            active = 0
        else:
            # Wrap to beginning (first page, first icon)
            current_page = 0
            icons = load_page_icons(current_page)
            active = 0
    elif active < 0:
        if current_page > 0:
            # Move to previous page
            current_page -= 1
            icons = load_page_icons(current_page)
            active = len(icons) - 1
        else:
            # Wrap to last page, last icon
            current_page = total_pages - 1
            icons = load_page_icons(current_page)
            active = len(icons) - 1

    # Launch app with error handling
    if io.BUTTON_B in io.pressed:
        app_idx = current_page * APPS_PER_PAGE + active
        if app_idx < len(apps):
            app_path = f"/system/apps/{apps[app_idx][1]}"
            try:
                # Verify the app still exists before launching
                if is_dir(app_path) and file_exists(f"{app_path}/__init__.py"):
                    return app_path
                else:
                    print(f"Error: App {apps[app_idx][1]} not found or missing __init__.py")
            except Exception as e:
                print(f"Error launching app {apps[app_idx][1]}: {e}")

    # Draw UI
    ui.draw_background()
    ui.draw_header()

    # Draw menu icons
    for i in range(len(icons)):
        icons[i].activate(active == i)
        icons[i].draw()

    # Draw label for active menu icon
    if Icon.active_icon:
        label = f"{Icon.active_icon.name}"
        w, _ = screen.measure_text(label)

        # Salesforce blue label background
        screen.brush = brushes.color(0, 112, 210)
        screen.draw(shapes.rounded_rectangle(80 - (w / 2) - 4, 100, w + 8, 15, 4))

        # White text
        screen.brush = brushes.color(255, 255, 255)
        screen.text(label, 80 - (w / 2), 101)

    # Draw page indicator if multiple pages
    if total_pages > 1:
        page_label = f"{current_page + 1}/{total_pages}"
        w, _ = screen.measure_text(page_label)
        screen.brush = brushes.color(0, 112, 210, 200)
        screen.text(page_label, 160 - w - 5, 108)

    # Fade in effect
    if alpha <= MAX_ALPHA:
        screen.brush = brushes.color(0, 0, 0, 255 - alpha)
        screen.clear()
        alpha += 30

    return None


if __name__ == "__main__":
    run(update)
