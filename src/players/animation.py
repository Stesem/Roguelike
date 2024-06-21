import pygame
import src.utils as utils
import os


def load_sprites_for_animation(path, sprite_size=utils.basic_entity_size):
    animation_data = {"IDLE": [], "WALK": [], "HURT": [], "DEAD": []}
    animation_states = os.listdir(path)
    for state in animation_states:
        sub_states = os.listdir({path}/{state})
        for sub_state in sub_states:
            key = state.upper()
            animation_image = pygame.image.load(
                path + state + "/" + sub_state
            ).convert_alpha()
            animation_image = pygame.transform.scale(animation_image, sprite_size)
            animation_data[key].append(animation_image)
    return animation_data


class AnimationHandler:
    def __init__(self, entity, death_frames=4, animation_speed=25):
        self.entity = entity
        self.direction = "right"
        self.frame_index = 0
        self.hurt_time_marker = 0
        self.total_death_frames = death_frames
        self.animation_speed = animation_speed

    def is_moving(self):
        return bool(self.entity.velocity[0]) or bool(self.entity.velocity[1])

    def determine_direction(self):
        if self.is_moving():
            if self.entity.velocity[0] > 0:
                self.direction = "right"
            elif self.entity.velocity[0] < 0:
                self.direction = "left"

    def increment_frame_index(self):
        self.frame_index += 0.1
        if self.frame_index >= 4:
            self.frame_index = 0

    def play_idle_animation(self, state):
        self.increment_frame_index()
        self.determine_direction()
        if self.direction == "right":
            self.entity.image = self.entity.animation_database[state][
                int(self.frame_index)
            ]
        else:
            self.entity.image = self.entity.animation_database[state][
                int(self.frame_index)
            ]
            self.entity.image = pygame.transform.flip(self.entity.image, True, False)

    def play_death_animation(self):
        self.frame_index += 1.0 / self.animation_speed
        if self.frame_index >= self.total_death_frames:
            self.entity.death_counter = 0
        if self.frame_index <= self.total_death_frames:
            state = "HURT" if self.frame_index < 1 else "DEAD"
            if self.entity.direction == "left":
                self.entity.image = self.entity.animation_database[state][
                    int(self.frame_index)
                ]
            else:
                self.entity.image = self.entity.animation_database[state][
                    int(self.frame_index)
                ]
                self.entity.image = pygame.transform.flip(
                    self.entity.image, True, False
                )

    def play_hurt_animation(self):
        self.frame_index = 0
        self.play_idle_animation("HURT")
        invincibility_time = 300
        if pygame.time.get_ticks() - self.hurt_time_marker > invincibility_time:
            self.hurt_time_marker = pygame.time.get_ticks()
            self.entity.hurt = False

    def run_animation(self):
        if self.entity.dead:
            self.play_death_animation()
        elif self.entity.hurt:
            self.play_hurt_animation()
        elif self.is_moving():
            self.play_idle_animation("WALK")
        else:
            self.play_idle_animation("IDLE")

    def update(self):
        self.run_animation()
