import random
import chess
from .abstrategy import Strategy

class RandomStrategy(Strategy):
    def __init__(self, board: chess.Board, side: chess.Color):
        super().__init__(board=board, side=side)

    def select_move(self):
        valid_moves = self.board.legal_moves
        return random.choice(list(valid_moves)) if valid_moves else None