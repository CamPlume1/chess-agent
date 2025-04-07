import chess
from controller.game_controller import GameController
from strategies.random_strategy import RandomStrategy
#from strategies.evaluators.neural_network_evaluator import NeuralNetworkEvaluator
from strategies.evaluators.standard_evaluator import StandardEvaluator
from strategies.abstrategy import Strategy
from view.gui_view import ChessGui
from strategies.a_b_search_strategy import AB_Search

chess_board = chess.Board()
#evaluator1 = NeuralNetworkEvaluator()
evaluator2 = StandardEvaluator()

agent1 = AB_Search(board=chess_board, positional_evaluator=evaluator2, side=chess.WHITE)
agent2 = RandomStrategy(board=chess_board)
view = ChessGui(chess_board)
controller = GameController(agent1, agent2, chess_board, view)
print(controller.play_game())
view.cleanup()
svg = chess.svg.board(chess_board)

with open("final_board_state.svg", 'w') as f:
    f.write(svg)