from .map import *


class GameManager:
    def __init__(self, map):
        self.map = map
        self.moves = set()

    def add_move(self, move: Move):
        self.moves.add(move)
