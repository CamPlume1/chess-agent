import random
import chess
from .abstrategy import Strategy

class RandomStrategy(Strategy):
    def __init__(self, board: chess.Board):
        self.board = board

    def select_move(self):
        valid_moves = self.board.legal_moves
        return random.choice(list(valid_moves)) if valid_moves else None