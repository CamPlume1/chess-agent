from strategies.a_b_search_strategy import AB_Search
from strategies.evaluators.standard_evaluator import StandardEvaluator
from controller.game_controller import GameController
from strategies.random_strategy import RandomStrategy
from strategies.abstrategy import Strategy
from view.gui_view import ChessGui
from chess import Board


chess_board = Board()
simple_evaluator = StandardEvaluator()

agent1 = RandomStrategy(chess_board)
agent2 = AB_Search(chess_board, simple_evaluator)
view = ChessGui(chess_board)
controller = GameController(agent1, agent2, chess_board, view)
print(controller.play_game())
view.cleanup()