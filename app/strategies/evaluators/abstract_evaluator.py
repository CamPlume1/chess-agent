from abc import ABC, abstractmethod
import chess

class PositionEvaluator(ABC):
    @abstractmethod
    def evaluate(self, board: chess.Board):
        pass