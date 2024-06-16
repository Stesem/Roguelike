from src.map.map_layout import MapLayout


def test_map_layout_create():
    size = 11
    map_layout = MapLayout(size)
    layout_for_assert = [[False for _ in range(size)] for _ in range(size)]
    assert (
        map_layout.layout == layout_for_assert
    ), f"Error in creating Fallse table, result {map_layout.show()}"


def test_map_layout_show():
    size = 2
    map_layout = MapLayout(size)
    table_for_assert = "[False, False]\n[False, False]"
    assert (
        map_layout.show() == table_for_assert
    ), f"Error in showing method, result {map_layout.show()}"


def test_map_layout_fill():
    size = 5
    elem_cuant = 10
    map_layout = MapLayout(size)
    map_layout.fill_layout(elem_cuant)
    layout_all_false = [[False for _ in range(size)] for _ in range(size)]
    assert (map_layout.layout != layout_all_false) and (
        map_layout.elem_count >= elem_cuant
    ), f"Error in filling layout, result {map_layout.show()}"
