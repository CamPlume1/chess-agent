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
from dotenv import load_dotenv
import os

load_dotenv()
STOCKFISH_PATH = os.getenv("STOCKFISH_PATH")

initial_board = chess.Board()

######################################## Strategies ########################################

mcts_standard = MCTSStrategy(
    board=None,
    evaluator=StandardEvaluator(),
    side=None,
)

mcts_ff = MCTSStrategy(
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

ab_standard_depth_4 = ABPruningStrategy(
    board=None,
    evaluator=StandardEvaluator(),
    side=None,
    max_depth=4,
)

ab_ff = ABPruningStrategy(
    board=None,
    evaluator=NeuralNetworkEvaluator(),
    side=None,
)

ab_cnn = ABPruningStrategy(
    board=None,
    evaluator=ConvolutionalNetworkEvaluator(),
    side=None,
)

######################################## Benchmarks ########################################

stockfish = StockfishStrategy(
    board=None,
    side=None,
    stockfish_path=STOCKFISH_PATH,
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
    stockfish_path=STOCKFISH_PATH,
    skill_level=20,
    uci_elo=3000,
    move_time=0.1
)

######################################## Cam's Matchups ########################################

matchup_1 = ChessAgentEvaluator(
    agent=ab_standard,
    agent_name="AB + Standard",
    benchmark=ab_ff,
    benchmark_name="AB + FF",
    benchmark_elo=0,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_2 = ChessAgentEvaluator(
    agent=ab_standard,
    agent_name="AB + Standard",
    benchmark=ab_cnn,
    benchmark_name="AB + CNN",
    benchmark_elo=0,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_3 = ChessAgentEvaluator(
    agent=ab_standard,
    agent_name="AB + Standard",
    benchmark=mcts_standard,
    benchmark_name="MCTS + Standard",
    benchmark_elo=0,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_4 = ChessAgentEvaluator(
    agent=ab_standard,
    agent_name="AB + Standard",
    benchmark=mcts_ff,
    benchmark_name="MCTS + FF",
    benchmark_elo=0,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_5 = ChessAgentEvaluator(
    agent=ab_standard,
    agent_name="AB + Standard",
    benchmark=mcts_cnn,
    benchmark_name="MCTS + CNN",
    benchmark_elo=0,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_6 = ChessAgentEvaluator(
    agent=ab_ff,
    agent_name="AB + FF",
    benchmark=ab_cnn,
    benchmark_name="AB + CNN",
    benchmark_elo=0,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_7 = ChessAgentEvaluator(
    agent=ab_ff,
    agent_name="AB + FF",
    benchmark=mcts_standard,
    benchmark_name="MCTS + Standard",
    benchmark_elo=0,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_8 = ChessAgentEvaluator(
    agent=ab_ff,
    agent_name="AB + FF",
    benchmark=mcts_ff,
    benchmark_name="MCTS + FF",
    benchmark_elo=0,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_9 = ChessAgentEvaluator(
    agent=ab_ff,
    agent_name="AB + FF",
    benchmark=mcts_cnn,
    benchmark_name="MCTS + CNN",
    benchmark_elo=0,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_10 = ChessAgentEvaluator(
    agent=ab_cnn,
    agent_name="AB + CNN",
    benchmark=mcts_standard,
    benchmark_name="MCTS + Standard",
    benchmark_elo=0,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_11 = ChessAgentEvaluator(
    agent=ab_cnn,
    agent_name="AB + CNN",
    benchmark=mcts_ff,
    benchmark_name="MCTS + FF",
    benchmark_elo=0,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_12 = ChessAgentEvaluator(
    agent=ab_cnn,
    agent_name="AB + CNN",
    benchmark=mcts_cnn,
    benchmark_name="MCTS + CNN",
    benchmark_elo=0,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

######################################## Adam's Matchups ########################################

matchup_13 = ChessAgentEvaluator(
    agent=mcts_standard,
    agent_name="MCTS + Standard",
    benchmark=mcts_ff,
    benchmark_name="MCTS + FF",
    benchmark_elo=0,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_14 = ChessAgentEvaluator(
    agent=mcts_standard,
    agent_name="MCTS + Standard",
    benchmark=mcts_cnn,
    benchmark_name="MCTS + CNN",
    benchmark_elo=0,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_15 = ChessAgentEvaluator(
    agent=mcts_ff,
    agent_name="MCTS + FF",
    benchmark=mcts_cnn,
    benchmark_name="MCTS + CNN",
    benchmark_elo=0,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_16 = ChessAgentEvaluator(
    agent=ab_standard,
    agent_name="AB + Standard",
    benchmark=random,
    benchmark_name="Random",
    benchmark_elo=500,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_17 = ChessAgentEvaluator(
    agent=ab_ff,
    agent_name="AB + FF",
    benchmark=stockfish,
    benchmark_name="Random",
    benchmark_elo=500,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_18 = ChessAgentEvaluator(
    agent=ab_cnn,
    agent_name="AB + CNN",
    benchmark=stockfish,
    benchmark_name="Random",
    benchmark_elo=500,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_19 = ChessAgentEvaluator(
    agent=mcts_standard,
    agent_name="MCTS + Standard",
    benchmark=stockfish,
    benchmark_name="Random",
    benchmark_elo=500,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_20 = ChessAgentEvaluator(
    agent=mcts_ff,
    agent_name="MCTS + FF",
    benchmark=stockfish,
    benchmark_name="Random",
    benchmark_elo=500,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_21 = ChessAgentEvaluator(
    agent=mcts_cnn,
    agent_name="MCTS + CNN",
    benchmark=stockfish,
    benchmark_name="Random",
    benchmark_elo=500,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_22 = ChessAgentEvaluator(
    agent=ab_standard_depth_4,
    agent_name="AB + Standard Depth=4",
    benchmark=stockfish,
    benchmark_name="Stockfish",
    benchmark_elo=1320,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_23 = ChessAgentEvaluator(
    agent=ab_ff,
    agent_name="AB + FF",
    benchmark=stockfish,
    benchmark_name="Stockfish",
    benchmark_elo=1320,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_24 = ChessAgentEvaluator(
    agent=ab_cnn,
    agent_name="AB + CNN",
    benchmark=stockfish,
    benchmark_name="Stockfish",
    benchmark_elo=1320,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_25 = ChessAgentEvaluator(
    agent=mcts_standard,
    agent_name="MCTS + Standard",
    benchmark=stockfish,
    benchmark_name="Stockfish",
    benchmark_elo=1320,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_26 = ChessAgentEvaluator(
    agent=mcts_ff,
    agent_name="MCTS + FF",
    benchmark=stockfish,
    benchmark_name="Stockfish",
    benchmark_elo=1320,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

matchup_27 = ChessAgentEvaluator(
    agent=mcts_cnn,
    agent_name="MCTS + CNN",
    benchmark=stockfish,
    benchmark_name="Stockfish",
    benchmark_elo=1320,
    view=None,
    centipawn_benchmark=centipawn_benchmark,
    view_game_progression=True
)

cam_matchups = [matchup_1, matchup_2, matchup_3, matchup_4, matchup_5, matchup_6, matchup_7, matchup_8, matchup_9, matchup_10, matchup_11, matchup_12]
adam_matchups = [matchup_13, matchup_14, matchup_15, matchup_16, matchup_17, matchup_18, matchup_19, matchup_20, matchup_21, matchup_22, matchup_23, matchup_24, matchup_25, matchup_26, matchup_27, matchup_27]

for i in range(len(cam_matchups)):
    print(f"Beginning matchup {i + 1}")
    cam_matchups[i].run_match(n_games=1)
    cam_matchups[i].print_summary()

