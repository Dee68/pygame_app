import pygame
import math


class Bullet:
    def __init__(self, x, y, angle=90, speed=12):
        self.speed = speed
        self.angle = angle
        self.active = True

        # direction vector
        radians = math.radians(angle)
        self.dx = speed * math.cos(radians)
        self.dy = -speed * math.sin(radians)

        self.width = 6
        self.height = 10

        # visual representation
        self.rect = pygame.Rect(x - self.width // 2,
                                y - self.height,
                                self.width,
                                self.height)

        self.color = (255, 255, 0)  # yellow

    # ---------------- movement ----------------

    def update(self, screen_height):
        if not self.active:
            return

        self.rect.x += self.dx
        self.rect.y += self.dy

        # off-screen cleanup
        if self.rect.bottom < 0 or self.rect.top > screen_height:
            self.destroy()

    # ---------------- lifecycle ----------------

    def destroy(self):
        self.active = False

    # ---------------- collision helper ----------------

    def get_bbox(self):
        return self.rect

    # ---------------- draw ----------------

    def draw(self, screen):
        if self.active:
            pygame.draw.rect(screen, self.color, self.rect)