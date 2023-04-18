from lib.core.game_manager import Map, Province, ProvinceType, Unit

import pytest


game_map = Map()

pr1 = Province("PR1", ProvinceType.water.value, False)
pr2 = Province("PR2", ProvinceType.coast.value, False)
pr3 = Province("PR3", ProvinceType.land.value,  False)
pr4 = Province("PR4", ProvinceType.coast.value, False)
pr5 = Province("PR5", ProvinceType.water.value, False)

u1 = Unit(pr1)
u2 = Unit(pr2)
u3 = Unit(pr3)
u4 = Unit(pr4)


def setup_function():
    global game_map, pr1, pr2, pr3, pr4, pr5
    game_map = Map()

def teardown_function():
    global game_map
    game_map = Map()

def setup_provinces_in_mup():
    game_map.add_province(pr1, [])
    game_map.add_province(pr2, [])
    game_map.add_province(pr3, [])
    game_map.add_province(pr4, [])
    game_map.add_province(pr5, [])


def test_add_province_result():
    #   
    #                       coast
    #   PR1 ---------------- PR2 -_
    #  water                  |     -_
    #                         |        -_
    #                         |           -_
    #                        PR3 -------- PR4 ------- PR5
    #                       land         coast       water
    #
    
    game_map.add_province(pr1, [])
    assert game_map.provinces_graph == {pr1: set()}

    game_map.add_province(pr3, [pr2])
    assert game_map.provinces_graph == {pr1: set(), 
                                        pr3: set([pr2]),
                                        pr2: set([pr3])}

    game_map.add_province(pr2, [pr1, pr4])
    assert game_map.provinces_graph == {pr1: set([pr2]), 
                                        pr3: set([pr2]),
                                        pr2: set([pr1,pr3, pr4]),
                                        pr4: set([pr2])}
    
    game_map.add_province(pr4, [pr2, pr3, pr5])
    assert game_map.provinces_graph == {pr1: set([pr2]), 
                                        pr3: set([pr2, pr4]),
                                        pr2: set([pr1,pr3, pr4]),
                                        pr4: set([pr2, pr3, pr5]),
                                        pr5: set([pr4])}

    game_map.add_province(pr5, [pr4])
    assert game_map.provinces_graph == {pr1: set([pr2]), 
                                        pr3: set([pr2, pr4]),
                                        pr2: set([pr1,pr3, pr4]),
                                        pr4: set([pr2, pr3, pr5]),
                                        pr5: set([pr4])}

@pytest.mark.parametrize(("new_province", "neighboring_provinces"), ( ["123", 123],
                                                                      ["123", [1, 2, 3]],
                                                                      ["123", [pr1, 2, pr2]] ))
def test_add_province_with_type_error(new_province, neighboring_provinces):
    game_map.add_province(pr1, [pr2])

    with pytest.raises(TypeError):
        game_map.add_province(new_province, neighboring_provinces)

@pytest.mark.parametrize(("new_province", "neighboring_provinces"), ( [pr5, [pr3]],
                                                                      [pr3, [pr1]] ))
def test_add_province_type_neighboring_with_value_error(new_province, neighboring_provinces):
    game_map.add_province(pr1, [pr2])

    with pytest.raises(ValueError):
        game_map.add_province(new_province, neighboring_provinces)


def test_add_transition_result():
    setup_provinces_in_mup()

    game_map.add_transition(pr1, pr2)
    assert game_map.provinces_graph == {pr1: set([pr2]),
                                        pr2: set([pr1]),
                                        pr3: set(),
                                        pr4: set(),
                                        pr5: set()}

    game_map.add_transition(pr2, pr4)
    assert game_map.provinces_graph == {pr1: set([pr2]),
                                        pr2: set([pr1, pr4]),
                                        pr3: set(),
                                        pr4: set([pr2]),
                                        pr5: set()}

    game_map.add_transition(pr3, pr4)
    assert game_map.provinces_graph == {pr1: set([pr2]),
                                        pr2: set([pr1, pr4]),
                                        pr3: set([pr4]),
                                        pr4: set([pr2, pr3]),
                                        pr5: set()}

    game_map.add_transition(pr4, pr3)
    assert game_map.provinces_graph == {pr1: set([pr2]),
                                        pr2: set([pr1, pr4]),
                                        pr3: set([pr4]),
                                        pr4: set([pr2, pr3]),
                                        pr5: set()}

@pytest.mark.parametrize(("first_province", "second_province"), ( ["123", 123],
                                                                  ["123", [1, 2, 3]],
                                                                  ["123", [pr1, 2, pr2]]))
def test_add_transition_type_neighboring_with_type_error(first_province, second_province):
    setup_provinces_in_mup()

    game_map.add_transition(pr1, pr2)
    
    with pytest.raises(TypeError):
        game_map.add_transition(first_province, second_province)

@pytest.mark.parametrize(("first_province", "second_province"), ( [pr1, pr3],
                                                                  [pr5, pr3] ))
def test_add_transition_type_neighboring_with_value_error(first_province, second_province):
    setup_provinces_in_mup()

    game_map.add_transition(pr1, pr2)
    
    with pytest.raises(ValueError):
        game_map.add_transition(first_province, second_province)


@pytest.mark.parametrize(("unit", "result"), ([u1, set([u1])],
                                              [u1, set([u1])]))
def test_add_unit_result(unit, result):
    game_map.add_unit(unit)
    assert game_map.units == result

@pytest.mark.parametrize("unit", ( [ 123 ],
                                   [[123]],
                                   ["123"]))
def test_add_unit_type_error(unit):
    game_map.add_unit(u1)
    
    with pytest.raises(TypeError):
        game_map.add_unit(unit)
