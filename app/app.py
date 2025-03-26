from controller.game_controller import GameController
from strategies.random_strategy import RandomStrategy
from view.gui_view import ChessGui
from chess import Board


chess_board = Board()

agent1 = RandomStrategy(chess_board)
agent2 = RandomStrategy(chess_board)
view = ChessGui(chess_board)
controller = GameController(agent1, agent2, view)
controller.play_game()