import random

class Passage:
    def __init__(self, pattern=None, from_room=None, to_room=None):
        self.pattern = pattern if pattern is not None else self.random_pattern()
        self.from_room = from_room
        self.to_room = to_room

    @staticmethod
    def random_pattern():
        return random.randint(0, 100)  # Generate random pattern


class SqRoom:
    def __init__(self):
        self.pattern = Passage.random_pattern()
        self.passages = {
            'r': Passage(),
            'l': Passage(),
            'u': Passage(),
            'd': Passage()
        }


def check_neighbors(graph, index_j, index_i, current_room):
    directions = ['r', 'l', 'u', 'd']
    neighbors_coords = [(0, 1), (0, -1), (-1, 0), (1, 0)]

    for direction, (dj, di) in zip(directions, neighbors_coords):
        neighbor_j = index_j + dj
        neighbor_i = index_i + di

        if 0 <= neighbor_j < len(graph) and 0 <= neighbor_i < len(graph[0]):
            neighbor = graph[neighbor_j][neighbor_i]

            if neighbor:
                current_room.passages[direction].from_room = current_room
                current_room.passages[direction].to_room = neighbor


def create_map(existing_table, graph, index_i, index_j):
    if graph[index_j][index_i]:
        return
    elif not graph[index_j][index_i] and existing_table[index_j][index_i]:
        graph[index_j][index_i] = SqRoom()
        check_neighbors(graph, index_j, index_i, graph[index_j][index_i])

        if index_i + 1 < len(graph[0]):
            create_map(existing_table, graph, index_i + 1, index_j)  # Right
        if index_i - 1 >= 0:
            create_map(existing_table, graph, index_i - 1, index_j)  # Left
        if index_j - 1 >= 0:
            create_map(existing_table, graph, index_i, index_j - 1)  # Up
        if index_j + 1 < len(graph):
            create_map(existing_table, graph, index_i, index_j + 1)  # Down


# Example usage
if __name__ == "__main__":
    size = 4
    existing_table = [[False for _ in range(size)] for _ in range(size)]
    graph = [[None for _ in range(size)] for _ in range(size)]

    # Simulate existing table with some rooms
    existing_table[1][1] = True
    existing_table[1][2] = True
    existing_table[2][2] = True

    create_map(existing_table, graph, 1, 1)
    
    # Display the generated map (for testing purposes)
    for row in graph:
        for room in row:
            if room:
                print("Room", room.pattern, "Passages", {k: v.to_room.pattern if v.to_room else None for k, v in room.passages.items()})
            else:
                print("None", end=" ")
        print()
