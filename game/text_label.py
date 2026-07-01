import pygame


class TextLabel:
    """
        Generic class to display values
        of score, lives and level on screen.
    """
    
    def __init__(
        self,
        text,
        x,
        y,
        font_size=30,
        color=(0, 0, 0)
    ):
        self.text = text
        self.x = x
        self.y = y
        self.color = color

        self.font = pygame.font.SysFont(
            "Arial",
            font_size
        )

    def set_text(self, text):
        self.text = text
        
    def clear(self):
        self.visible = False

    def show(self):
        self.visible = True

    def reset(self):
        self.text = self.initial_text
        self.visible = True

    def draw(self, screen):
        surface = self.font.render(
            self.text,
            True,
            self.color
        )

        screen.blit(
            surface,
            (self.x, self.y)
        )