import pygame
from src.players.entity_base import EntityBase
from math import sqrt
from src.utils import get_mask_rect

pygame.init()


class Player(EntityBase):
    name = "player"
    speed = 10
    max_hp = 100
    hp = max_hp

    def __init__(self, game):
        super().__init__(game, self.name)
        self.weapon = None
        self.rect = self.image.get_rect(center=(500, 250))
        self.hitbox = get_mask_rect(self.image, self.rect.topleft)
        self.hitbox.midbottom = self.rect.midbottom
        self.attacking = False
        self.interaction = True
        self.attack_cooldown = 350
        self.room = None
        self.death_counter = 1
        self.falling = False
        self.floor_value = self.rect.y

    def input(self):
        pressed = pygame.key.get_pressed()
        if pressed[pygame.K_w]:
            self.direction = "up"
        if pressed[pygame.K_s]:
            self.direction = "down"
        if pressed[pygame.K_a]:
            self.direction = "left"
        if pressed[pygame.K_d]:
            self.direction = "right"

        vel_up = [0, -self.speed]
        vel_up = [i * pressed[pygame.K_w] for i in vel_up]
        vel_down = [0, self.speed]
        vel_down = [i * pressed[pygame.K_s] for i in vel_down]
        vel_left = [-self.speed, 0]
        vel_left = [i * pressed[pygame.K_a] for i in vel_left]
        vel_right = [self.speed, 0]
        vel_right = [i * pressed[pygame.K_d] for i in vel_right]
        vel = zip(vel_up, vel_down, vel_left, vel_right)
        vel_list = [sum(elem) for elem in vel]

        rms_velocity = sqrt(pow(vel_list[0], 2) + pow(vel_list[1], 2))

        if 0 not in vel_list:

            velocity = rms_velocity / (abs(vel_list[0]) + abs(vel_list[1]))
            vel_list_fixed = [elem * velocity for elem in vel_list]
            self.set_velocity(vel_list_fixed)
        else:
            self.set_velocity(vel_list)

    def wall_and_passage_collision(self):
        position_after_moving = self.hitbox.move(self.velocity)
        collide_points = (
            position_after_moving.midbottom,
            position_after_moving.bottomleft,
            position_after_moving.bottomright,
        )
        for wall in self.game.dungeon_manager.current_room.walls:
            if any(wall.rect.collidepoint(point) for point in collide_points):
                self.set_velocity([0, 0])
                return

        """ if not collided_with_wall:
            for passage in current_room.passages:
                if any(
                    passage.rect.collidepoint(check_point)
                    for check_point in collide_points
                ):
                    if passage.rect.collidepoint(collide_points[1]):
                        self.game.dungeon_manager.go_to_next_room(passage)
                    break """

    def update(self):
        if self.death_counter == 0:
            return
        self.entity_animation.update()
        self.wall_and_passage_collision()
        if self.can_move:
            self.rect.move_ip(self.velocity)
            self.hitbox.move_ip(self.velocity)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
