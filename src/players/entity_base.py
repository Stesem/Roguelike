import pygame
from src.players.animation import load_sprites_for_animation, AnimationHandler
from src.suppor import basic_entity_size, get_mask_rect


class EntityBase:

    def __init__(self, game, name):
        self.game = game
        self.name = name
        self.path = f"assets/characters/{self.name}"
        self.animation_database = load_sprites_for_animation(f"{self.path}/")
        self.image = pygame.transform.scale(
            pygame.image.load(f"{self.path}/idle/idle0.png"), basic_entity_size
        ).convert_alpha()
        self.rect = self.image.get_rect()
        self.hitbox = get_mask_rect(self.image, self.rect.topleft)
        self.velocity = [0, 0]
        self.hurt = False
        self.dead = False
        self.direction = "right"
        self.can_move = True
        self.entity_animation = AnimationHandler(self)
        self.time = 0
        self.can_get_hurt = True
        self.hurt_time_marker = 0

    def set_velocity(self, new_velocity):
        self.velocity = new_velocity

    def slowing_by_hurt(self):
        base_speed = self.speed
        hurted_speed = base_speed - 70
        if self.hurt:
            self.speed = hurted_speed
        else:
            self.speed = base_speed

    def moving(self):
        return self.velocity[0] != 0 or self.velocity[1] != 0

    def detecting_hurt(self):
        if self.hurt == True:
            self.can_get_hurt = False
            invincibility_time = 300
            if pygame.time.get_ticks() - self.hurt_time_marker > invincibility_time:
                self.hurt_time_marker = pygame.time.get_ticks()
                self.hurt = False
                self.can_get_hurt = True

    def detect_death(self):
        if self.hp <= 0 and not self.dead:
            self.dead = True
            self.entity_animation.animation_frame = 0
            self.can_move = False
            self.velocity = [0, 0]
        if self.death_counter == 0:
            if self.room:
                self.room.enemy_list.remove(self)

    def basic_update(self):
        self.detect_death()
        self.update_hitbox()
        self.entity_animation.update()
        self.rect.move_ip(self.velocity)
        self.hitbox.move_ip(self.velocity)

    def update_hitbox(self):
        self.hitbox = get_mask_rect(self.image, self.rect.topleft)
        self.hitbox.midbottom = self.rect.midbottom

    def wall_collision(self):
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
