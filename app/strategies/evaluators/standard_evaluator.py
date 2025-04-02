from .abstract_evaluator import PositionEvaluator
import chess


class StandardEvaluator(PositionEvaluator):
    def evaluate(self, board: chess.Board) -> float:
        """
        Advanced board evaluation function considering:
        - Material balance
        - Pawn structure
        - King safety
        - Piece mobility
        """
        if board.is_game_over():
            print("End State Found")
            print("State Evaluation: ", super()._game_over_evaluation(board))
            return super()._game_over_evaluation(board)

        # Piece values (in centipawns) -> Very high king value to discincentivize losing King.
        piece_values = {
            chess.PAWN: 100,
            chess.KNIGHT: 300,
            chess.BISHOP: 350,
            chess.ROOK: 500,
            chess.QUEEN: 900,
            chess.KING: 10000,
        }

        side_values = {
            chess.WHITE: 1,
            chess.BLACK: -1,
        }
        
        # Initialize evaluation components
        material_balance = 0
        
        # Material Balance
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            
            if piece:
                value = piece_values[piece.piece_type] * side_values[piece.color]
                
                material_balance += value
        
        return material_balance

