import pygame
from pygame.sprite import Group
import json
import random


class Room:
    def __init__(self, config_file):
        self.load_from_json(config_file)

    def load_from_json(self, config_file):
        with open(config_file, "r") as file:
            config = json.load(file)

        self.width = config["width"]
        self.height = config["height"]
        self.walls = self.create_sprites_group(config["walls"])
        self.floor = self.create_sprites_group(config["floor"])

        # Load passages
        self.passages = {}
        self.passages_open = config["passages_open"]
        for direction, passage_info in config["passages"].items():
            closed_image = pygame.image.load(
                passage_info["closed_image"]
            ).convert_alpha()
            open_image = pygame.image.load(passage_info["open_image"]).convert_alpha()
            self.passages[direction] = {
                "closed": self.create_sprite(closed_image, passage_info),
                "open": self.create_sprite(open_image, passage_info),
            }

    def create_sprite(self, image, sprite_info):
        sprite = pygame.sprite.Sprite()
        sprite.image = image
        sprite.rect = pygame.Rect(
            sprite_info["x"],
            sprite_info["y"],
            sprite_info["width"],
            sprite_info["height"],
        )
        return sprite

    def create_sprites_group(self, sprites_info):
        group = Group()
        for sprite_info in sprites_info:
            image = pygame.image.load(sprite_info["image"]).convert_alpha()
            sprite = pygame.sprite.Sprite()
            sprite.image = image
            sprite.rect = pygame.Rect(
                sprite_info["x"],
                sprite_info["y"],
                sprite_info["width"],
                sprite_info["height"],
            )
            group.add(sprite)
        return group

    def toggle_passage(self, direction):
        self.passages_open[direction] = not self.passages_open[direction]

    def get_passage_state(self, direction):
        return self.passages_open[direction]

    def draw(self, screen):
        self.floor.draw(screen)
        self.walls.draw(screen)
        for direction, state in self.passages_open.items():
            if state:
                screen.blit(
                    self.passages[direction]["open"].image,
                    self.passages[direction]["open"].rect,
                )
            else:
                screen.blit(
                    self.passages[direction]["closed"].image,
                    self.passages[direction]["closed"].rect,
                )
