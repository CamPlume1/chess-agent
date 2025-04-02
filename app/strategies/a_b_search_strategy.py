import random
from chess import Board, WHITE, BLACK
from strategies.abstrategy import Strategy
from strategies.evaluators.abstract_evaluator import PositionEvaluator


class AB_Search(Strategy):

    def __init__(self, board: Board, positional_evaluator: PositionEvaluator, side=WHITE, max_depth=5):
        super().__init__(side=WHITE)
        self.evaluator = positional_evaluator
        self.board = board
        self.seen : dict[Board: int] = [] # Make sure to watch for deep copies in this-> Board is mutable, need to make a copy before hashing


    def select_move(self):
        valid_moves = self.board.legal_moves
        print(self.evaluator.evaluate(self.board, self.side))
        return random.choice(list(valid_moves)) if valid_moves else None
    
