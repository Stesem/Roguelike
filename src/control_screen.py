import pygame
import sys

class ControlScreen:
    def __init__(self, game):
        self.game = game
        self.font = pygame.font.Font(None, 36)
        self.instructions = [
            "WASD - Moving",
            "RMB - Interact",
            "Press Space bar"
        ]
        self.is_active = True

    def draw(self):
        # Darken the background
        dark_overlay = pygame.Surface(self.game.screen.get_size()).convert_alpha()
        dark_overlay.fill((0, 0, 0, 180))  # Darken with semi-transparency
        self.game.screen.blit(dark_overlay, (0, 0))
        
        # Draw instructions
        for idx, line in enumerate(self.instructions):
            text_surface = self.font.render(line, True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(self.game.screen.get_width() // 2, 100 + idx * 40))
            self.game.screen.blit(text_surface, text_rect)

    def update(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.is_active = False
