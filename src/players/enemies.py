import pygame
from src.players.entity_base import EntityBase
from random import randint
from src.suppor import floor_size, world_size, check_time_passed


class Enemy(EntityBase):
    def __init__(self, game, name, max_hp, spawn_room):
        super().__init__(game, name)
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
        self.destination_point = None

    def spawn(self):
        screen_center = (world_size[0] / 2, world_size[1] / 2)
        spawn_space_x = screen_center[0] - floor_size[0] / 2
        spawn_space_y = screen_center[1] - floor_size[1] / 2
        spawn_place_width = floor_size[0] - 100
        spawn_place_height = floor_size[1] - 100
        self.rect.x = randint(spawn_space_x, spawn_space_x + spawn_place_width)
        self.rect.y = randint(spawn_space_y, spawn_space_y + spawn_place_height)

    def can_attack(self):
        if check_time_passed(self.attack_timer, self.attack_cd):
            self.attack_timer = pygame.time.get_ticks()
            return True

    def attack_player(self, player):
        if self.can_attack() and self.hitbox.colliderect(player.hitbox):
            player.getting_hit(self)

    def move_to_player(self):
        d_time = self.game.d_time
        direct_vect = pygame.math.Vector2(
            self.game.player.hitbox.x - self.hitbox.x,
            self.game.player.hitbox.y - self.hitbox.y,
        )
        if direct_vect.length_squared() > 0:
            direct_vect.normalize_ip()
            direct_vect.scale_to_length(self.speed * d_time)
        self.set_velocity(direct_vect)

    def chose_random_point(self):
        screen_center = (world_size[0] / 2, world_size[1] / 2)
        range_x = (
            (screen_center[0] - floor_size[0] / 2),
            (screen_center[0] + floor_size[0] / 2),
        )
        range_y = (
            (screen_center[1] - floor_size[1] / 2),
            (screen_center[1] + floor_size[1] / 2),
        )
        point = [randint(range_x[0], range_x[1]), randint(range_y[0], range_y[1])]
        path_to_point = pygame.math.Vector2(
            self.game.player.hitbox.x - point[0], self.game.player.hitbox.y - point[1]
        )
        while path_to_point.length() < 100:
            point = [randint(range_x[0], range_x[1]), randint(range_y[0], range_y[1])]
            path_to_point = pygame.math.Vector2(
                self.game.player.hitbox.x - point[0],
                self.game.player.hitbox.y - point[1],
            )
        self.destination_point = point

    def stay_away_from_player(self, radius):
        d_time = self.game.d_time
        dist_to_player = pygame.math.Vector2(
            self.game.player.hitbox.x - self.hitbox.x,
            self.game.player.hitbox.y - self.hitbox.y,
        ).length()
        if self.destination_point:
            path_to_point = pygame.math.Vector2(
                self.game.player.hitbox.x - self.destination_point[0],
                self.game.player.hitbox.y - self.destination_point[1],
            ).length()
            if path_to_point < radius:
                self.chose_random_point()
        if dist_to_player < radius:
            if not self.destination_point:
                self.chose_random_point()
            dir_vect = pygame.math.Vector2(
                self.destination_point[0] - self.hitbox.x,
                self.destination_point[1] - self.hitbox.y,
            )
            if dir_vect.length_squared() > 0:
                dir_vect.normalize_ip()
                dir_vect.scale_to_length(self.speed * d_time)
                self.set_velocity(dir_vect)
            else:
                self.chose_random_point()
        else:
            self.set_velocity([0, 0])

    def move(self):
        if (
            not self.dead
            and not self.game.player.dead
            and self.hp > 0
            and self.can_move
        ):
            self.move_to_player()
        else:
            self.set_velocity([0, 0])

    def update(self):
        self.basic_update()
        self.move()
        self.attack_player(self.game.player)

    def draw(self, screen):
        screen.blit(self.image, self.rect)


class Abomination(Enemy):
    name = "abomination"
    damage = 15
    speed = 200

    def __init__(self, game, max_hp, room):
        super().__init__(game, self.name, max_hp, room)


class Cultist(Enemy):
    name = "cultist"
    damage = 20
    speed = 300

    def __init__(self, game, max_hp, room):
        super().__init__(game, self.name, max_hp, room)
