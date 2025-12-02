import sys
import os

sys.path.insert(0, "/system/apps/sf_settings")
os.chdir("/system/apps/sf_settings")

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

# Settings
settings = {
    "brightness": 80,  # percentage
    "led_style": "pulse",  # pulse, solid, off
    "mesh_enabled": True,
    "presence_enabled": True,
}

selected_index = 0
setting_names = ["Brightness", "LED Style", "Mesh Discovery", "BLE Presence"]


def draw_header():
    """Draw settings header"""
    screen.brush = sf_darker_blue
    screen.draw(shapes.rectangle(0, 0, 160, 14))

    screen.font = body_font
    screen.brush = sf_white
    screen.text("Settings", 5, 3)


def draw_status_bar():
    """Draw connectivity and battery status"""
    y = 18
    screen.font = small_font
    screen.brush = sf_gray

    # Wi-Fi status (mock)
    screen.text("WiFi: Connected", 10, y)

    # BLE status
    ble_status = "On" if settings["presence_enabled"] else "Off"
    screen.text(f"BLE: {ble_status}", 95, y)

    # Battery
    battery = get_battery_level() if not is_charging() else 100
    bat_text = f"{battery}%"

    # Battery icon
    y = 30
    pos = (10, y)
    size = (20, 10)

    screen.brush = sf_white
    screen.draw(shapes.rectangle(*pos, *size))
    screen.draw(shapes.rectangle(pos[0] + size[0], pos[1] + 3, 1, 4))

    width = ((size[0] - 2) / 100) * battery
    if width > 0:
        if battery > 50:
            bar_color = sf_green
        elif battery > 20:
            bar_color = sf_orange
        else:
            bar_color = brushes.color(255, 100, 100)
        screen.brush = bar_color
        screen.draw(shapes.rectangle(pos[0] + 1, pos[1] + 1, width, size[1] - 2))

    screen.font = small_font
    screen.brush = sf_darker_blue
    screen.text(bat_text, 35, y + 2)

    # Firmware version
    screen.brush = sf_gray
    screen.text("v1.0.0-beta", 100, y + 2)


def draw_settings_list():
    """Draw settings options"""
    y = 48

    for i, setting_name in enumerate(setting_names):
        # Selection highlight
        if i == selected_index:
            screen.brush = brushes.color(0, 161, 224, 50)
            screen.draw(shapes.rounded_rectangle(8, y - 2, 144, 15, 3))

        # Setting name
        screen.font = small_font
        screen.brush = sf_darker_blue
        screen.text(setting_name, 12, y)

        # Setting value
        if setting_name == "Brightness":
            value = f"{settings['brightness']}%"
        elif setting_name == "LED Style":
            value = settings["led_style"].title()
        elif setting_name == "Mesh Discovery":
            value = "On" if settings["mesh_enabled"] else "Off"
        elif setting_name == "BLE Presence":
            value = "On" if settings["presence_enabled"] else "Off"

        # Value with indicator color
        w, _ = screen.measure_text(value)
        if "On" in value or settings.get("brightness", 0) > 50:
            screen.brush = sf_green
        elif "Off" in value:
            screen.brush = sf_gray
        else:
            screen.brush = sf_orange

        screen.text(value, 150 - w, y)

        y += 17


def draw_footer():
    """Draw control hints"""
    screen.font = small_font
    screen.brush = sf_gray
    screen.text("A/B: Select", 10, 110)
    screen.text("C: Toggle", 80, 110)


def update():
    global selected_index

    # Navigation
    if io.BUTTON_A in io.pressed and selected_index > 0:
        selected_index -= 1
    elif io.BUTTON_B in io.pressed and selected_index < len(setting_names) - 1:
        selected_index += 1

    # Adjust settings (only C button for toggling/cycling)
    if io.BUTTON_C in io.pressed:
        setting = setting_names[selected_index]

        if setting == "Brightness":
            # Cycle brightness: 20% -> 40% -> 60% -> 80% -> 100% -> 20%
            levels = [20, 40, 60, 80, 100]
            current_idx = min(range(len(levels)), key=lambda i: abs(levels[i] - settings["brightness"]))
            settings["brightness"] = levels[(current_idx + 1) % len(levels)]

        elif setting == "LED Style":
            styles = ["pulse", "solid", "off"]
            current = styles.index(settings["led_style"])
            settings["led_style"] = styles[(current + 1) % len(styles)]

        elif setting == "Mesh Discovery":
            settings["mesh_enabled"] = not settings["mesh_enabled"]

        elif setting == "BLE Presence":
            settings["presence_enabled"] = not settings["presence_enabled"]

    # Clear screen
    screen.brush = sf_background
    screen.clear()

    # Draw UI
    draw_header()
    draw_status_bar()
    draw_settings_list()
    draw_footer()

    return None


if __name__ == "__main__":
    run(update)
