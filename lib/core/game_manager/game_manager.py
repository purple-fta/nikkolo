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
        if new_move.target not in self.provinces_graph[new_move.unit.location]:
            return

        for move in self.moves:
            if new_move.unit == move.unit:
                self.moves.remove(move)
                self.moves.add(new_move)
                break
        else:
            self.moves.add(new_move)

    def applying_moves(self):
        """Applies all created moves (moves units)
        """
        target_provinces = dict()

        for move in self.moves:
            if move.target in target_provinces:
                target_provinces[move.target].append(move)
            else:
                target_provinces[move.target] = [move]

        for target_province in target_provinces:
            self._apply_and_delate_support_moves(target_provinces[target_province])
            self._apply_and_delate_support_holds(target_provinces[target_province])
            
            move = self._get_move_with_max_power(target_provinces[target_province])

            if move:
                unit_in_target = self._get_unit_in_province(move.target)

                if move.power > unit_in_target.protection:
                    move.unit.location.protection -=  move.unit.protection

                    if unit_in_target:
                        unit_in_target.location = random.choice(self._get_free_neighboring_provinces(unit_in_target.location))

                    move.unit.location = move.target

        self.moves = set()
    
    def _apply_and_delate_support_moves(self, moves: [Move]):
        i = 0
        while i < len(moves):
            if type(moves[i]) == SupportMove:
                moves[i].move_target.power += moves[i].power
                moves.remove(moves[i])
            else:
                i += 1

    def _apply_and_delate_support_holds(self, moves: [Move]):
        i = 0
        while i < len(moves):
            if type(moves[i]) == SupportHold:
                moves[i].unit_target.protection += moves[i].unit.protection
                moves.remove(moves[i])
            else:
                i += 1


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