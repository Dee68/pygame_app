import pygame
import random
import math


class Target:
    def __init__(self, x, y, speed=4, asset_path="assets/images"):
        self.speed = speed
        self.active = True

        # self.images = [
        #     pygame.image.load(f"{asset_path}/hell.png").convert_alpha(),
        #     pygame.image.load(f"{asset_path}/hell1.png").convert_alpha(),
        #     pygame.image.load(f"{asset_path}/hell2.png").convert_alpha(),
        # ]

        #self.image = random.choice(self.images)
        self.rotor_angle = 0
        self.body_angle = 0
        self.tilt_phase = random.random() * math.pi * 2
        self.body_images = [
            pygame.image.load("assets/images/hell_body_0.png").convert_alpha(),
            pygame.image.load("assets/images/hell_body_1.png").convert_alpha(),
            pygame.image.load("assets/images/hell_body_2.png").convert_alpha(),
        ]

        self.rotor_images = [
            pygame.image.load("assets/images/rotor_0.png").convert_alpha(),
            pygame.image.load("assets/images/rotor_1.png").convert_alpha(),
            pygame.image.load("assets/images/rotor_2.png").convert_alpha(),
        ]
       
        self.body = random.choice(self.body_images)
        self.rotor = random.choice(self.rotor_images)

        self.rect = self.body.get_rect(center=(x, y))#self.image.get_rect(center=(x, y))
        #print(self.image)

    # ---------------- movement / update ----------------

    def update(self, screen_height, slow_motion=False):
        if not self.active:
            return "dead"

        speed = self.speed * (0.4 if slow_motion else 1)

        self.rect.y += speed
        
        #self.rect.y += self.speed

        self.rotor_angle = (self.rotor_angle + 25) % 360

        self.tilt_phase += 0.05

        self.body_angle = 8 * math.sin(self.tilt_phase)

        # escaped to bottom
        if self.rect.top > screen_height:
            #print("Target escaped")
            return "escaped"

        return "alive"

    # ---------------- respawn ----------------

    def reset(self, screen_width):
        self.active = True

        x = random.randint(0, screen_width)
        y = random.randint(-300, -40)

        # self.image = random.choice(self.images)
        # self.rect = self.image.get_rect(center=(x, y))
        self.body = random.choice(self.body_images)
        self.rotor = random.choice(self.rotor_images)

        self.rect = self.body.get_rect(center=(x, y))

    # ---------------- lifecycle ----------------

    def destroy(self):
        self.active = False

    # ---------------- collision helper ----------------

    def get_bbox(self):
        return self.rect

    # ---------------- draw ----------------

    def draw(self, screen):
        if not self.active:
            return

        # Body tilt
        body_surface = pygame.transform.rotate(
            self.body,
            self.body_angle
        )

        body_rect = body_surface.get_rect(
            center=self.rect.center
        )

        screen.blit(body_surface, body_rect)

        # Fake X-axis rotor effect
        scale = abs(math.cos(math.radians(self.rotor_angle)))
        scale = max(scale, 0.2)

        rotor_surface = pygame.transform.scale(
            self.rotor,
            (
                self.rotor.get_width(),
                int(self.rotor.get_height() * scale)
            )
        )

        rotor_surface = pygame.transform.rotate(
            rotor_surface,
            self.rotor_angle
        )

        rotor_rect = rotor_surface.get_rect(
            center=(
                body_rect.centerx,
                body_rect.top + 15
            )
        )

        screen.blit(rotor_surface, rotor_rect)
        # body_surface = pygame.transform.rotate(
        # self.body,
        # self.body_angle
        # )
        
        # body_rect = body_surface.get_rect(
        #     center=self.rect.center
        # )
        
        # rotor_surface = pygame.transform.rotate(
        #     self.rotor,
        #     self.rotor_angle
        # )

        # rotor_rect = rotor_surface.get_rect(
        #     center=(
        #         body_rect.centerx,
        #         body_rect.top + 15
        #     )
        # )

        

        # if self.active:
        #     screen.blit(self.image, self.rect)
           
            