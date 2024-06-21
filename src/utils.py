import pygame
from pygame.sprite import Group


floor_size = (936, 500)
basic_entity_size = (64, 64)
world_size = (1280, 800)
rooms_quantity = 10
map_size = 9


def check_time_passed(time, threshold_time):
    if pygame.time.get_ticks() - time > threshold_time:
        time = pygame.time.get_ticks()
        return True


def get_mask_rect(surface, topleft=(0, 0)):
    surface_mask = pygame.mask.from_surface(surface)
    rect_list = surface_mask.get_bounding_rects()
    if rect_list:
        surface_mask_rect = rect_list[0].unionall(rect_list)
        surface_mask_rect.move_ip(topleft)
        return surface_mask_rect


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
