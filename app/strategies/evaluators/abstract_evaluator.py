from abc import ABC, abstractmethod
from chess import Board, Outcome, WHITE, BLACK, Color

class PositionEvaluator(ABC):


    @abstractmethod
    def evaluate(board: Board):
        pass


    def _game_over_evaluation(self, board: Board, side: Color):
        outcome_map = {}
        if side == WHITE:
            outcome_map = {
                "1-0": 1000000,
                "0-1": -1000000,
                "1/2-1/2": 0,
            }
        else:
            outcome_map = {
                "1-0": -1000000,
                "0-1": 1000000,
                "1/2-1/2": 0,
            }

        return outcome_map[board.outcome().result()]