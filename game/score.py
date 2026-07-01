import pygame

class Score: 
    def __init__(self, x=20, y=20): 
        self.x = x 
        self.y = y 
        self.value = 0 
        # Create a font object 
        self.font = pygame.font.SysFont("Arial", 32) 
        
    def add(self, points=1): 
        self.value += points 
        
        
    def reset(self): 
        self.value = 0 
        
    def draw(self, screen): 
        # Render the text 
        text_surface = self.font.render( 
            f"Score: {self.value}", 
            True, # Anti-aliasing 
            (0, 0, 0) # Black text 
            ) 
        # Draw it on the screen 
        screen.blit(text_surface, (self.x, self.y))