from src.map.room import Room
from src.map.map_layout import MapLayout


class Dungeon:
    def __init__(self, map_pattern_size):
        self.map_layout = MapLayout(map_pattern_size)
        self.map = [
            [None for _ in range(map_pattern_size)] for _ in range(map_pattern_size)
        ]

    def _check_neighbors(self, row_index, colomn_index, current_room):
        neighbor_directions = {
            "right": (0, 1),
            "left": (0, -1),
            "up": (-1, 0),
            "down": (1, 0),
        }
        for direction in neighbor_directions:
            neighbor_row = row_index + neighbor_directions[direction][0]
            neighbor_colomn = colomn_index + neighbor_directions[direction][1]

            if 0 <= neighbor_row < len(self.map) and 0 <= neighbor_colomn < len(
                self.map[0]
            ):
                neighbor = self.map[neighbor_row][neighbor_colomn]

                if neighbor:  # Добавляет переходы от текущей комнаты к соседней
                    current_room.passages[direction].from_room = current_room
                    current_room.passages[direction].to_room = neighbor

    def _generate_recursive(self, row_index, colomn_index):
        if (
            self.map[row_index][colomn_index]
            or not self.map_layout[row_index][colomn_index]
        ):
            return
        else:
            self.map[row_index][colomn_index] = Room()
            self._check_neighbors(
                row_index, colomn_index, self.map[row_index][colomn_index]
            )
            if row_index - 1 >= 0:
                self._generate_recursive(row_index - 1, colomn_index)
            if colomn_index - 1 >= 0:
                self._generate_recursive(row_index, colomn_index - 1)
            if row_index + 1 < len(self.map):
                self._generate_recursive(row_index + 1, colomn_index)
            if colomn_index + 1 < len(self.map[0]):
                self._generate_recursive(row_index, colomn_index - 1)

    def generate_map(self):
        self._generate_recursive(
            self.map_layout.start_position, self.map_layout.start_position
        )
