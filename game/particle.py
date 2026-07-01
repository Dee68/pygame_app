import pygame
import random


class Particle:
    def __init__(self, x, y):
        self.x = x
        self.y = y

        self.dx = random.uniform(-3, 3)
        self.dy = random.uniform(-3, 3)

        self.life = 40  # frames
        self.radius = 3

        self.color = (255, 140, 0)  # orange
        self.active = True

    # ---------------- update ----------------

    def update(self):
        if self.life <= 0:
            self.active = False
            return False

        self.x += self.dx
        self.y += self.dy

        # gravity
        self.dy += 0.15

        self.life -= 1

        return True

    # ---------------- draw ----------------

    def draw(self, screen):
        if self.active:
            pygame.draw.circle(
                screen,
                self.color,
                (int(self.x), int(self.y)),
                self.radius
            )