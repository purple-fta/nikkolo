from lib.core.game_manager import GameManager, Move, SupportHold, SupportMove, \
                                  Province, ProvinceType, Unit, ConvoyMove, \
                                  UnitType

import pytest


pr1 = Province("PR1", ProvinceType.water.value, True)
pr2 = Province("PR2", ProvinceType.coast.value, True)
pr3 = Province("PR3", ProvinceType.land.value,  True)
pr4 = Province("PR4", ProvinceType.coast.value, True)
pr5 = Province("PR5", ProvinceType.water.value, True)

u1 = Unit(pr1)
u2 = Unit(pr2)
u3 = Unit(pr3)
u4 = Unit(pr4)

game_manager = GameManager()


def setup_function():
    global game_manager, pr1, pr2, pr3, pr4, pr5, u1, u2, u3, u4, u5
    game_manager = GameManager()

    pr1 = Province("PR1", ProvinceType.water.value, True)
    pr2 = Province("PR2", ProvinceType.coast.value, True)
    pr3 = Province("PR3", ProvinceType.land.value,  True)
    pr4 = Province("PR4", ProvinceType.coast.value, True)
    pr5 = Province("PR5", ProvinceType.water.value, True)
    
    u1 = Unit(pr1)
    u2 = Unit(pr2)
    u3 = Unit(pr3)
    u4 = Unit(pr4)

    game_manager.add_province(pr1, [pr2])
    game_manager.add_province(pr2, [pr1, pr3, pr4])
    game_manager.add_province(pr3, [pr2, pr4])
    game_manager.add_province(pr4, [pr3, pr2, pr5])
    game_manager.add_province(pr5, [pr4])

def teardown_function():
    global game_manager
    game_manager = GameManager()


def test_add_move_result():
    move1 = Move(u1, pr2)
    game_manager.add_move(move1)
    assert game_manager.moves == set([move1])

    move2 = SupportMove(u3, pr2, move1)
    game_manager.add_move(move2)
    assert game_manager.moves == set([move1, move2])

    move3 = SupportHold(u4, pr2, u2)
    game_manager.add_move(move3)
    assert game_manager.moves == set([move1, move2, move3])


def test_add_move_with_type_error():
    move = Move(u1, pr2)
    game_manager.add_move(move)
    game_manager.add_move(SupportMove(u2, pr2, move))

    with pytest.raises(TypeError):
        game_manager.add_move(123)
        game_manager.add_move("!@#")
        game_manager.add_move([123, 123, 234])


def test_applying_moves_first_example():
    move = Move(u1, pr2)
    
    game_manager.add_move(move)
    game_manager.applying_moves()

    assert game_manager.moves==set()
    assert move.unit.location == pr2


def test_applying_moves_second_example_without_destroy_unit():
    game_manager.add_unit(u1)
    game_manager.add_unit(u2)
    game_manager.add_unit(u3)

    move = Move(u1, pr2)
    support_move = SupportMove(u3, pr2, move)

    game_manager.add_move(move)
    game_manager.add_move(support_move)
    
    #assert pr1.protection == u1.protection
    #assert pr2.protection == u2.protection
    #assert pr3.protection == u3.protection

    game_manager.applying_moves()

    assert u1.location == pr2
    assert u2.location == pr4
    assert u3.location == pr3

    #assert pr1.protection == 0
    #assert pr2.protection == u1.protection
    #assert pr3.protection == u3.protection
    #assert pr4.protection == u2.protection

def test_applying_moves_second_example_with_destroy_unit():
    game_manager.add_unit(u1)
    game_manager.add_unit(u2)
    game_manager.add_unit(u3)
    game_manager.add_unit(u4)

    move = Move(u1, pr2)
    support_move = SupportMove(u3, pr2, move)

    game_manager.add_move(move)
    game_manager.add_move(support_move)
    
    #assert pr1.protection == u1.protection
    #assert pr2.protection == u2.protection
    #assert pr3.protection == u3.protection
    #assert pr4.protection == u4.protection

    game_manager.applying_moves()

    assert u1.location == pr2
    assert not u2 in game_manager.units
    assert u3.location == pr3
    assert u4.location == pr4

    #assert pr1.protection == 0
    #assert pr2.protection == u1.protection
    #assert pr3.protection == u3.protection
    #assert pr4.protection == u4.protection


def test_applying_moves_third_example():
    game_manager.add_unit(u1)
    game_manager.add_unit(u2)
    game_manager.add_unit(u3)
    game_manager.add_unit(u4)

    move = Move(u1, pr2)
    support_move = SupportMove(u3, pr2, move)
    support_hold = SupportHold(u4, pr2, u2)

    game_manager.add_move(move)
    game_manager.add_move(support_move)
    game_manager.add_move(support_hold)
    
    #assert pr1.protection == u1.protection
    #assert pr2.protection == u2.protection
    #assert pr3.protection == u3.protection
    #assert pr4.protection == u4.protection

    game_manager.applying_moves()

    assert u1.location == pr1
    assert u2.location == pr2
    assert u3.location == pr3
    assert u4.location == pr4

    #assert pr1.protection == u1.protection
    #assert pr2.protection == u2.protection
    #assert pr3.protection == u3.protection
    #assert pr4.protection == u4.protection


