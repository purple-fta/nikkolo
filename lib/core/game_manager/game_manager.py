from .map import *


class GameManager:
    def __init__(self, map):
        self.map = map
        self.moves = set()

    def add_move(self, move: Move):
        self.moves.add(move)

    def make_movements(self):
        for move in self.moves:
            move.unit.location = move.target
        
        self.moves = set()
