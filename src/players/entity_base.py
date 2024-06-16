import pygame


class EntityBase():
    
    def __init__(self, game, name):
        self.game = game
        self.name = name
        self.path = f'assets/characters/{self.name}'
        self.image = self.image = pygame.image.load(f'assets/characters/{name}/{name}0.png')
        self.rect = self.image.get_rect()
        self.velocity = [0, 0]
        self.direction = 'right'
        self.can_move = True
        self.time = 0
        self.can_get_hurt = True
        
    def set_velocity(self, new_velocity):
        self.velocity = new_velocity
        
        
    def basic_update(self):
        self.rect.move_ip(self.velocity)
        
    def moving(self):
        return self.velocity[0] != 0 or self.velocity[1] != 0

        
        