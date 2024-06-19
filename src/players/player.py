import pygame
from src.players.entity_base import EntityBase
from math import sqrt


class Player(EntityBase):
    name = "player"
    speed = 10
    max_hp = 100
    shield = 1
    strength = 1
    hp = max_hp
    items = []

    def __init__(self, game):
        EntityBase.__init__(self, game, self.name)
        self.weapon = None
        self.attacking = False
        self.interaction = True
        self.attack_cooldown = 350  # ms
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

        # balancing velocity moving diagonal
        if 0 not in vel_list:
            velocity = rms_velocity / (abs(vel_list[0]) + abs(vel_list[1]))
            vel_list_fixed = [elem * velocity for elem in vel_list]
            self.set_velocity(vel_list_fixed)
        else:
            self.set_velocity(vel_list)

    def update(self):
        if self.can_move:
            self.rect.move_ip(*self.velocity)

    def draw(self, surface):
        surface.blit(self.image, self.rect)
