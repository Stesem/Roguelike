from random import randint
from src.players.enemies import Abomination, Cultist
from src.map.room import Room


class EnemyManager:
    def __init__(self, game):
        self.game = game
        self.enemy_list = []

    def draw_enemies(self, screen):
        for enemy in self.game.dungeon_manager.current_room.enemy_list:
            enemy.draw(screen)

    def fill_enemy_list(self):
        self.enemy_list.clear()
        for enemy in self.game.dungeon_manager.current_room.enemy_list:
            self.enemy_list.append(enemy)

    def add_enemies_to_room(self, room):
        abomination_quantity = randint(2, 6)
        cultists_quantity = randint(1, 3)
        for _ in range(abomination_quantity):
            room.enemy_list.append(Abomination(self.game, max_hp=100, room=room))
            room.enemy_list[-1].spawn()
        for _ in range(cultists_quantity):
            room.enemy_list.append(Cultist(self.game, max_hp=60, room=room))
            room.enemy_list[-1].spawn()

    def add_enemies_to_dingeon(self):
        self.fill_enemy_list()
        for row in self.game.dungeon_manager.dungeon.map:
            for room in row:
                if isinstance(room, Room) and room.type == "normal":
                    self.add_enemies_to_room(room)

    def update_enemy_group(self):
        self.fill_enemy_list()
        for enemy in self.game.dungeon_manager.current_room.enemy_list:
            enemy.update()
