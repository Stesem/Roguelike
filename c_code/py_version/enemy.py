# the reference https://github.com/russs123/Battle/tree/main

import pygame
import random

pygame.init()

clock = pygame.time.Clock()
fps = 60

ACTION_INDEX = 0 # 0:idle, 1:attack, 2:hurt, 3:dead
SCALE = 1
NUMBER_OF_IMAGES = 5
ANIMATION_COOLDOWN = 100
MIN_DAMAGE = -5
MAX_DAMAGE = 5
CURRENT_WEAPON = 0 # i guess it should be class weapon

# for ai
current_fighter = 1
total_fighters = 3
action_cooldown = 0
action_wait_time = 90
attack = False
potion = False
clicked = False


# https://www.youtube.com/watch?v=PIS-L8_BojU --- base
# https://www.youtube.com/watch?v=hZGtgv6Hh40 --- animation
# https://www.youtube.com/watch?v=M4LjMbhkcfs --- health bar (not done)
# https://www.youtube.com/watch?v=hLRJVv7K8C8 --- attacking + ai (it's probably not an ai actually)
class Enemy:
    def __init__(self, name, coordinate_x, coordinate_y, max_hp, strength, weapon): # "name" probably not needed
        self.name = name

        self.max_hp = max_hp
        self.hp = max_hp

        self.strength = strength
        self.alive = True

        self.animation_list = []
        self.frame_index = 0
        self.action = ACTION_INDEX
        self.update_animation_time = pygame.time.get_ticks()
        # looping any kind of animation packs (idk if the project even needs it)
        # idle animation
        temporary_list = []
        for i in range(NUMBER_OF_IMAGES):
            image_start = pygame.image.load('image/{self.name}/Idle/{i}.png')
            image_start = pygame.transform.scale(image_start, (image_start.get_width() * SCALE, image_start.get_height() * SCALE))
            temporary_list.append(image_start)
        self.animation_list.append(temporary_list)
        # attack animation
        temporary_list = []
        for i in range(NUMBER_OF_IMAGES):
            image_start = pygame.image.load('image/{self.name}/Attack/{i}.png')
            image_start = pygame.transform.scale(image_start, (image_start.get_width() * SCALE, image_start.get_height() * SCALE))
            temporary_list.append(image_start)
        self.animation_list.append(temporary_list)

        self.weapon = CURRENT_WEAPON
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
    
    def attack(self, target, weapon):
        # deal damage to enemy
        random_buff_damage = random.randint(MIN_DAMAGE, MAX_DAMAGE)
		# should i change it to weapon_damage = self.weapon.damage ?
        damage = self.strength + random_buff_damage
        target.hp -= damage
		#check if target has died
        if target.hp < 1:
            target.hp = 0
            target.alive = False
		#set variables to attack animation
        self.action = 1
        self.frame_index = 0
        self.update_animation_time = pygame.time.get_ticks()
        

    def draw(self):
        screen.blit(self.image, self.rectangle)

SimpleEnemy = Enemy('npc', x, y, se_hp, se_strength) # example arguments

# def DrawText(text, font, test_col, coordinate_x, coordinate_y):


# did not analyse it
class HealthBar():
	def __init__(self, x, y, hp, max_hp):
		self.x = x
		self.y = y
		self.hp = hp
		self.max_hp = max_hp


	def draw(self, hp):
		#update with new health
		self.hp = hp
		#calculate health ratio
		ratio = self.hp / self.max_hp
		pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
		pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))


#example

knight = Fighter(200, 260, 'Knight', 30, 10, 3)
bandit1 = Fighter(550, 270, 'Bandit', 20, 6, 1)
bandit2 = Fighter(700, 270, 'Bandit', 20, 6, 1)

bandit_list = []
bandit_list.append(bandit1)
bandit_list.append(bandit2)

knight_health_bar = HealthBar(100, screen_height - bottom_panel + 40, knight.hp, knight.max_hp)
bandit1_health_bar = HealthBar(550, screen_height - bottom_panel + 40, bandit1.hp, bandit1.max_hp)
bandit2_health_bar = HealthBar(550, screen_height - bottom_panel + 100, bandit2.hp, bandit2.max_hp)

run = True
while run:

	clock.tick(fps)

	#draw background
	draw_bg()

	#draw panel
	draw_panel()
	knight_health_bar.draw(knight.hp)
	bandit1_health_bar.draw(bandit1.hp)
	bandit2_health_bar.draw(bandit2.hp)

	#draw fighters
	knight.update()
	knight.draw()
	for bandit in bandit_list:
		bandit.update()
		bandit.draw()


	#control player actions
	#reset action variables
	attack = False
	potion = False
	target = None
	#make sure mouse is visible
	pygame.mouse.set_visible(True)
	pos = pygame.mouse.get_pos()
	for count, bandit in enumerate(bandit_list):
		if bandit.rect.collidepoint(pos):
			#hide mouse
			pygame.mouse.set_visible(False)
			#show sword in place of mouse cursor
			screen.blit(sword_img, pos)
			if clicked == True:
				attack = True
				target = bandit_list[count]


	#player action
	if knight.alive == True:
		if current_fighter == 1:
			action_cooldown += 1
			if action_cooldown >= action_wait_time:
				#look for player action
				#attack
				if attack == True and target != None:
					knight.attack(target)
					current_fighter += 1
					action_cooldown = 0


	#enemy action
	for count, bandit in enumerate(bandit_list):
		if current_fighter == 2 + count:
			if bandit.alive == True:
				action_cooldown += 1
				if action_cooldown >= action_wait_time:
					#attack
					bandit.attack(knight)
					current_fighter += 1
					action_cooldown = 0
			else:
				current_fighter += 1

	#if all fighters have had a turn then reset
	if current_fighter > total_fighters:
		current_fighter = 1


	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			run = False
		if event.type == pygame.MOUSEBUTTONDOWN:
			clicked = True
		else:
			clicked = False

	pygame.display.update()

pygame.quit()
