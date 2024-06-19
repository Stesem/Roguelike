import pygame
from pygame.sprite import Group
import json
import random


# Вспомогательные функции
def create_sprite(image, sprite_info):
    sprite = pygame.sprite.Sprite()
    sprite.image = image
    sprite.rect = pygame.Rect(
        sprite_info["x"],
        sprite_info["y"],
        sprite_info["width"],
        sprite_info["height"],
    )
    return sprite


def create_sprites_group(sprites_info):
    group = Group()
    for sprite_info in sprites_info:
        image = pygame.image.load(sprite_info["image"]).convert_alpha()
        sprite = create_sprite(image, sprite_info)
        group.add(sprite)
    return group


class Passage:
    def __init__(self, from_room, to_room, image):
        self.image = image
        self.from_room = from_room
        self.to_room = to_room


class Room:
    def __init__(self):
        self.passages = {
            "right": Passage(),
            "left": Passage(),
            "up": Passage(),
            "down": Passage(),
        }
        self.load_from_json()

    def load_from_json(self):
        with open("src/map/room_pattern.json", "r") as file:
            config = json.load(file)

        self.width = config["width"]
        self.height = config["height"]
        self.walls = create_sprites_group(config["walls"])
        self.floor = create_sprites_group(config["floor"])

    def draw_room(self, screen):
        self.floor.draw(screen)
        self.walls.draw(screen)
