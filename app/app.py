import chess
from app.controller.game_controller import GameController
from app.strategies.random_strategy import RandomStrategy
from app.strategies.mcts_strategy import MCTSStrategy
from app.strategies.evaluators.neural_network_evaluator import NeuralNetworkEvaluator
from app.strategies.abstrategy import Strategy
from app.view.gui_view import ChessGui

chess_board = chess.Board()

agent1 = RandomStrategy(chess_board)
agent2 = RandomStrategy(chess_board)
view = ChessGui(chess_board)
controller = GameController(agent1, agent2, chess_board, view)
print(controller.play_game())
view.cleanup()