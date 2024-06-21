import pygame
from pygame.sprite import Group
import json


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
    def __init__(self, passage_info):
        self.passage_info = passage_info
        image = pygame.image.load(self.passage_info["image"]).convert_alpha()
        image = pygame.transform.scale(
            image, (self.passage_info["width"], self.passage_info["height"])
        )
        self.sprite = create_sprite(image, passage_info)
        self.from_room = None
        self.to_room = None


class Room:
    def __init__(self):
        self.passages_on_direction = {
            "right": None,
            "left": None,
            "up": None,
            "down": None,
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

    def create_passage(self, next_room, direction):
        passage_info = next(
            info for info in self.passages_info if info["direction"] == direction
        )
        pas = Passage(passage_info)
        self.passages_on_direction[direction] = pas
        self.passages_on_direction[direction].from_room = self
        self.passages_on_direction[direction].to_room = next_room
        self.passages.add(pas.sprite)

    def draw_room(self, screen):
        self.floor.draw(screen)
        self.walls.draw(screen)
        self.passages.draw(screen)


"""         for passage in self.passages:
            print(passage.rect.topleft) """
