from abc import ABC, abstractmethod
from chess import Board

class PositionEvaluator(ABC):


    @abstractmethod
    def evaluate(board: Board):
        pass