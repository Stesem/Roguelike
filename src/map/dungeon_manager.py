from src.map.dungeon import Dungeon
from src.suppor import rooms_quantity, map_size, basic_entity_size, floor_size


class DungeonManager:
    def __init__(self, game):
        self.game = game
        self.dungeon = None
        self.position_x, self.position_y = None, None
        self.current_room = None
        self.next_room = None
        self.switch_room = None
        self.create_dungeon_manager()

    def create_dungeon_manager(self):
        self.dungeon = Dungeon(map_size, rooms_quantity)
        self.position_x = self.dungeon.start_position
        self.position_y = self.dungeon.start_position
        self.current_room = self.dungeon.map[self.position_y][self.position_x]

    def set_current_room(self, room):
        self.current_room = room

    def go_to_next_room(self, passage):
        current_room = self.current_room
        for direction in current_room.passages_on_direction:

            if (
                current_room.passages_on_direction[direction]
                and current_room.passages_on_direction[direction].sprite == passage
            ):
                next_room = current_room.passages_on_direction[direction].to_room
                self.set_current_room(next_room)
                self.move_player_in_new_room(direction)

    def move_player_in_new_room(self, direction_in_prev_room):
        if direction_in_prev_room == "right":
            self.game.player.rect.move_ip(
                -(floor_size[0] - basic_entity_size[0] // 4), 0
            )
            self.game.player.hitbox.move_ip(
                -(floor_size[0] - basic_entity_size[0] // 4), 0
            )
        if direction_in_prev_room == "left":
            self.game.player.rect.move_ip(
                (floor_size[0] - basic_entity_size[0] // 4), 0
            )
            self.game.player.hitbox.move_ip(
                (floor_size[0] - basic_entity_size[0] // 4), 0
            )
        if direction_in_prev_room == "up":
            self.game.player.rect.move_ip(
                0, (floor_size[1] - basic_entity_size[1] // 4)
            )
            self.game.player.hitbox.move_ip(
                0, (floor_size[1] - basic_entity_size[1] // 4)
            )
        if direction_in_prev_room == "down":
            self.game.player.rect.move_ip(
                0, -(floor_size[1] - basic_entity_size[1] // 4)
            )
            self.game.player.hitbox.move_ip(
                0, -(floor_size[1] - basic_entity_size[1] // 4)
            )

    def update_dungeon(self):
        self.current_room.update_room()

    def draw_dungeon(self, screen):
        self.current_room.draw_room(screen)
