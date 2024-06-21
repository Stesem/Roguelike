import pygame
from src.players.entity_base import EntityBase
from random import randint
from src.utils import floor_size, world_size, check_time_passed


class Enemy(EntityBase):
    def __init__(self, game, name, max_hp, spawn_room):
        EntityBase.__init__(self, game, name)
        self.max_hp = max_hp
        self.hp = self.max_hp
        self.room = spawn_room
        self.death_counter = 1
        self.attack_cd = 1000
        self.attack_timer = 0
        self.being_attacked_timer = 0
        self.changing_speed_cd = 1000
        self.changing_speed_timer = 0
        self.loot = []
        """ self.add_loot """

    """ def add_loot(self):
        for _ in range(randint(1, 25)):
            self.loot.append(RedFlask(self.game, self.room)) """

    def spawn(self):
        narrowing = 50
        screen_center = (world_size[0] / 2, world_size[1] / 2)
        spawn_space_x = (screen_center[0] - floor_size[0] / 2) + narrowing
        spawn_space_y = (screen_center[1] - floor_size[1] / 2) + narrowing / 2
        spawn_place_width = floor_size[0] - 2 * narrowing
        spawn_place_height = floor_size[1] - narrowing
        self.rect.x = randint(spawn_space_x, spawn_space_x + spawn_place_width)
        self.rect.y = randint(spawn_space_y, spawn_space_y + spawn_place_height)

    def can_attack(self):
        time = 0
        if check_time_passed(time, self.attack_cd) and not self.hurt:
            self.attack_timer = pygame.time.get_ticks()
            return True

    """ def can_get_hurt(self): """

    def attack_player(self, player):
        if self.can_attack() and self.hitbox.colliderect(player.hitbox):
            player.getting_hit(self)

    def move(self):
        pass
