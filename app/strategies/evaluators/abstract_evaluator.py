from abc import ABC, abstractmethod
import chess

class PositionEvaluator(ABC):
    @abstractmethod
    def evaluate(self, board: chess.Board):
        pass

    def _game_over_evaluation(self, board: chess.Board, side: chess.Color):
        outcome_map = {}
        if side == chess.WHITE:
            outcome_map = {
                "1-0": 100000,
                "0-1": -100000,
                "1/2-1/2": 0,
            }
        else:
            outcome_map = {
                "1-0": -100000,
                "0-1": 100000,
                "1/2-1/2": 0,
            }

        return outcome_map[board.outcome().result()]