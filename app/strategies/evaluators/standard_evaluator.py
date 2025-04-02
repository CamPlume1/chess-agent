from .abstract_evaluator import PositionEvaluator
import chess


class StandardEvaluator(PositionEvaluator):
    def evaluate(self, board: chess.Board, side: chess.Color) -> float:
        """
        Advanced board evaluation function considering:
        - Material balance
        - Pawn structure
        - King safety
        - Piece mobility
        """
        if board.is_game_over():
            return super()._game_over_evaluation(board, side)

        # Piece values (in centipawns) -> Very high king value to discincentivize losing King.
        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 300,
            chess.BISHOP: 350,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 10000,
        }
        
        # Initialize evaluation components
        material_balance = 0
        
        # Material Balance
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            
            if piece:
                value = piece_values[piece.piece_type]
                
                # Negative value for black pieces
                if piece.color != side:
                    value = -value
                
                material_balance += value

        
        return material_balance

