from src.map.room import Room
from src.map.map_layout import MapLayout


class Dungeon:
    def __init__(self, map_pattern_size, room_quantity):
        self.map_layout = MapLayout(map_pattern_size, room_quantity)
        self.map = [
            [None for _ in range(map_pattern_size)] for _ in range(map_pattern_size)
        ]
        self.start_position = self.map_layout.start_position
        self.generate_map()

    def _check_neighbors(self, row_index, column_index):
        neighbor_directions = {
            "right": (0, 1),
            "left": (0, -1),
            "up": (-1, 0),
            "down": (1, 0),
        }
        for direction, (d_row, d_col) in neighbor_directions.items():
            neighbor_row = row_index + d_row
            neighbor_column = column_index + d_col

            if 0 <= neighbor_row < len(self.map) and 0 <= neighbor_column < len(
                self.map[0]
            ):
                neighbor = self.map[neighbor_row][neighbor_column]

                if neighbor:
                    self.map[row_index][column_index].create_passage(
                        neighbor, direction
                    )

                    opposite_directions = {
                        "right": "left",
                        "left": "right",
                        "up": "down",
                        "down": "up",
                    }
                    neighbor.create_passage(
                        self.map[row_index][column_index],
                        opposite_directions[direction],
                    )

    def _generate_recursive(self, row_index, column_index):
        if (
            self.map[row_index][column_index]
            or not self.map_layout.layout[row_index][column_index]
        ):
            return
        self.map[row_index][column_index] = Room()
        self._check_neighbors(row_index, column_index)
        if row_index - 1 >= 0:
            self._generate_recursive(row_index - 1, column_index)
        if column_index - 1 >= 0:
            self._generate_recursive(row_index, column_index - 1)
        if row_index + 1 < len(self.map):
            self._generate_recursive(row_index + 1, column_index)
        if column_index + 1 < len(self.map[0]):
            self._generate_recursive(row_index, column_index + 1)

    def generate_map(self):
        self._generate_recursive(self.start_position, self.start_position)
