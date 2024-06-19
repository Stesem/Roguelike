from random import shuffle, randint


class MapLayout:
    def __init__(self, size):
        self.size = size
        self.layout = [[False for _ in range(self.size)] for _ in range(self.size)]
        self.start_position = self.size // 2
        self.elem_count = 0

    def __fill_layout_recursive(self, row_index, column_index, elem_quantity):
        if (self.elem_count == elem_quantity) or self.layout[row_index][column_index]:
            return
        if (row_index > (self.size - 1)) or (row_index < 0):
            return
        if (column_index > (self.size - 1)) or (column_index < 0):
            return
        self.elem_count += 1
        self.layout[row_index][column_index] = True
        offsets = {"right": (0, 1), "left": (0, -1), "up": (-1, 0), "down": (1, 0)}
        free_places = []

        if (
            row_index + offsets["right"][0] < self.size
            and column_index + offsets["right"][1] < self.size
            and not self.layout[row_index + offsets["right"][0]][
                column_index + offsets["right"][1]
            ]
        ):
            free_places.append("right")

        if (
            row_index + offsets["left"][0] >= 0
            and column_index + offsets["left"][1] >= 0
            and not self.layout[row_index + offsets["left"][0]][
                column_index + offsets["left"][1]
            ]
        ):
            free_places.append("left")

        if (
            row_index + offsets["up"][0] >= 0
            and column_index + offsets["up"][1] >= 0
            and not self.layout[row_index + offsets["up"][0]][
                column_index + offsets["up"][1]
            ]
        ):
            free_places.append("up")

        if (
            row_index + offsets["down"][0] < self.size
            and column_index + offsets["down"][1] < self.size
            and not self.layout[row_index + offsets["down"][0]][
                column_index + offsets["down"][1]
            ]
        ):
            free_places.append("down")

        if free_places:
            quantity_free_places = randint(1, len(free_places))
        else:
            quantity_free_places = 0

        while quantity_free_places > 0 and free_places:
            shuffle(free_places)
            self.__fill_layout_recursive(
                row_index + offsets[free_places[0]][0],
                column_index + offsets[free_places[0]][1],
                elem_quantity,
            )
            del free_places[0]
            quantity_free_places -= 1

    def fill_layout(self, elem_quantity):
        self.elem_count = 0  # Сброс счетчика перед заполнением
        self.layout = [
            [False for _ in range(self.size)] for _ in range(self.size)
        ]  # Очистка перед заполнением
        self.__fill_layout_recursive(
            self.start_position, self.start_position, elem_quantity
        )

    def show(self):
        table = []
        for k in range(self.size):
            table.append(f"{self.layout[k]}")
        return "\n".join(table)
