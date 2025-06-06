import chess
from app.strategies.abstrategy import Strategy
from app.strategies.evaluators.abstract_evaluator import PositionEvaluator


class ABPruningStrategy(Strategy):
    # Depth must be greater than 1, or function will fail.
    def __init__(self, board: chess.Board, evaluator: PositionEvaluator, side=chess.WHITE, max_depth=3):
        super().__init__(board=board, side=side)
        self.evaluator = evaluator
        self.max_depth= max_depth
        self.seen : dict[str: int] = {} # Uses fen representation to track seen states

    def select_move(self):
        # Initialize parameter states
        best_move = None
        alpha = float('-inf')
        beta = float('inf')


        if self.side == chess.WHITE:
            _, best_move = self._a_b_maximizer(self.board, self.max_depth, alpha=alpha, beta=beta)

        else:
            _, best_move = self._a_b_minimizer(self.board, self.max_depth, alpha=alpha, beta=beta)


        return best_move

    def _a_b_maximizer(self, board: chess.Board, depth: int, alpha: float, beta: float):
        if depth == 0 or board.is_game_over():
            return self.evaluator.evaluate(board), None
        
        best_value = float('-inf')
        moves = board.legal_moves
        best_move = None
        for move in moves:
            board.push(move) 
            score, _ = self._a_b_minimizer(board, depth-1, alpha, beta)
            board.pop()
            if score > best_value:
                best_value = score
                best_move = move
                if score > alpha:
                    alpha = score
            if score >= beta:
                # print("Prune with remaining depth: ", depth - 1)
                return score, best_move
        return best_value, best_move

    def _a_b_minimizer(self, board: chess.Board, depth, alpha, beta):
        if depth == 0 or board.is_game_over():
            return self.evaluator.evaluate(board), None
        best_value = float('inf')
        moves = board.legal_moves
        best_move = None
        for move in moves:
            board.push(move)
            score, _ = self._a_b_maximizer(board, depth-1, alpha, beta)
            board.pop()
            if (score < best_value):
                best_value = score
                best_move = move
                if score < beta:
                    beta = score
            if score <= alpha:
                # print("Prune with remaining depth: ", depth - 1)
                return score, best_move
        return best_value, best_move
