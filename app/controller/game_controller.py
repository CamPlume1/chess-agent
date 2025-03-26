from chess import Board

class GameController:


    def __init__(self, agent1, agent2, view=None):
        self.white = agent1
        self.black = agent2
        if view:
            self.view = view

    def play_game(self):
        # Reset board to home state
        self.view.print_board()
        