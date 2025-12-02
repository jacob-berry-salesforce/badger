import math
import random
from badgeware import brushes, shapes, io, screen, Matrix, get_battery_level, is_charging

# Salesforce colors
black = brushes.color(0, 0, 0)
sf_blue = brushes.color(0, 112, 210)
sf_darker_blue = brushes.color(3, 45, 96)
sf_light_blue = brushes.color(186, 218, 255)
sf_white = brushes.color(255, 255, 255)
sf_cloud_gray = brushes.color(243, 243, 243)
sf_cloud_fade = brushes.color(186, 218, 255, 150)


def draw_background():
    # Draw corner blacks for rounded rectangle
    screen.brush = black
    screen.draw(shapes.rectangle(0, 0, 10, 10))
    screen.draw(shapes.rectangle(150, 0, 10, 10))
    screen.draw(shapes.rectangle(0, 110, 10, 10))
    screen.draw(shapes.rectangle(150, 110, 10, 10))

    # Draw gradient background (blue to light blue)
    for y in range(120):
        # Calculate gradient from darker blue to light blue
        progress = y / 120
        r = int(0 + (186 - 0) * progress)
        g = int(112 + (218 - 112) * progress)
        b = int(210 + (255 - 210) * progress)
        screen.brush = brushes.color(r, g, b)
        screen.draw(shapes.rectangle(0, y, 160, 1))

    # Overlay with rounded corners
    screen.brush = brushes.color(0, 95, 178, 50)  # Semi-transparent overlay
    screen.draw(shapes.rounded_rectangle(0, 0, 160, 120, 8))


class CloudPattern:
    clouds = []
    max_clouds = 15
    cloud_added_at = None
    clouds_added = 0
    speed = 300

    def update():
        if CloudPattern.cloud_added_at is None:
            CloudPattern.cloud_added_at = io.ticks

        if io.ticks - CloudPattern.cloud_added_at > CloudPattern.speed:
            CloudPattern.add_cloud()

    def add_cloud():
        CloudPattern.clouds.append({
            'width': random.randint(15, 40),
            'y': random.randint(20, 100),
            'alpha': random.randint(20, 60)
        })
        CloudPattern.cloud_added_at = io.ticks
        CloudPattern.clouds_added += 1
        if len(CloudPattern.clouds) > CloudPattern.max_clouds:
            CloudPattern.clouds = CloudPattern.clouds[1:]


# Pre-populate clouds
for _ in range(15):
    CloudPattern.add_cloud()


def draw_clouds():
    """Draw floating cloud pattern effect"""
    CloudPattern.update()

    for i, cloud in enumerate(CloudPattern.clouds):
        # Calculate position with slow drift
        x = ((io.ticks / 50) + i * 20) % 180 - 20
        y = cloud['y']

        # Draw cloud as soft rounded shapes
        screen.brush = brushes.color(255, 255, 255, cloud['alpha'])
        screen.draw(shapes.circle(x, y, 8))
        screen.draw(shapes.circle(x + 8, y - 2, 6))
        screen.draw(shapes.circle(x + 14, y, 7))

    # Fade at top
    screen.brush = sf_cloud_fade
    screen.draw(shapes.rectangle(0, 15, 160, 5))


def draw_header():
    """Draw Salesforce AI Centre header with logo"""
    # Header background with subtle gradient
    for y in range(16):
        alpha = 255 - int(y * 3)  # Fade slightly towards bottom
        screen.brush = brushes.color(0, 95, 178, alpha)
        screen.draw(shapes.rectangle(0, y, 160, 1))

    # Create animated header text
    dots = "." * int(math.sin(io.ticks / 250) * 2 + 2)
    label = f"AI Centre{dots}"

    # Draw the title with slight shadow
    screen.brush = brushes.color(0, 0, 0, 80)
    screen.text(label, 6, 3)
    screen.brush = sf_white
    screen.text(label, 5, 2)

    # Draw battery indicator
    if is_charging():
        battery_level = (io.ticks / 20) % 100
    else:
        battery_level = get_battery_level()

    pos = (137, 4)
    size = (16, 8)

    # Battery with glow
    screen.brush = brushes.color(255, 255, 255, 100)
    screen.draw(shapes.rectangle(pos[0] - 1, pos[1] - 1, size[0] + 2, size[1] + 2))

    # Battery outline
    screen.brush = sf_white
    screen.draw(shapes.rectangle(*pos, *size))
    screen.draw(shapes.rectangle(pos[0] + size[0], pos[1] + 2, 1, 4))

    # Battery fill with gradient
    width = ((size[0] - 4) / 100) * battery_level
    if width > 0:
        # Green to yellow gradient based on battery level
        if battery_level > 50:
            bar_color = brushes.color(95, 237, 131)
        elif battery_level > 20:
            bar_color = brushes.color(255, 220, 100)
        else:
            bar_color = brushes.color(255, 100, 100)

        screen.brush = bar_color
        screen.draw(shapes.rectangle(pos[0] + 2, pos[1] + 2, width, size[1] - 4))


def draw_lightning_bolt(x, y):
    """Draw a small lightning bolt icon"""
    screen.brush = sf_white
    # Simple lightning bolt shape using lines
    screen.draw(shapes.line(x, y, x + 2, y + 4, 2))
    screen.draw(shapes.line(x + 2, y + 4, x, y + 8, 2))
    screen.draw(shapes.line(x, y + 4, x + 3, y + 4, 2))
