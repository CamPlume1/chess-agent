import time
from chess import Board
from strategies.abstrategy import Strategy

class GameController:


    def __init__(self, agent1: Strategy, agent2: Strategy, board: Board, view=None):
        self.white = agent1
        self.black = agent2
        self.current_agent = self.white
        self.board = board
        if view:
            self.view = view

    def play_game(self) -> str:
        # Reset board to home state
        self.view.print_board()

        while not self.board.is_game_over():
            print("Game iteration")
            move = self.current_agent.select_move()
            self.board.push(move)
            if self.view:
                self.view.print_board()
                time.sleep(1) 
            if self.current_agent is self.white:
                self.current_agent = self.black
            else:
                self.current_agent = self.white
        
        # Determine the game result
        if self.board.is_checkmate():
            # If game is over by checkmate, the last player to move was the winner
            return "Black" if self.current_agent is self.white else "White"
        else:
            return "Draw"
