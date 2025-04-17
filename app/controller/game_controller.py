import time
import chess
from app.strategies.abstrategy import Strategy
from app.strategies.stockfish_strategy import StockfishStrategy

class GameController:


    def __init__(self, agent1: Strategy, agent2: Strategy, board: chess.Board, view=None):
        self.white = agent1
        self.black = agent2
        self.current_agent = self.white
        self.board = board
        if view:
            self.view = view

    def play_game(self, centipawn_benchmark: StockfishStrategy) -> str:
        # Reset board to home state
        self.view.print_board()
        white_centipawn_loss = 0
        black_centipawn_loss = 0

        while not self.board.is_game_over():
            print("Game iteration")

            board_before = self.board.copy()

            centipawn_benchmark.board = board_before
            top_engine_move = centipawn_benchmark.select_move()
            board_before.push(top_engine_move)
            top_engine_move_centipawn = centipawn_benchmark.get_centipawn_analysis()

            centipawn_benchmark.board = self.board
            move = self.current_agent.select_move()
            self.board.push(move)
            actual_move_centipawn = centipawn_benchmark.get_centipawn_analysis()

            if self.view:
                self.view.print_board()
                time.sleep(1) 
            if self.current_agent is self.white:
                white_centipawn_loss += top_engine_move_centipawn - actual_move_centipawn
                self.current_agent = self.black
            else:
                black_centipawn_loss += actual_move_centipawn - top_engine_move_centipawn
                self.current_agent = self.white
        
        result = {
            "white_total_centipawn_loss": white_centipawn_loss,
            "white_average_centipawn_loss": white_centipawn_loss / (len(self.board.move_stack) / 2),
            "black_total_centipawn_loss": black_centipawn_loss,
            "black_average_centipawn_loss": black_centipawn_loss / (len(self.board.move_stack) / 2)
        }

        # Determine the game result
        if self.board.is_checkmate():
            # If game is over by checkmate, the last player to move was the winner
            result["result"] = "Black" if self.current_agent is self.white else "White"
        else:
            result["result"] = "Draw"

        return result