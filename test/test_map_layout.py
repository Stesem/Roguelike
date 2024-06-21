from src.map.map_layout import MapLayout


def test_map_layout_fill():
    size = 5
    elem_cuant = 10
    map_layout = MapLayout(size, elem_cuant)
    map_layout.fill_layout(elem_cuant)
    layout_all_false = [[False for _ in range(size)] for _ in range(size)]
    assert (map_layout.layout != layout_all_false) and (
        map_layout.elem_count >= elem_cuant
    ), f"Error in filling layout, result {map_layout.show()}"
