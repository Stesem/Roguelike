import pygame
from src.suppor import white, purple


class CultistBullet:
    speed = 7
    size = 10
    radius = 5

    def __init__(self, game, master, x, y, target, room):
        self.game = game
        self.master = master
        self.damage = master.damage
        self.rect = None
        self.image = None
        self.position = (x, y)
        self.create_image()
        self.rect.x = x
        self.rect.y = y
        self.direction = None
        self.define_direction()
        self.room = room

    def create_image(self):
        self.image = pygame.Surface([self.size, self.size])

    def define_direction(self, target):
        direct = pygame.math.Vector2(
            target[0] - self.position[0], target[1] - self.position[1]
        )
        if direct.length_squared > 0:
            self.direction = direct.normalize

    def update_position(self):
        if self.room == self.game.dungeon_manager.curren_room:
            self.position = (
                self.position[0] + self.direction[0] * self.speed,
                self.position[1] + self.direction[1] * self.speed,
            )

            self.rect.x = self.position[0]
            self.rect.y = self.position[1]

    def kill(self):
        if self in self.game.bullet_manager.bullet_list:
            self.game.bullet_manager.bullet_list.remove(self)

    def hit_player(self, player):
        if self.rect.colliderect(player.hitbox):
            if player.shild == 0:
                player.hp -= 1
                player.hurt = True
                player.entity_animation.hurt_timer_mark = pygame.time.get_ticks()
            else:
                player.shild -= 1

    def wall_collision(self):
        collide_points = (
            self.rect.bottomleft,
            self.rect.midbottom,
            self.rect.bottomright,
        )
        for wall in self.game.dungeon_manager.current_map.walls:
            if any(
                wall.hitbox.collidepoint(check_point) for check_point in collide_points
            ):
                self.kill()
                break

    def update(self):
        self.update_position()
        self.hit_player()
        self.wall_collision()

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            white,
            (self.rect.x + self.radius / 2, self.rect.y + self.radius / 2),
            self.radius,
        )
        pygame.draw.circle(
            screen,
            purple,
            (self.rect.x + self.radius / 2, self.rect.y + self.radius / 2),
            self.radius - 1,
        )
