import pygame
import time
from pathlib import Path

from game.direction import Direction
from game.bullet import Bullet


ANGLE_MAP = {
    Direction.LEFT: 120,
    Direction.CENTER: 90,
    Direction.RIGHT: 60,
}



class Gun:
    def __init__(self, x: int, y: int, asset_path: str):
        self.x = x
        self.y = y

        self.speed = 10

        self.last_shot_time = 0
        self.fire_delay = 0.25
        base = Path(asset_path)
        # load images once
        # self.images = {
        #     Direction.LEFT: pygame.image.load(
        #         f"{asset_path}/gun_left.png"
        #     ).convert_alpha(),

        #     Direction.CENTER: pygame.image.load(
        #         f"{asset_path}/gun_center.png"
        #     ).convert_alpha(),

        #     Direction.RIGHT: pygame.image.load(
        #         f"{asset_path}/gun_right.png"
        #     ).convert_alpha(),
        # }
        self.images = {
            Direction.LEFT: pygame.image.load(base / "gun_left.png").convert_alpha(),
            Direction.CENTER: pygame.image.load(base / "gun_center.png").convert_alpha(),
            Direction.RIGHT: pygame.image.load(base / "gun_right.png").convert_alpha(),
        }

        self.direction = Direction.CENTER
        self.current_image = self.images[self.direction]

        # rect replaces canvas coords
        self.rect = self.current_image.get_rect(center=(x, y))

    # ---------------- movement ----------------

    def move_left(self, screen_width):
        if self.rect.left > 0:
            self.rect.x -= self.speed
            self.set_direction(Direction.LEFT)

    def move_right(self, screen_width):
        if self.rect.right < screen_width:
            self.rect.x += self.speed
            self.set_direction(Direction.RIGHT)

    def aim_center(self):
        self.set_direction(Direction.CENTER)

    # ---------------- direction handling ----------------

    def set_direction(self, direction: Direction):
        self.direction = direction
        self.current_image = self.images[direction]

        # preserve center when swapping images
        center = self.rect.center
        self.rect = self.current_image.get_rect(center=center)

    # ---------------- position helpers ----------------

    def get_position(self):
        return self.rect.topleft

    def get_center(self):
        return self.rect.center

    # ---------------- shooting ----------------

    def shoot(self):
        current_time = time.time()

        if current_time - self.last_shot_time >= self.fire_delay:
            self.last_shot_time = current_time

            x, y = self.get_center()
            angle = ANGLE_MAP[self.direction]

            return Bullet(x, y - 20, angle)

        return None
    
    # ----------------- update -----------------------
    def update(self, keys, screen_width):
        if keys[pygame.K_LEFT]:
            self.move_left(screen_width)
        elif keys[pygame.K_RIGHT]:
            self.move_right(screen_width)
        else:
            self.aim_center()

    # ---------------- draw ----------------

    def draw(self, screen):
        screen.blit(self.current_image, self.rect)