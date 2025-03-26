import time
from chess import Board

class GameController:


    def __init__(self, agent1, agent2, board: Board, view=None):
        self.white = agent1
        self.black = agent2
        self.current_agent = self.white
        self.board = board
        if view:
            self.view = view

    def play_game(self):
        # Reset board to home state
        self.view.print_board()

        while not self.board.is_game_over():
            print("Game iteration")
            move = self.current_agent.select_move()
            self.board.push(move)
            if self.view:
                self.view.print_board()
                time.sleep(0.5) 
            if self.current_agent is self.white:
                self.current_agent = self.black
            else:
                self.current_agent = self.white
        