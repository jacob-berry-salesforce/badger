import math
from badgeware import brushes, shapes, io, Matrix, screen

# Salesforce bold icon colors (cloud-themed palette)
bold = [
    brushes.color(0, 112, 210),    # Salesforce blue
    brushes.color(95, 237, 131),   # Success green
    brushes.color(255, 186, 88),   # Warning orange
    brushes.color(186, 218, 255),  # Light blue
    brushes.color(255, 128, 210),  # Pink
    brushes.color(110, 68, 255),   # Purple
]

# Create faded variants for inactive icons
fade = 2.5
faded = [
    brushes.color(0 / fade, 112 / fade, 210 / fade),
    brushes.color(95 / fade, 237 / fade, 131 / fade),
    brushes.color(255 / fade, 186 / fade, 88 / fade),
    brushes.color(186 / fade, 218 / fade, 255 / fade),
    brushes.color(255 / fade, 128 / fade, 210 / fade),
    brushes.color(110 / fade, 68 / fade, 255 / fade),
]

# Cloud-shaped icon (more rounded than squircle)
cloud_shape = shapes.squircle(0, 0, 20, 6)  # Higher n value = more rounded
shade_brush = brushes.color(0, 0, 0, 40)


class Icon:
    active_icon = None

    def __init__(self, pos, name, index, icon):
        self.active = False
        self.pos = pos
        self.icon = icon
        self.name = name
        self.index = index
        self.spin = False
        self.bounce = False

    def activate(self, active):
        # If this icon wasn't already activated, flag it for animation
        if not self.active and active:
            self.spin = True
            self.spin_start = io.ticks
        self.active = active
        if active:
            Icon.active_icon = self

    def draw(self):
        width = 1
        height = 1
        sprite_width = self.icon.width
        sprite_offset = sprite_width / 2
        y_offset = 0

        if self.spin:
            # Create spin animation that runs over 100ms
            speed = 100
            frame = io.ticks - self.spin_start

            # Calculate width during animation
            width = round(math.cos(frame / speed) * 3) / 3

            # Ensure width never reduces to zero
            width = max(0.1, width) if width > 0 else min(-0.1, width)

            # Determine sprite offset and scale to match tile width
            sprite_width = width * self.icon.width
            sprite_offset = abs(sprite_width) / 2

            # Once animation completed, unset spin flag
            if frame > (speed * 6):
                self.spin = False

        # Add gentle bounce for active icon
        if self.active:
            y_offset = math.sin(io.ticks / 200) * 2

        # Transform to icon position with bounce
        cloud_shape.transform = Matrix().translate(self.pos[0], self.pos[1] + y_offset).scale(width, height)

        # Draw icon shadow
        screen.brush = shade_brush
        cloud_shape.transform = cloud_shape.transform.scale(1.1, 1.1)
        screen.draw(cloud_shape)

        # Draw icon body (cloud shape)
        cloud_shape.transform = cloud_shape.transform.scale(1 / 1.1, 1 / 1.1)
        if self.active:
            screen.brush = bold[self.index]
        else:
            screen.brush = faded[self.index]

        cloud_shape.transform = cloud_shape.transform.translate(-1, -1)
        screen.draw(cloud_shape)

        # Add subtle highlight
        cloud_shape.transform = cloud_shape.transform.translate(2, 2)
        screen.brush = brushes.color(255, 255, 255, 30 if self.active else 10)
        screen.draw(cloud_shape)

        # Draw the icon sprite - bigger and centered
        if sprite_width > 0:
            self.icon.alpha = 255 if self.active else 120
            # Scale to 32px (bigger) and center it properly
            scaled_size = 32 if self.active else 30
            scaled_width = scaled_size * width
            scaled_offset = abs(scaled_width) / 2
            screen.scale_blit(
                self.icon,
                self.pos[0] - scaled_offset,
                self.pos[1] - scaled_size/2 + y_offset,
                scaled_width,
                scaled_size,
            )
