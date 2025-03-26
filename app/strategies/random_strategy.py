import random
from chess import Board

class RandomStrategy:

    def __init__(self, board: Board):
        self.board = board


    def selectMove(self):
        valid_moves = self.board.legal_moves()
        return random.choice(valid_moves) if valid_moves else None