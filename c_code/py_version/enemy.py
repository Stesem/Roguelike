import pygame

pygame.init()

SCALE = 1
NUMBER_OF_IMAGES = 5
ANIMATION_COOLDOWN = 100

# https://www.youtube.com/watch?v=PIS-L8_BojU --- base
# https://www.youtube.com/watch?v=hZGtgv6Hh40 --- animation
class Enemy:
    def __init__(self, name, coordinate_x, coordinate_y, max_hp, strength): # "name" probably not needed
        self.name = name

        self.max_hp = max_hp
        self.hp = max_hp

        self.strength = strength
        self.alive = True

        self.animation_list = []
        self.frame_index = 0
        self.action = 0 # 0:idle, 1:attack, 2:hurt, 3:dead
        self.update_animation_time = pygame.time.get_ticks()
        temporary_list = []
        for i in range(NUMBER_OF_IMAGES):
            image_start = pygame.image.load('image/{self.name}/Idle/{i}.png')
            image_start = pygame.transform.scale(image_start, (image_start.get_width() * SCALE, image_start.get_height() * SCALE))
            temporary_list.append(image_start)
        self.animation_list.append(temporary_list)
        self.image = self.animation_list[self.action][self.frame_index]
        self.rectangle = self.image.get_rect()
        self.rectangle.center = (coordinate_x, coordinate_y)
    
    def update_animation(self):
        self.image = self.animation_list[self.action][self.frame_index]
        #check if enough time has passed since the last update
        if (pygame.time.get_ticks() - self.update_animation_time > ANIMATION_COOLDOWN):
            self.update_animation_time = pygame.time.get_ticks()
            self.frame_index += 1
        #if the animation has run out then reset back to the start
        if self.frame_index >= len(self.animation_list[self.action]):
            self.frame_index = 0
        
    def draw(self):
        screen.blit(self.image, self.rectangle)

SimpleEnemy = Enemy('npc', x, y, se_hp, se_strength) # example arguments
