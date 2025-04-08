import chess
import chess.svg
from app.strategies.random_strategy import RandomStrategy
from app.strategies.mcts_strategy import MCTSStrategy
from app.strategies.a_b_pruning_strategy import ABPruningStrategy
from app.strategies.stockfish_strategy import StockfishStrategy
from app.strategies.evaluators.neural_network_evaluator import NeuralNetworkEvaluator
from app.strategies.evaluators.standard_evaluator import StandardEvaluator
from app.benchmarking.benchmark import ChessAgentEvaluator
from app.view.gui_view import ChessGui

initial_board = chess.Board()
view = ChessGui(initial_board)

agent = ABPruningStrategy(
    board=None,
    evaluator=StandardEvaluator(),
    side=None,
    max_depth=3,
)

stockfish = StockfishStrategy(
    board=None,
    side=None,
    stockfish_path="/usr/local/bin/stockfish",
    skill_level=0,
    uci_elo=1320,
    move_time=0.1
)

random = RandomStrategy(
    board=None,
    side=None
)

try:
    evaluator = ChessAgentEvaluator(
        agent=agent,
        agent_name="AB + Standard",
        benchmark=stockfish,
        benchmark_name="Stockfish",
        benchmark_elo=1320,
        view=view
    )
    evaluator.run_match(n_games=10)
    evaluator.print_summary()

finally:
    view.cleanup()

svg = chess.svg.board(view.board)
with open("./app/chess_boards/final_board_state.svg", 'w') as f:
    f.write(svg)
