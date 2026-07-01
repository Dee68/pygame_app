import pygame
from game.game_state import GameState
from game.gun import Gun
from game.target import Target
from game.particle import Particle
#from game.score import Score
import random
from game.text_label import TextLabel
import config
import math

class Game:
    def __init__(self):
        # set up the screen width and height
        self.screen = pygame.display.set_mode((config.WIDTH, config.HEIGHT))
        # load a background image and stretch to screen size
        self.bg_image = pygame.image.load(
            "assets/images/sky.png"
        ).convert()
        self.bg_image = pygame.transform.scale(
            self.bg_image,
            (config.WIDTH, config.HEIGHT)
        )
        #
        pygame.display.set_caption("Shooting Game version 1.0")
        pygame.mixer.init()
        self.clock = pygame.time.Clock()
    
        self.running = True
        self.score = 0
        # self.lives = 5
        # self.level = 1
        self.lives = config.STARTING_LIVES
        self.level = config.START_LEVEL
        self.target_speed = config.TARGET_SPEED
        self.max_targets = config.MAX_TARGETS
        self.slow_motion = False
        self.slow_motion_end = 0
        self.spawn_timer = 0
        self.spawn_delay = 1200 # milliseconds
        self.last_spawn_time = pygame.time.get_ticks()
        self.life_warning = False
        self.life_warning_start = 0
        self.life_warning_duration = 1000   # milliseconds
        
        self.level_message = False
        self.level_message_start = 0
        self.level_message_duration = 1000 # milliseconds
        
        self.score_label = TextLabel(
            f"Score: {self.score}",
            20,
            20
        )

        self.lives_label = TextLabel(
            f"Lives: {self.lives}",
            200,
            20,
            color="Grey"
        )

        self.level_label = TextLabel(
            f"Level: {self.level}",
            400,
            20,
            color="#0000FFA4"
        )
        self.state = GameState.MENU
        self.shoot_sound = pygame.mixer.Sound("assets/sounds/gun_shot.mp3")
        self.bg_sound = pygame.mixer.Sound("assets/sounds/start_game.mp3")
        self.great_sound = pygame.mixer.Sound("assets/sounds/doing_great.mp3")
        
        self.rotor_angle = 0
        self.body_angle = 0
        self.tilt_phase = random.random() * math.pi * 2
        # initialize gun
        self.gun = Gun(350,580,"assets/images")
        
        self.bullets = []

        self.targets = []
        self.particles = []
        

        
    #
    def spawn_target(self):
        x = random.randint(0, self.screen.get_width())
        y = random.randint(-300, -50)

        speed = self.target_speed

        target = Target(
            x=x,
            y=y,
            speed=speed,
            asset_path="assets/images"
        )

        self.targets.append(target)
     
     
    #
    def maybe_spawn_target(self):
        """
        Spawn a target when enough time has elapsed.
        """

        if self.state != GameState.PLAYING:
            return

        now = pygame.time.get_ticks()

        if (
            len(self.targets) < self.max_targets
            and now - self.last_spawn_time >= self.spawn_delay
        ):
            self.spawn_target()
            self.last_spawn_time = now
        
    #
    def spawn_particles(self, x, y):
        for _ in range(10):  # explosion size
            self.particles.append(Particle(x, y))
    
    #
    def show_life_warning(self):
        #print("Life warning triggered")
        self.life_warning = True
        self.life_warning_start = pygame.time.get_ticks()
        #self.life_warning_duration = 1500  # 1.5 seconds
        
    #
    def increase_difficulty(self):
        """
        Increase the game's difficulty.
        """

        self.max_targets += 1

        # Spawn targets faster
        self.spawn_delay = max(400, self.spawn_delay - 100)

        # make targets fall faster
        self.target_speed += 0.5
     
    
    #
    def show_level_complete(self):
        self.level_message = True
        self.level_message_start = pygame.time.get_ticks()  
        
     
    #
    def update_level(self):
        """
        Check if the player has reached the next level.
        """

        new_level = (self.score // config.LEVEL_SCORE) + 1

        if new_level > self.level:
            self.level = new_level

            self.level_label.set_text(
                f"Level: {self.level}"
            )

            self.show_level_complete()
            
            # Enable slow motion
            self.slow_motion = True
            self.slow_motion_end = pygame.time.get_ticks() + 1000

            self.increase_difficulty()
            
    #
    def handle_escape(self,target):
        #print("handle escaped called")
        self.lives -= 1
        # Update the UI label
        self.lives_label.set_text(f"Lives: {self.lives}")

        # Show temporary warning
        self.show_life_warning()

        if self.lives <= 0:
            self.show_game_over()
            return

        target.reset(self.screen.get_width())
    #
    def handle_shoot(self):
        bullet = self.gun.shoot()
        if bullet:
            self.bullets.append(bullet)
            self.shoot_sound.play()
    
    def start_game(self):
        self.state = GameState.PLAYING
        self.bg_sound.play(-1) # continuos
        # reset gameplay values
        self.score = 0
        self.lives = 5
        self.level = 1

        self.target_speed = config.TARGET_SPEED
        
        self.score_label.set_text("Score: 0")
        self.lives_label.set_text("Lives: 5")
        self.level_label.set_text("Level: 1")

        self.score_label.show()
        self.lives_label.show()
        self.level_label.show()

        # clear objects
        self.bullets.clear()
        self.targets.clear()
        self.particles.clear()
        
        

        # reset timers
        self.spawn_timer = 0

        # recreate gun
        self.gun = Gun(350, 580, "assets/images")

        # spawn initial wave
        for _ in range(5):
            self.spawn_target()        
            
    
    #
    def draw_menu(self):
        self.screen.fill((10, 100, 240))

        font = pygame.font.SysFont(None, 48)
        title = font.render("SHOOTING GAME", True, (255, 255, 255))

        small = pygame.font.SysFont(None, 28)
        start = small.render("Press ENTER to Start", True, (200, 200, 200))

        self.screen.blit(title, (200, 200))
        self.screen.blit(start, (220, 300))
        
    #
    def show_game_over(self):
        self.state = GameState.GAME_OVER
        pygame.mixer.stop()
        self.targets.clear()
        self.bullets.clear()
        self.particles.clear()
        
    
    #
    def draw_game_over(self):
        self.screen.fill((20, 20, 20))

        font = pygame.font.SysFont(None, 64)
        small = pygame.font.SysFont(None, 32)

        title = font.render("GAME OVER", True, (255, 0, 0))
        score = small.render(f"Final Score: {self.score}", True, (255, 255, 255))
        level = small.render(f"Level Reached: {self.level}", True, (200, 200, 255))
        restart = small.render("Press R to Restart", True, (200, 200, 200))
        quit_text = small.render("Press ESC to Quit", True, (200, 200, 200))

        self.screen.blit(title, (200, 150))
        self.screen.blit(score, (200, 230))
        self.screen.blit(level, (200, 270))
        self.screen.blit(restart, (200, 330))
        self.screen.blit(quit_text, (200, 370))
        
    #
    def handle_game_over_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.start_game()

                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    
    
    #
    def handle_menu_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    self.start_game()
    
    # check collision of bullet and target
    def check_collisions(self):
        for bullet in self.bullets[:]:  # copy list 
            for target in self.targets[:]:

                if bullet.rect.colliderect(target.rect):

                    bullet.destroy()
                    target.destroy()
                    self.spawn_particles(*target.rect.center)
                    # remove from lists safely
                    if bullet in self.bullets:
                        self.bullets.remove(bullet)

                    if target in self.targets:
                        self.targets.remove(target)

                    self.score += 1
                    self.score_label.set_text(f"Score: {self.score}")
                    # add sound effect for score = 10
                    if self.score == 10:
                        self.great_sound.play()
                        
                    self.update_level()
                    
                    break
            
        
    def run(self):
        while self.running:
            # self.handle_events()
            # self.update()
            # self.draw()
            if self.state == GameState.MENU:
                self.handle_menu_events()
                self.draw_menu()

            elif self.state == GameState.PLAYING:
                self.handle_events()
                self.update()
                self.draw()

            elif self.state == GameState.GAME_OVER:
                self.handle_game_over_events()
                self.draw_game_over()
                
            
            pygame.display.flip()
            self.clock.tick(60)
            
    
    def handle_events(self):

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.KEYDOWN:

                if event.key == pygame.K_SPACE:
                    self.handle_shoot()
                    
                    
    
    #
    def update(self):
        if self.state != GameState.PLAYING:
            return

        keys = pygame.key.get_pressed()
        self.gun.update(keys, self.screen.get_width())
        
        #self.rect.y += self.speed

        self.rotor_angle = (self.rotor_angle + 25) % 360

        self.tilt_phase += 0.05

        self.body_angle = 8 * math.sin(self.tilt_phase)

        # Update bullets
        for bullet in self.bullets:
            bullet.update(self.screen.get_height())

        # Update targets
        for target in self.targets[:]:
            state = target.update(
                self.screen.get_height(),
                self.slow_motion
            )

            if state == "escaped":
                self.handle_escape(target)

        # Spawn new targets if needed
        self.maybe_spawn_target()

        # Collision detection
        self.check_collisions()

        # Update particles
        for particle in self.particles:
            particle.update()

        self.particles = [
            p for p in self.particles
            if p.active
        ]
        
        
    def draw(self):

        # Background first
        self.screen.blit(self.bg_image, (0, 0))

        # draw score
        self.score_label.draw(self.screen)
        # draw lives
        self.lives_label.draw(self.screen)
        # draw level
        self.level_label.draw(self.screen)
        
        self.gun.draw(self.screen)

        for bullet in self.bullets:
            bullet.draw(self.screen)

        for target in self.targets:
            target.draw(self.screen)
            
        self.check_collisions()
        # draw particles
        for particle in self.particles:
            particle.draw(self.screen)
        
        # show message briefly
        if self.level_message:
            font = pygame.font.SysFont("Arial", 32, bold=True)

            text = font.render(
                "LEVEL COMPLETE!",
                True,
                (0, 180, 0)
            )

            rect = text.get_rect(
                center=(
                    config.WIDTH // 2,
                    config.HEIGHT // 2
                )
            )

            self.screen.blit(text, rect)
        # show life span warning
        if self.life_warning:
            font = pygame.font.SysFont("Arial", 28, bold=True)

            warning = font.render("-1 LIFE!", True, (255, 0, 0))

            rect = warning.get_rect(
                center=(config.WIDTH // 2, 80)
            )

            self.screen.blit(warning, rect)

        pygame.display.flip()