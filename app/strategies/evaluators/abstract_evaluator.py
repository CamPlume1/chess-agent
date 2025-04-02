from abc import ABC, abstractmethod
import chess

class PositionEvaluator(ABC):
    @abstractmethod
    def evaluate(self, board: chess.Board):
        pass

    def _game_over_evaluation(self, board: chess.Board):
        outcome_map = {
            "1-0": 1000000,
            "0-1": -1000000,
            "1/2-1/2": 0,
        }

        return outcome_map[board.outcome().result()]