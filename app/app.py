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

mcts_standard = MCTSStrategy(
    board=None,
    evaluator=StandardEvaluator(),
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


matchup_1 = ChessAgentEvaluator(
    agent=ab_standard,
    agent_name="AB + Standard",
    benchmark=ab_ffn,
    benchmark_name="AB + FF",
    benchmark_elo=900,
    view=None,
    centipawn_benchmark=centipawn_benchmark
)

matchup_2 = ChessAgentEvaluator(
    agent=ab_standard,
    agent_name="AB + Standard",
    benchmark=ab_cnn,
    benchmark_name="AB + CNN",
    benchmark_elo=900,
    view=None,
    centipawn_benchmark=centipawn_benchmark
)

matchup_3 = ChessAgentEvaluator(
    agent=ab_standard,
    agent_name="AB + Standard",
    benchmark=mcts_standard,
    benchmark_name="MCTS + Standard",
    benchmark_elo=900,
    view=None,
    centipawn_benchmark=centipawn_benchmark
)

matchup_4 = ChessAgentEvaluator(
    agent=ab_standard,
    agent_name="AB + Standard",
    benchmark=mcts_ffn,
    benchmark_name="MCTS + FF",
    benchmark_elo=900,
    view=None,
    centipawn_benchmark=centipawn_benchmark
)

matchup_5 = ChessAgentEvaluator(
    agent=ab_standard,
    agent_name="AB + Standard",
    benchmark=mcts_cnn,
    benchmark_name="MCTS + CNN",
    benchmark_elo=900,
    view=None,
    centipawn_benchmark=centipawn_benchmark
)

matchup_6 = ChessAgentEvaluator(
    agent=ab_ffn,
    agent_name="AB + FFN",
    benchmark=ab_cnn,
    benchmark_name="AB + CNN",
    benchmark_elo=900,
    view=None,
    centipawn_benchmark=centipawn_benchmark
)



matchup_7 = ChessAgentEvaluator(
    agent=ab_ffn,
    agent_name="AB + FFN",
    benchmark=mcts_standard,
    benchmark_name="MCTS + Standard",
    benchmark_elo=900,
    view=None,
    centipawn_benchmark=centipawn_benchmark
)


matchup_8 = ChessAgentEvaluator(
    agent=ab_ffn,
    agent_name="AB + FFN",
    benchmark=mcts_ffn,
    benchmark_name="MCTS + FF",
    benchmark_elo=900,
    view=None,
    centipawn_benchmark=centipawn_benchmark
)


matchup_9 = ChessAgentEvaluator(
    agent=ab_ffn,
    agent_name="AB + FFN",
    benchmark=mcts_cnn,
    benchmark_name="MCTS + CNN",
    benchmark_elo=900,
    view=None,
    centipawn_benchmark=centipawn_benchmark
)


matchup_10 = ChessAgentEvaluator(
    agent=ab_cnn,
    agent_name="AB + CNN",
    benchmark=mcts_standard,
    benchmark_name="MCTS + Standard",
    benchmark_elo=900,
    view=None,
    centipawn_benchmark=centipawn_benchmark
)

matchup_11 = ChessAgentEvaluator(
    agent=ab_cnn,
    agent_name="AB + CNN",
    benchmark=mcts_ffn,
    benchmark_name="MCTS + FFN",
    benchmark_elo=900,
    view=None,
    centipawn_benchmark=centipawn_benchmark
)

matchup_12 = ChessAgentEvaluator(
    agent=ab_cnn,
    agent_name="AB + CNN",
    benchmark=mcts_cnn,
    benchmark_name="MCTS + CNN",
    benchmark_elo=900,
    view=None,
    centipawn_benchmark=centipawn_benchmark
)

smart = ABPruningStrategy(
    board=None,
    evaluator=StandardEvaluator(),
    side=None,
    max_depth=4,
)

matchup_13 = ChessAgentEvaluator(
    agent=smart,
    agent_name="AB + Standard D=4",
    benchmark=stockfish,
    benchmark_name="Stockfish",
    benchmark_elo=900,
    view=None,
    centipawn_benchmark=centipawn_benchmark
)



matchups = [matchup_1, matchup_2, matchup_3, matchup_4, matchup_5, matchup_6, matchup_7, matchup_8, matchup_9, matchup_10, matchup_11, matchup_12, matchup_13]

for i in range(len(matchups)):
    print("Beginning matchup: ", i)
    matchups[i].run_match(n_games=25)
    matchups[i].print_summary()



