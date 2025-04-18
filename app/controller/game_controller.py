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
        else:
            self.view = None

    def play_game(self, centipawn_benchmark: StockfishStrategy) -> str:
        # Reset board to home state
        if self.view:
            self.view.print_board()
        white_centipawn_loss = 0
        black_centipawn_loss = 0

        game_analysis_progression = [0]

        result = {}

        while not self.board.is_game_over():
            if len(self.board.move_stack) // 2 > 80:
                centipawn_benchmark.board = self.board
                stockfish_evaluation = centipawn_benchmark.get_centipawn_analysis()

                if stockfish_evaluation > 100:
                    result["result"] = "White"

                elif stockfish_evaluation < -100:
                    result["result"] = "Black"

                else:
                    result["result"] = "Draw"

                break

            board_before = self.board.copy()

            centipawn_benchmark.board = board_before
            top_engine_move = centipawn_benchmark.select_move()
            board_before.push(top_engine_move)
            top_engine_move_centipawn = centipawn_benchmark.get_centipawn_analysis()

            centipawn_benchmark.board = self.board
            move = self.current_agent.select_move()
            self.board.push(move)
            actual_move_centipawn = centipawn_benchmark.get_centipawn_analysis()

            clamped_actual_move_centipawn = min(abs(actual_move_centipawn), 1000) * (1 if actual_move_centipawn > 0 else -1)
            game_analysis_progression.append(clamped_actual_move_centipawn)

            if self.view:
                self.view.print_board()
                time.sleep(1) 
            if self.current_agent is self.white:
                white_centipawn_loss += top_engine_move_centipawn - actual_move_centipawn
                self.current_agent = self.black
            else:
                black_centipawn_loss += actual_move_centipawn - top_engine_move_centipawn
                self.current_agent = self.white
        
        result["white_total_centipawn_loss"] = white_centipawn_loss
        result["white_average_centipawn_loss"] = white_centipawn_loss / (len(self.board.move_stack) / 2)
        result["black_total_centipawn_loss"] = black_centipawn_loss
        result["black_average_centipawn_loss"] = black_centipawn_loss / (len(self.board.move_stack) / 2)
        result["game_analysis_progression"] = game_analysis_progression[:-1]

        # Determine the game result
        if self.board.is_checkmate():
            # If game is over by checkmate, the last player to move was the winner
            result["result"] = "Black" if self.current_agent is self.white else "White"
        elif self.board.is_game_over():
            result["result"] = "Draw"

        return result