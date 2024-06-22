import pygame
from src.players.player import Player
from src.map.dungeon_manager import DungeonManager
from src.players.enemy_manager import EnemyManager
from src.suppor import world_size
from time import time
from src.items.bullet import BulletManager
from src.control_screen import ControlScreen

pygame.init()
pygame.mixer.init()


class Game:
    def __init__(self):
        self.display = pygame.display.set_mode(world_size)
        self.screen = pygame.Surface(world_size).convert()
        self.clock = pygame.time.Clock()
        self.player = Player(self)
        self.dungeon_manager = DungeonManager(self)
        self.enemy_manager = EnemyManager(self)
        self.bullet_manager = BulletManager(self)
        self.running = True
        self.d_time = 0
        self.fps = 60
        self.screen_position = (0, 0)
        self.control_screen = ControlScreen(self)
        self.show_control_screen = True

    def update_groups(self):
        self.dungeon_manager.update_dungeon()
        self.enemy_manager.update_enemy_group()
        self.player.update()
        self.bullet_manager.update()

    def draw_groups(self):
        self.dungeon_manager.draw_dungeon(self.screen)
        self.enemy_manager.draw_enemies(self.screen)
        if self.player:
            self.player.draw(self.screen)
        self.bullet_manager.draw(self.screen)

    def input(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        self.player.input()

    def run_game(self):
        previous_time = time()
        self.enemy_manager.add_enemies_to_dingeon()
        while self.running:
            self.clock.tick(self.fps)
            now_time = time()
            self.d_time = now_time - previous_time
            previous_time = now_time
            self.screen.fill((0, 0, 0))

            if self.control_screen.is_active:
                self.control_screen.update()
                self.control_screen.draw()
            else:
                self.input()
                self.update_groups()
                self.draw_groups()
                if self.dungeon_manager.finished:
                    self.control_screen.draw_congrats_message()
                else:
                    self.display.blit(self.screen, self.screen_position)
            pygame.display.flip()
        pygame.quit()
