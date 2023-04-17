from lib.core.game_manager import GameManager, Move, SupportHold, SupportMove, \
                                  Province, ProvinceType, Unit

import pytest


pr1 = Province("PR1", ProvinceType.water.value, False)
pr2 = Province("PR2", ProvinceType.coast.value, False)
pr3 = Province("PR3", ProvinceType.land.value,  False)
pr4 = Province("PR4", ProvinceType.coast.value, False)
pr5 = Province("PR5", ProvinceType.water.value, False)

u1 = Unit(pr1)
u2 = Unit(pr2)
u3 = Unit(pr3)
u4 = Unit(pr4)

game_manager = GameManager()


def setup_function():
    global game_manager
    game_manager = GameManager()

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

    move2 = SupportMove(u1, pr2, move1)
    game_manager.add_move(move2)
    assert game_manager.moves == set([move1, move2])

    move3 = SupportHold(pr4, pr2, u2)
    game_manager.add_move(move3)
    assert game_manager.moves == set([move1, move2, move3])

def test_add_move_with_type_error():
    game_manager.add_move(Move(u1, pr2))

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
    game_manager.add_transition(pr1, pr3)

    game_manager.add_unit(u2)
    game_manager.add_unit(u3)
    game_manager.add_unit(u4)

    move = Move(u4, pr3)
    support_move = SupportMove(u2, pr3, move)

    assert u2.location == pr2
    assert u3.location == pr1
    assert u4.location == pr3


def test_applying_moves_second_example_with_destroy_unit():
    game_manager.add_transition(pr1, pr3)

    game_manager.add_unit(u2)
    game_manager.add_unit(u3)
    game_manager.add_unit(u4)

    move = Move(u4, pr3)
    support_move = SupportMove(u2, pr3, move)

    assert u2.location == pr2
    assert u3.location == pr1
    assert u4.location == pr3

