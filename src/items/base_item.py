import pygame
from src.utils import get_mask_rect

class BaseItem():
    def __init__(self, game, room, name, object_type, size, player, position, damage, protection):
        self.game = game
        self.room = room
        self.name = name
        self.object_type = object_type
        self.size = size
        self.player = player
        #fix it
        self.image = None
        self.path = f'./assets/objects/{self.name}'
        self.load_image()
        self.rect = self.image.get_rect()
        self.hitbox = get_mask_rect(self.image, *self.rect.topleft)
        #^^^^^^
        if position:
            self.rect.x, self.rect.y = position[0], position[1]
        self.damage = damage
        self.protection = protection
        self.interaction = False
        self.dropped = False
        pass
    
    def use(self):
        pass
    