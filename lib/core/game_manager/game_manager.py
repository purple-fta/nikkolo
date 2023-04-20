from .map import *
import random


class GameManager(Map):
    """A set of commands for managing the game (adding moves, applying moves)"""
    
    def __init__(self):
        Map.__init__(self)

        self.moves = set()

    def add_move(self, new_move: Move):
        """Add new move

        Args:
            move (Move): Move class to add
        """

        # Type checking
        if not issubclass(type(new_move), Move):
            raise TypeError("The first argument has the wrong type")

        # If the target is out of reach
        if type(new_move) == ConvoyMove:
            pass
        elif new_move.province_target not in self.provinces_graph[new_move.unit.location]:
            return

        # If there is already a move for this unit, then delete it
        for move in self.moves:
            if new_move.unit == move.unit:
                self.moves.remove(move)
                self.moves.add(new_move)
                break
        else:
            self.moves.add(new_move)

    def applying_moves(self):
        """Applies all created moves (moves units)"""
        
        self._apply_support_moves()
        self._apply_support_holds()

        # Заполнение target_province_with_moves провинциями и ходами в которых они - цель
        target_province_with_moves = dict()
        for move in self.moves:
            if type(move) == Move or type(move) == ConvoyMove:
                if move.province_target in target_province_with_moves:
                    target_province_with_moves[move.province_target].append(move)
                else:
                    target_province_with_moves[move.province_target] = [move]



        for province in target_province_with_moves:
            move = self._get_move_with_max_power(target_province_with_moves[province])

            if move:
                unit_in_target = self._get_unit_in_province(move.province_target)
                protection = province.protection + (unit_in_target.protection if unit_in_target else 0)

                if move.power > protection:
                    if unit_in_target:
                        if self._get_free_neighboring_provinces(unit_in_target.location):
                            self._move_unit(unit_in_target, random.choice(self._get_free_neighboring_provinces(unit_in_target.location)))
                        else:
                            unit_in_target.location.protection -= unit_in_target.protection
                            self.units.remove(unit_in_target)

                    self._move_unit(move.unit, move.province_target)

        self.moves = set()

    def _apply_support_moves(self):
        for move in self.moves:
            if type(move) == SupportMove:
                move.move_target.power += move.power

    def _apply_support_holds(self):
        for move in self.moves:
            if type(move) == SupportHold:
                move.unit_target.protection += move.unit.protection

    def _get_move_with_max_power(self, moves: [Move]): 
        max_power = max([move.power for move in moves])
        
        if [move.power for move in moves].count(max_power) > 1:
            return None
        else:
            return moves[[move.power for move in moves].index(max_power)]        

    def _get_unit_in_province(self, province: Province):
        for unit in self.units:
            if unit.location == province:
                return unit

    def _get_free_neighboring_provinces(self, province):
        result_provinces = []
        
        for pr in self.provinces_graph[province]:
            if pr not in [unit.location for unit in self.units]:
                result_provinces.append(pr)

        return result_provinces

    def _move_unit(self, unit: Unit, target: Province):
        # Type checking
        if not issubclass(type(unit), Unit):
            raise TypeError("The first argument has the wrong type")
        if not issubclass(type(target), Province):
            raise TypeError("The second argument has the wrong type")

        unit.location = target
