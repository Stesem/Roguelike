import pygame
from pygame.sprite import Group
import json
from src.suppor import world_size, create_sprite, create_sprites_group


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
        self.tipe = None
        self.enemy_list = []
        self.items_list = []

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

    def centering_room(self):
        screen_cecter = (world_size[0] / 2, world_size[1] / 2)
        room_offset = (
            screen_cecter[0] - self.width / 2,
            screen_cecter[1] - self.height / 2,
        )
        for floor in self.floor.sprites():
            if floor.rect.topleft == (32, 32):
                floor.rect.move_ip(room_offset)
                for wall in self.walls.sprites():
                    wall.rect.move_ip(room_offset)
                for passage in self.passages.sprites():
                    passage.rect.move_ip(room_offset)

    def update_room(self):
        self.centering_room()
        self.floor.update()
        self.walls.update()
        self.passages.update()

    def draw_room(self, screen):
        self.floor.draw(screen)
        self.walls.draw(screen)
        self.passages.draw(screen)