def test_applying_moves_fourth_example():
    game_manager = GameManager()

    pr1 = Province("PR1", ProvinceType.coast.value, True)
    pr2 = Province("PR2", ProvinceType.water.value, True)
    pr3 = Province("PR3", ProvinceType.water.value, True)
    pr4 = Province("PR4", ProvinceType.coast.value, True)

    u1 = Unit(pr1)
    u2 = Unit(pr2)
    u3 = Unit(pr3)


    convoy = ConvoyMove(u1, pr4, [u2, u3])
    game_manager.add_move(convoy)

    game_manager.add_province(pr1, [pr2])
    game_manager.add_province(pr2, [pr3])
    game_manager.add_province(pr3, [pr4])

    game_manager.add_move(convoy)

    game_manager.applying_moves()

    assert u1.location == pr4
    assert u2.location == pr2
    assert u3.location == pr3


def test_interrupt_support_move():
    u5 = Unit(pr5)

    game_manager.add_unit(u1)
    game_manager.add_unit(u2)
    game_manager.add_unit(u3)
    game_manager.add_unit(u4)
    game_manager.add_unit(u5)

    move = Move(u1, pr2)
    support_move = SupportMove(u3, pr2, move)
    move_for_interrupt = Move(u4, pr3)

    game_manager.add_move(move)
    game_manager.add_move(support_move)
    game_manager.add_move(move_for_interrupt)
    
    game_manager.applying_moves()

    assert u1.location == pr1
    assert u2.location == pr2
    assert u3.location == pr3
    assert u4.location == pr4

def test_interrupt_support_hold():
    u5 = Unit(pr5)
    
    game_manager.add_unit(u1)
    game_manager.add_unit(u2)
    game_manager.add_unit(u3)
    game_manager.add_unit(u4)
    game_manager.add_unit(u5)

    move_for_interrupt = Move(u1, pr2)
    move = Move(u3, pr4)
    support_move = SupportMove(u5, pr4, move)
    support_hold = SupportHold(u2, pr4, u4)

    game_manager.add_move(move)
    game_manager.add_move(support_hold)
    game_manager.add_move(support_move)
    game_manager.add_move(move_for_interrupt)
    
    game_manager.applying_moves()

    assert u1.location == pr1
    assert u2.location == pr2
    assert u3.location == pr4
    assert u4 not in game_manager.units
    assert u5.location == pr5

def test_interrupt_convoy_move():
    #   
    #                       water        coast
    #   PR1 ---------------- PR2 -_------ PR6
    #  coast                  |     -_    
    #                         |        -_ 
    #                         |           -_
    #                        PR3 -------- PR4 ------- PR5
    #                       water        water       coast
    #

    game_manager = GameManager()

    pr1 = Province("PR1", ProvinceType.coast.value, True)
    pr2 = Province("PR2", ProvinceType.water.value, True)
    pr3 = Province("PR3", ProvinceType.water.value, True)
    pr4 = Province("PR4", ProvinceType.water.value, True)
    pr5 = Province("PR5", ProvinceType.coast.value, True)
    pr6 = Province("PR5", ProvinceType.coast.value, True)

    game_manager.add_province(pr1, [pr2])
    game_manager.add_province(pr2, [pr1, pr3, pr4])
    game_manager.add_province(pr3, [pr2, pr4])
    game_manager.add_province(pr4, [pr3, pr2, pr5])
    game_manager.add_province(pr5, [pr4])
    game_manager.add_province(pr6, [pr2])

    u2 = Unit(pr2)
    u3 = Unit(pr3)
    u4 = Unit(pr4)
    u5 = Unit(pr5)
    u6 = Unit(pr6, UnitType.nautical.value)

    game_manager.add_unit(u2)
    game_manager.add_unit(u3)
    game_manager.add_unit(u4)
    game_manager.add_unit(u5)
    game_manager.add_unit(u6)

    convoy = ConvoyMove(u5, pr1, [u2, u3, u4])
    move_for_interrupt = Move(u6, pr2)

    game_manager.add_move(convoy)
    game_manager.add_move(move_for_interrupt)

    game_manager.applying_moves()


def test_ship_to_land():
    teardown_function()

    game_manager.add_province(pr1, [pr2])
    game_manager.add_province(pr2, [pr3])

    ship = Unit(pr1)

    move = Move(ship, pr2)

    game_manager.add_move(move)

    game_manager.applying_moves()

    with pytest.raises(ValueError):        
        move = Move(ship, pr3)

def test_overland_unit_to_water():
    teardown_function()

    game_manager.add_province(pr1, [pr2])
    game_manager.add_province(pr2, [pr3])

    unit = Unit(pr3)

    move = Move(unit, pr2)

    game_manager.add_move(move)

    game_manager.applying_moves()

    with pytest.raises(ValueError):        
        move = Move(unit, pr1)


@pytest.mark.parametrize(("country"), ( [1], ["123"], [[1, 2, 3]] ))
def test_add_country_with_type_error(country):
    with pytest.raises(TypeError):
        game_manager.add_country(country)
