import pygame
from src.players.player import Player
from src.map.dungeon import Dungeon
pygame.init()
pygame.mixer.init()


world_size = (1280, 720)


class Game():
    def __init__(self):
        self.display = pygame.display.set_mode(world_size)
        self.screen = pygame.Surface(world_size).convert()
        self.clock = pygame.time.Clock()
        self.player = Player(self)
        self.dungeon = Dungeon()
        self.running = True
        self.game_time = None
        self.fps = 60
        self.screen_position = (0, 0)
        
    def update_groups(self):
        self.dungeon.update()
        self.player.update()
    
    def draw_groups(self):
        if self.dungeon:
            self.dungeon.draw(self.screen)
        if self.player:
            self.player.draw(self.screen)

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        self.player.input()
        pressed = pygame.key.get_pressed()
        
    def run_game(self):
        while self.running:
            self.map = self.dungeon.create_map("start_room")
            self.clock.tick(self.fps)
            self.screen.fill((0, 0, 0))
            self.input()
            self.update_groups()
            self.draw_groups()
            self.game_time = pygame.time.get_ticks()
            self.display.blit(self.screen, self.screen_position)
            if self.running:
                pygame.display.flip()
        pygame.quit()

