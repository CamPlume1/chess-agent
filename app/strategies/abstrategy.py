from abc import ABC, abstractmethod


class Strategy(ABC):

    @abstractmethod
    def select_move(self):
        pass