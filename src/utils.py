import pygame


floor_size = (936, 500)
basic_entity_size = (64, 64)
world_size = (1280, 800)
rooms_quantity = 10
map_size = 9


def get_mask_rect(surface, topleft=(0, 0)):
    surface_mask = pygame.mask.from_surface(surface)
    rect_list = surface_mask.get_bounding_rects()
    if rect_list:
        surface_mask_rect = rect_list[0].unionall(rect_list)
        surface_mask_rect.move_ip(topleft)
        return surface_mask_rect
