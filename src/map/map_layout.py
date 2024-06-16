from random import shuffle, randint


class MapLayout:
    def __init__(self, size):
        self.size = size
        self.layout = [[False for _ in range(self.size)] for _ in range(self.size)]
        self.start_position = self.size // 2
        self.elem_count = 0

    def __fill_layout_recursive(self, position_j, position_i, elem_quantity):
        if (self.elem_count == elem_quantity) or self.layout[position_j][position_i]:
            return
        if (position_j > (self.size - 1)) or (position_j < 0):
            return
        if (position_i > (self.size - 1)) or (position_i < 0):
            return
        self.elem_count += 1
        self.layout[position_j][position_i] = True
        offsets = {"right": (0, 1), "left": (0, -1), "up": (-1, 0), "down": (1, 0)}
        free_places = []

        if (
            position_j + offsets["right"][0] < self.size
            and position_i + offsets["right"][1] < self.size
            and not self.layout[position_j + offsets["right"][0]][
                position_i + offsets["right"][1]
            ]
        ):
            free_places.append("right")

        if (
            position_j + offsets["left"][0] >= 0
            and position_i + offsets["left"][1] >= 0
            and not self.layout[position_j + offsets["left"][0]][
                position_i + offsets["left"][1]
            ]
        ):
            free_places.append("left")

        if (
            position_j + offsets["up"][0] >= 0
            and position_i + offsets["up"][1] >= 0
            and not self.layout[position_j + offsets["up"][0]][
                position_i + offsets["up"][1]
            ]
        ):
            free_places.append("up")

        if (
            position_j + offsets["down"][0] < self.size
            and position_i + offsets["down"][1] < self.size
            and not self.layout[position_j + offsets["down"][0]][
                position_i + offsets["down"][1]
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
                position_j + offsets[free_places[0]][0],
                position_i + offsets[free_places[0]][1],
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
