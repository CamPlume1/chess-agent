import chess
from app.controller.game_controller import GameController
from app.strategies.random_strategy import RandomStrategy
from app.strategies.mcts_strategy import MCTSStrategy
from app.strategies.a_b_pruning_strategy import ABPruningStrategy
from app.strategies.evaluators.neural_network_evaluator import NeuralNetworkEvaluator
from app.strategies.evaluators.convolutional_network_evaluator import ConvolutionalNetworkEvaluator
from app.strategies.evaluators.standard_evaluator import StandardEvaluator
from app.view.gui_view import ChessGui

chess_board = chess.Board()
evaluator1 = ConvolutionalNetworkEvaluator()
evaluator2 = NeuralNetworkEvaluator()

agent1 = ABPruningStrategy(board=chess_board, evaluator=evaluator1, side=chess.WHITE)
agent2 = RandomStrategy(chess_board)
view = ChessGui(chess_board)
controller = GameController(agent1, agent2, chess_board, view)
print(controller.play_game())
view.cleanup()
svg = chess.svg.board(chess_board)

with open("final_board_state.svg", 'w') as f:
    f.write(svg)