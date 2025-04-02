import chess
from app.controller.game_controller import GameController
from app.strategies.random_strategy import RandomStrategy
from app.strategies.mcts_strategy import MCTSStrategy
from app.strategies.a_b_pruning_strategy import ABPruningStrategy
from app.strategies.evaluators.neural_network_evaluator import NeuralNetworkEvaluator
from app.strategies.evaluators.standard_evaluator import StandardEvaluator
from app.strategies.abstrategy import Strategy
from app.view.gui_view import ChessGui

chess_board = chess.Board()
evaluator1 = NeuralNetworkEvaluator()
evaluator2 = StandardEvaluator()

agent1 = MCTSStrategy(board=chess_board, evaluator=evaluator1, side=chess.WHITE)
agent2 = ABPruningStrategy(board=chess_board, evaluator=evaluator2, side=chess.BLACK)
view = ChessGui(chess_board)
controller = GameController(agent1, agent2, chess_board, view)
print(controller.play_game())
view.cleanup()