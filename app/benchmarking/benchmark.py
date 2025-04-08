import chess
import math
import copy
from app.strategies.abstrategy import Strategy


class ChessAgentEvaluator:
    def __init__(
        self,
        agent: Strategy,
        benchmark: Strategy,
    ):
        self.base_agent = agent
        self.base_benchmark = benchmark
        self.results = {"win": 0, "loss": 0, "draw": 0}

    def play_game(self, agent_color="white") -> str:
        board = chess.Board()

        agent = copy.deepcopy(self.base_agent)
        benchmark = copy.deepcopy(self.base_benchmark)

        agent.side = chess.WHITE if agent_color == "white" else chess.BLACK
        benchmark.side = chess.BLACK if agent_color == "white" else chess.WHITE
        agent.board = board
        benchmark.board = board

        while not board.is_game_over():
            if board.turn == agent.side:
                move = agent.select_move()
            else:
                move = benchmark.select_move()

            if move not in board.legal_moves:
                print(f"Illegal move attempted: {move}")
                break

            board.push(move)

        return board.result()

    def run_match(self, n_games=10):
        self.results = {"win": 0, "loss": 0, "draw": 0}
        for i in range(n_games):
            agent_color = "white" if i % 2 == 0 else "black"
            result = self.play_game(agent_color=agent_color)

            if result == "1-0":
                outcome = "win" if agent_color == "white" else "loss"
            elif result == "0-1":
                outcome = "loss" if agent_color == "white" else "win"
            else:
                outcome = "draw"

            self.results[outcome] += 1
            print(f"Game {i + 1}: {result} → {outcome}")

    def calculate_elo_diff(self) -> float:
        total = sum(self.results.values())
        score = (self.results["win"] + 0.5 * self.results["draw"]) / total
        if score <= 0 or score >= 1:
            return float("inf") if score == 1 else float("-inf")
        return -400 * math.log10((1 / score) - 1)

    def print_summary(self, benchmark_elo=1600):
        diff = self.calculate_elo_diff()
        estimated_elo = benchmark_elo + diff
        print("\n=== Final Results ===")
        print(f"Wins: {self.results['win']}, Losses: {self.results['loss']}, Draws: {self.results['draw']}")
        print(f"Score: {(self.results['win'] + 0.5 * self.results['draw']) / sum(self.results.values()):.3f}")
        print(f"Estimated Elo difference vs benchmark: {diff:.2f}")
        print(f"Your agent ≈ {estimated_elo:.0f} Elo (assuming benchmark is {benchmark_elo})")
