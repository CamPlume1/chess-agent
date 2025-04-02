import chess
from app.strategies.abstrategy import Strategy
from app.strategies.evaluators.abstract_evaluator import PositionEvaluator

class ABPruningStrategy(Strategy):
    def __init__(self, board: chess.Board, evaluator: PositionEvaluator, side=chess.WHITE, max_depth=5):
        super().__init__(side=side)
        self.evaluator = evaluator
        self.board = board
        self.max_depth= max_depth
        self.seen : dict[str: int] = {} # Uses fen representation to track seen states

    def select_move(self):
        # Get list of valid moves
        valid_moves = self.board.legal_moves

        # Initialize parameter states
        best_move = None
        best_value = float('-inf')
        alpha = float('-inf')
        beta = float('inf')


        for move in valid_moves:
            # Make a copy of the board for simulation
            board_copy = self.board.copy()
            
            # Make the move
            board_copy.push(move)
            
            # Calculate the value of this move
            value = -self._alpha_beta(board_copy, self.max_depth - 1, -beta, -alpha, self._opposing_side(self.side))
            
            # Update best move if found
            if value > best_value:
                print(f"Replacing best move value {best_value} with new value{value}")
                best_value = value
                best_move = move
            
            # Update alpha
            alpha = max(alpha, value)

        print(f"Selected move with value: {best_value}")
        return best_move

    def _alpha_beta(self, board_copy: chess.Board, depth: int, beta: float, alpha: float, side: chess.Color):
        # Create a unique key for the board position
        board_key = board_copy.fen()
        
        # Check if we've seen this position before
        if board_key in self.seen:
            return self.seen[board_key]
        
        # Check for terminal condition
        if depth == 0 or not board_copy.legal_moves:
            evaluation = self.evaluator.evaluate(board_copy, side)
            self.seen[board_key] = evaluation
            return evaluation
        
        if side == self.side:  # Maximizing player
            value = float('-inf')
            for move in board_copy.legal_moves:
                move_board = board_copy.copy()
                move_board.push(move)
                value = max(value, self._alpha_beta(move_board, depth - 1, alpha, beta, self._opposing_side(side)))
                alpha = max(alpha, value)
                if alpha >= beta:
                    break  # Beta cut-off
            
            self.seen[board_key] = value
            return value
        
        else:  # Minimizing player
            value = float('inf')
            for move in board_copy.legal_moves:
                move_board = board_copy.copy()
                move_board.push(move)
                value = min(value, self._alpha_beta(move_board, depth - 1, alpha, beta, self._opposing_side(side)))
                beta = min(beta, value)
                if alpha >= beta:
                    break  # Alpha cut-off
            
            self.seen[board_key] = value
            return value

    # Get opposite side easily
    def _opposing_side(self, side):
        return chess.BLACK if side == chess.WHITE else chess.WHITE
    
