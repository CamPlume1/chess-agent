import random
from chess import Board

class RandomStrategy:

    def __init__(self, board: Board):
        self.board = board


    def select_move(self):
        valid_moves = self.board.legal_moves
        return random.choice(list(valid_moves)) if valid_moves else None