from abc import ABC, abstractmethod
from chess import WHITE


class Strategy(ABC):
    def __init__(self, side=WHITE):
        self.side = side

    @abstractmethod
    def select_move(self):
        pass