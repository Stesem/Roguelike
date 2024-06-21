import pygame
from random import randint
from src.map.room import Room


class EnemyManager:
    def __init__(self, game):
        self.game = game
        self.enemy_list = []

    def draw_enemies(self):
        for enemy in self.game.dungeon_manager.current_room.enemy_list:
            enemy.draw()

    def set_enemy_list(self):
        self.enemy_list.clear()
        for enemy in self.game.dungeon_manager.current_room.enemy_list:
            self.enemy_list.append(enemy)
