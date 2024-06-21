import pygame
from src.players.player import Player
from src.map.dungeon_manager import DungeonManager
from src.utils import world_size
from time import time

pygame.init()
pygame.mixer.init()


class Game:
    def __init__(self):
        self.display = pygame.display.set_mode(world_size)
        self.screen = pygame.Surface(world_size).convert()
        self.clock = pygame.time.Clock()
        self.player = Player(self)
        self.dungeon_manager = DungeonManager(self)
        self.running = True
        self.d_time = 0
        self.fps = 60
        self.screen_position = (0, 0)

    def update_groups(self):
        self.player.update()

    def draw_groups(self):
        self.dungeon_manager.draw_dungeon(self.screen)
        if self.player:
            self.player.draw(self.screen)

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        self.player.input()

    def run_game(self):
        previous_time = time()
        while self.running:
            self.clock.tick(self.fps)
            now_time = time()
            self.d_time = now_time - previous_time
            previous_time = now_time
            self.screen.fill((0, 0, 0))
            self.input()
            self.update_groups()
            self.draw_groups()
            self.display.blit(self.screen, self.screen_position)
            if self.running:
                pygame.display.flip()
        pygame.quit()
