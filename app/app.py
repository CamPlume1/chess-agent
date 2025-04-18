import chess
import chess.svg
from app.controller.game_controller import GameController
from app.strategies.random_strategy import RandomStrategy
from app.strategies.mcts_strategy import MCTSStrategy
from app.strategies.a_b_pruning_strategy import ABPruningStrategy
from app.strategies.stockfish_strategy import StockfishStrategy
from app.strategies.evaluators.neural_network_evaluator import NeuralNetworkEvaluator
from app.strategies.evaluators.convolutional_network_evaluator import ConvolutionalNetworkEvaluator
from app.strategies.evaluators.standard_evaluator import StandardEvaluator
from app.benchmarking.benchmark import ChessAgentEvaluator
from app.view.gui_view import ChessGui

initial_board = chess.Board()
#view = ChessGui(initial_board)
view = None

mcts_standard = MCTSStrategy(
    board=None,
    evaluator=NeuralNetworkEvaluator(),
    side=None,
)

agent2 = MCTSStrategy(
    board=None,
    evaluator=ConvolutionalNetworkEvaluator(),
    side=None,
)

mcts_ffn = MCTSStrategy(
    board=None,
    evaluator=NeuralNetworkEvaluator(),
    side=None,
)

mcts_cnn = MCTSStrategy(
    board=None,
    evaluator=ConvolutionalNetworkEvaluator(),
    side=None,
)


ab_standard = ABPruningStrategy(
    board=None,
    evaluator=StandardEvaluator(),
    side=None,
)

ab_ffn = ABPruningStrategy(
    board=None,
    evaluator=NeuralNetworkEvaluator(),
    side=None,
)

ab_cnn = ABPruningStrategy(
    board=None,
    evaluator=ConvolutionalNetworkEvaluator(),
    side=None,
)

stockfish = StockfishStrategy(
    board=None,
    side=None,
    stockfish_path="C:/Users/Cam/Desktop/stockfish/stockfish/stockfish-windows-x86-64-avx2.exe",
    skill_level=0,
    uci_elo=1320,
    move_time=0.1
)

random = RandomStrategy(
    board=None,
    side=None
)

centipawn_benchmark = StockfishStrategy(
    board=None,
    side=None,
    stockfish_path="C:/Users/Cam/Desktop/stockfish/stockfish/stockfish-windows-x86-64-avx2.exe",
    skill_level=20,
    uci_elo=3000,
    move_time=0.1
)

try:
    evaluator = ChessAgentEvaluator(
        agent=agent,
        agent_name="MCTS + FF",
        benchmark=agent2,
        benchmark_name="MCTS + CNN",
        benchmark_elo=900,
        view=view,
        centipawn_benchmark=centipawn_benchmark
    )
    evaluator.run_match(n_games=25)
    evaluator.print_summary()

finally:
    if view:
        view.cleanup()

if view:
    svg = chess.svg.board(view.board)
    with open("./app/chess_boards/final_board_state.svg", 'w') as f:
        f.write(svg)
