import pygame
from pygame.sprite import Group
import json
from src.utils import get_mask_rect


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
        image = pygame.transform.scale(
            image, (sprite_info["width"], sprite_info["height"])
        )
        sprite = create_sprite(image, sprite_info)
        group.add(sprite)
    return group


class Passage:
    def __init__(self, from_room=None, to_room=None, passage_info=None):
        self.passage_info = passage_info
        if passage_info:
            image = pygame.image.load(self.passage_info["image"]).convert_alpha()
            self.sprite = create_sprite(image, passage_info)
        else:
            self.sprite = None
        self.from_room = from_room
        self.to_room = to_room


class Room:
    def __init__(self):
        self.passages_on_direction = {
            "right": Passage(),
            "left": Passage(),
            "up": Passage(),
            "down": Passage(),
        }
        self.load_from_json()
        self.passages = Group()

    def load_from_json(self):
        with open("src/map/room_pattern.json", "r") as file:
            config = json.load(file)

        self.width = config["width"]
        self.height = config["height"]
        self.walls = create_sprites_group(config["walls"])
        self.floor = create_sprites_group(config["floor"])
        self.passages_info = config["passages"]

    def create_passages(self, next_room, direction):
        passage_info = next(
            info for info in self.passages_info if info["direction"] == direction
        )
        self.passages_on_direction[direction].passage_info = passage_info
        if self.passages_on_direction[direction].sprite:
            self.passages_on_direction[direction].from_room = self
            self.passages_on_direction[direction].to_room = next_room
            self.passages.add(self.passages_on_direction[direction].sprite)

    def draw_room(self, screen):
        self.floor.draw(screen)
        self.walls.draw(screen)
        self.passages.draw(screen)
