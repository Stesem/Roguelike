import pygame
from src.suppor import white, purple


class CultistBullet:
    def __init__(self, game, master, x, y, target, room):
        self.game = game
        self.master = master
        self.damage = master.damage
        self.target = target
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
        self.image.fill(white)
        self.rect = self.image.get_rect()

    def define_direction(self):
        direct = pygame.math.Vector2(
            self.target[0] - self.position[0], self.target[1] - self.position[1]
        )
        if direct.length_squared() > 0:
            self.direction = direct.normalize()

    def update_position(self):
        if self.room == self.game.dungeon_manager.current_room:
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
            if player.shield == 0:
                player.hp -= 1
                player.hurt = True
                player.entity_animation.hurt_timer_mark = pygame.time.get_ticks()
            else:
                player.shield -= 1

    def wall_collision(self):
        collide_points = (
            self.rect.bottomleft,
            self.rect.midbottom,
            self.rect.bottomright,
        )
        for wall in self.game.dungeon_manager.current_room.walls:
            if any(
                wall.rect.collidepoint(check_point) for check_point in collide_points
            ):
                self.kill()
                break

    def update(self):
        self.update_position()
        self.hit_player(self.game.player)
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


class PlayerBullet:
    def __init__(self, game, master, x, y, target, room):
        self.game = game
        self.master = master
        self.damage = master.damage
        self.target = target
        self.position = (x, y)
        self.size = 10  # чуть больше чем у энеми
        self.speed = 5  # скорость надо выставить
        self.create_image()
        self.rect.x = x
        self.rect.y = y
        self.direction = None
        self.define_direction()
        self.room = room

    def create_image(self):
        self.image = pygame.Surface([self.size, self.size])
        self.image.fill((0, 255, 0))  # зеленым пусть будет
        self.rect = self.image.get_rect()

    def define_direction(self):
        direct = pygame.math.Vector2(
            self.target[0] - self.position[0], self.target[1] - self.position[1]
        )
        if direct.length_squared() > 0:
            self.direction = direct.normalize()

    def update_position(self):
        if self.room == self.game.dungeon_manager.current_room:
            self.position = (
                self.position[0] + self.direction[0] * self.speed,
                self.position[1] + self.direction[1] * self.speed,
            )

            self.rect.x = self.position[0]
            self.rect.y = self.position[1]

    def kill(self):
        if self in self.game.bullet_manager.bullet_list:
            self.game.bullet_manager.bullet_list.remove(self)

    def hit_enemy(self, enemy):
        if self.rect.colliderect(enemy.hitbox):
            enemy.hp -= self.damage
            self.kill()  # пуля исчезает когда попадает в энеми

    def wall_collision(self):
        collide_points = (
            self.rect.bottomleft,
            self.rect.midbottom,
            self.rect.bottomright,
        )
        for wall in self.game.dungeon_manager.current_room.walls:
            if any(
                wall.rect.collidepoint(check_point) for check_point in collide_points
            ):
                self.kill()
                break

    def update(self):
        self.update_position()
        # проверка на коллизии с энеми
        for enemy in self.game.enemy_manager.enemy_list:
            self.hit_enemy(enemy)
        self.wall_collision()

    def draw(self, screen):
        pygame.draw.circle(
            screen,
            (0, 255, 0),  # зеленый цвет пули
            (self.rect.x + self.size // 2, self.rect.y + self.size // 2),
            self.size // 2,
        )

class BulletManager:

    def __init__(self, game):
        self.game = game
        self.bullets = []

    def remove_bullets(self):
        for bullet in self.bullets:
            if self.game.world_manager.current_room is not bullet.room:
                self.bullets.remove(bullet)
                #self.kill(bullet)

    def add_bullet(self, bullet):
        self.bullets.append(bullet)

    def kill(self, bullet):
        self.bullets.remove(bullet)

    def update(self):
        self.remove_bullets()
        for bullet in self.bullets:
            bullet.update()

    def draw(self):
        for bullet in self.bullets:
            bullet.draw()