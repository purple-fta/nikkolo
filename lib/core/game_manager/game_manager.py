from .map import *
import random

from lib.map_creator.gui_unit import *


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
        #elif new_move.province_target not in self.provinces_graph[new_move.unit.location]:
        #    return

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
        
        self._apply_interrupt_moves()
        
        self._apply_support_moves()
        self._apply_support_holds()

        # Заполнение target_province_with_moves провинциями и ходами в которых они - цель
        target_province_with_moves = dict()
        for move in self.moves:
            if (type(move) == Move or type(move) == ConvoyMove) or (type(move) == GuiMove or type(move) == ConvoyMove):
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
                        if self._get_free_neighboring_provinces(unit_in_target.location, target_province_with_moves):
                            self._move_unit(unit_in_target, random.choice(self._get_free_neighboring_provinces(unit_in_target.location, target_province_with_moves)))
                        else:
                            unit_in_target.location.protection -= unit_in_target.protection
                            self.units.remove(unit_in_target)
                            for country in self.countries:
                                if unit_in_target in country.units:
                                    country.units.remove(unit_in_target)

                    self._move_unit(move.unit, move.province_target)

        self.moves = set()

        self._delete_countries_without_province_with_initial_sc()    

    def paint_map(self):
        for country in self.countries:
            for unit in country.units:
                if not unit.location.is_supply_center:
                    country.provinces.add(unit.location)

    def form(self):
        for country in self.countries:
            for unit in country.units:
                self.add_province_to_country(unit.location, country)


    def _apply_support_moves(self):
        for move in self.moves:
            if type(move) == SupportMove or type(move) == GuiSupportMove:
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

    def _get_free_neighboring_provinces(self, province, target_province_with_moves):
        result_provinces = []
        
        for pr in self.provinces_graph[province]:
            if pr not in [unit.location for unit in self.units]:
                if pr not in target_province_with_moves:
                    result_provinces.append(pr)

        return result_provinces

    def _move_unit(self, unit: Unit, target: Province):
        # Type checking
        if not issubclass(type(unit), Unit):
            raise TypeError("The first argument has the wrong type")
        if not issubclass(type(target), Province):
            raise TypeError("The second argument has the wrong type")

        if type(unit) == GuiUnit:
            x, y = random.choice(target.tiles_coordinates)
            unit.coordinates = [x*16, y*16]

        unit.location = target

    def _apply_interrupt_moves(self):
        moves_for_remove = []

        for move in self.moves:
            if type(move) == Move:
                if self._get_unit_in_province(move.province_target):
                    for move2 in self.moves:
                        if move2.unit.location == move.province_target:
                            if type(move2) == SupportHold or type(move2) == SupportMove or type(move2) == GuiSupportMove:
                                moves_for_remove.append(move2)
                        elif type(move2) == ConvoyMove:
                            for ship in move2.ships:
                                if ship.location == move.province_target:
                                    moves_for_remove.append(move2)

        for i in moves_for_remove:
            self.moves.remove(i)

    def _delete_countries_without_province_with_initial_sc(self):
        country_to_remove = []
        unit_to_remove = []
        for country in self.countries:
            for pr_with_sc in country.initial_provinces_with_sc:
                if pr_with_sc in country.provinces:
                    break
            else:
                country_to_remove.append(country)
                for unit in country.units:
                    unit_to_remove.append(unit)
        
        for country in country_to_remove:
            self.countries.remove(country)
        for unit in unit_to_remove:
            self.units.remove(unit)
