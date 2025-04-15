from abc import ABC, abstractmethod
import chess

class PositionEvaluator(ABC):
    @abstractmethod
    def evaluate(self, board: chess.Board):
        pass

    def _game_over_evaluation(self, board: chess.Board, remaining_depth: int = 0):
        outcome_map = {
            "1-0": 10000000 + remaining_depth,
            "0-1": -10000000 - remaining_depth,
            "1/2-1/2": 0,
        }
        return outcome_map[board.outcome().result()]