from abc import ABC, abstractmethod
from chess import WHITE, Board, Color

class Strategy(ABC):
    def __init__(self, board: Board = None, side: Color = WHITE):
        self.board = board
        self.side = side

    @abstractmethod
    def select_move(self):
        pass