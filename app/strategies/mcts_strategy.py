import chess
import math
import random
from typing import List
from app.strategies.evaluators.abstract_evaluator import PositionEvaluator
from app.strategies.abstrategy import Strategy

class MCTSNode:
    def __init__(self, board: chess.Board, parent: 'MCTSNode' = None, move: chess.Move = None):
        self.board = board
        self.parent = parent
        self.move = move
        self.children: List[MCTSNode] = []
        self.visits = 0
        self.value = 0.0
        self.untried_moves = list(board.legal_moves)

    def is_fully_expanded(self):
        return len(self.untried_moves) == 0

    def best_child(self):
        return max(
            self.children,
            key=lambda child: (child.value / child.visits) + math.sqrt(2 * math.log(self.visits) / child.visits)
        )

    def expand(self):
        move = self.untried_moves.pop()
        new_board = self.board.copy()
        new_board.push(move)
        child_node = MCTSNode(new_board, parent=self, move=move)
        self.children.append(child_node)
        return child_node

    def backpropagate(self, value):
        self.visits += 1
        self.value += value
        if self.parent:
            self.parent.backpropagate(-value)

class MCTSStrategy(Strategy):
    def __init__(self, board: chess.Board, evaluator: PositionEvaluator, side: bool, simulations=1000):
        super().__init__(board=board, side=side)
        self.evaluator = evaluator
        self.simulations = simulations

    def select_move(self):
        root = MCTSNode(self.board)

        for _ in range(self.simulations):
            node = root
            while node.is_fully_expanded() and node.children:
                node = node.best_child()

            if not node.is_fully_expanded():
                node = node.expand()

            value = self._evaluate_leaf(node.board)

            node.backpropagate(value)

        best_move = max(root.children, key=lambda child: child.visits)


        return best_move.move

    def _evaluate_leaf(self, board: chess.Board, rollout_depth=4) -> float:
        sim_board = board.copy()
        moves_played = 0

        while not sim_board.is_game_over() and moves_played < rollout_depth:
            legal_moves = list(sim_board.legal_moves)
            if not legal_moves:
                break
            move = random.choice(legal_moves)
            sim_board.push(move)
            moves_played += 1

        score = self.evaluator.evaluate(sim_board)
        return score if self.side == chess.WHITE else -score
