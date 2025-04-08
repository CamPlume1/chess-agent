import chess
import math
from app.strategies.abstrategy import Strategy
from app.controller.game_controller import GameController
from app.view.gui_view import ChessGui

class ChessAgentEvaluator:
    def __init__(
        self,
        agent: Strategy,
        benchmark: Strategy,
        benchmark_elo: int,
        view: ChessGui,
        agent_name: str,
        benchmark_name: str
    ):
        self.agent = agent
        self.benchmark = benchmark
        self.benchmark_elo = benchmark_elo
        self.view = view
        self.agent_name = agent_name
        self.benchmark_name = benchmark_name
        self.results = {"win": 0, "loss": 0, "draw": 0}
        self.total_moves = 0

    def play_game(self, agent_color="white") -> str:
        board = chess.Board()

        if self.view:
            self.view.board = board

        if agent_color == "white":
            self.agent.side = chess.WHITE
            self.benchmark.side = chess.BLACK
            white, black = self.agent, self.benchmark
        else:
            self.agent.side = chess.BLACK
            self.benchmark.side = chess.WHITE
            white, black = self.benchmark, self.agent

        self.agent.board = board
        self.benchmark.board = board

        controller = GameController(white, black, board, view=self.view)
        winner = controller.play_game()

        self.total_moves += len(board.move_stack)

        if winner == "White":
            return "1-0"
        elif winner == "Black":
            return "0-1"
        else:
            return "1/2-1/2"

    def run_match(self, n_games):
        self.results = {"win": 0, "loss": 0, "draw": 0}
        self.total_moves = 0
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

    def print_summary(self):
        diff = self.calculate_elo_diff()
        estimated_elo = self.benchmark_elo + diff
        total_games = sum(self.results.values())
        avg_moves = self.total_moves / total_games if total_games > 0 else 0

        summary = (
            f"\n=== Final Results ([{self.agent_name}] vs [{self.benchmark_name}]) ===\n"
            f"Wins: {self.results['win']}, Losses: {self.results['loss']}, Draws: {self.results['draw']}\n"
            f"Number of games: {total_games}\n"
            f"Average moves per game (plies): {avg_moves:.1f}\n"
            f"Score: {(self.results['win'] + 0.5 * self.results['draw']) / total_games:.3f}\n"
            f"Estimated Elo difference vs benchmark: {diff:.2f}\n"
            f"{self.agent_name} ≈ {estimated_elo:.0f} Elo (assuming {self.benchmark_name} is {self.benchmark_elo})\n"
        )

        print(summary)

        filename = f"./app/benchmarking/results/[{self.agent_name}]_vs_[{self.benchmark_name}]_results.txt"
        with open(filename, 'w') as f:
            f.write(summary)
