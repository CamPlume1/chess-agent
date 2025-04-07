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
        
        score = 0
        score += self._material_balance(board)
        score += self._pawn_structure_rewards(board)
        score += self._king_safety_rewards(board)
        score += self._piece_positioning_reward(board)
        return score
    


    def _material_balance(self, board: chess.Board):
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
                value = piece_values[piece.piece_type]
                
                # Negative value for black pieces
                if piece.color != chess.WHITE:
                    value = -value
                
                material_balance += value
        return material_balance
    


    def _pawn_structure_rewards(self, board: chess.Board) -> float:
        """
        Reward passed pawns and penalize doubled or isolated pawns.
        (Note: These heuristics are simplified for illustration.)
        """
        reward = 0

        # Loop over all pawns on board.
        for square, piece in board.piece_map().items():
            if piece.piece_type == chess.PAWN:
                # For white pawns, bonus if passed; for black, penalty.
                if piece.color == chess.WHITE:
                    if self._is_passed_pawn(board, square, chess.WHITE):
                        reward += 50
                else:
                    if self._is_passed_pawn(board, square, chess.BLACK):
                        reward -= 50
        return reward

    def _is_passed_pawn(self, board: chess.Board, square: int, color: bool) -> bool:
        """
        A simple check: a pawn is passed if there are no opposing pawns
        in the same or adjacent files in front of it.
        """
        file = chess.square_file(square)
        rank = chess.square_rank(square)
        direction = 1 if color == chess.WHITE else -1

        # Files to check: same file and adjacent files.
        files_to_check = [file]
        if file - 1 >= 0:
            files_to_check.append(file - 1)
        if file + 1 <= 7:
            files_to_check.append(file + 1)

        # For each file, check all squares ahead of the pawn.
        for f in files_to_check:
            for r in range(rank + direction, 8 if color == chess.WHITE else -1, direction):
                sq = chess.square(f, r)
                opp_piece = board.piece_at(sq)
                if opp_piece and opp_piece.piece_type == chess.PAWN and opp_piece.color != color:
                    return False
        return True

    def _king_safety_rewards(self, board: chess.Board) -> float:
        """
        Reward having castling rights and penalize if the king remains uncastled
        and stuck in the center. The idea is that castling generally improves safety.
        """
        score = 0

        # White king safety:
        if board.has_kingside_castling_rights(chess.WHITE) or board.has_queenside_castling_rights(chess.WHITE):
            score += 30
        else:
            white_king_square = board.king(chess.WHITE)
            # Penalize if the white king is in a central square - Not a safe space traditionally
            if white_king_square in [chess.E1, chess.D1]:
                score -= 50

        # Black king safety:
        if board.has_kingside_castling_rights(chess.BLACK) or board.has_queenside_castling_rights(chess.BLACK):
            score -= 30
        else:
            black_king_square = board.king(chess.BLACK)
            if black_king_square in [chess.E8, chess.D8]:
                score += 50

        return score

    def _piece_positioning_reward(self, board: chess.Board) -> float:
        # Right now only includes knights, but will extend to other pieces to try and control the center
        score = 0

        knight_table = [
            [-50, -40, -30, -30, -30, -30, -40, -50],
            [-40, -20,   0,   0,   0,   0, -20, -40],
            [-30,   0,  10,  15,  15,  10,   0, -30],
            [-30,   5,  15,  20,  20,  15,   5, -30],
            [-30,   0,  15,  20,  20,  15,   0, -30],
            [-30,   5,  10,  15,  15,  10,   5, -30],
            [-40, -20,   0,   5,   5,   0, -20, -40],
            [-50, -40, -30, -30, -30, -30, -40, -50]
        ]

        for square, piece in board.piece_map().items():
            if piece.piece_type == chess.KNIGHT:
                rank = chess.square_rank(square)
                file = chess.square_file(square)
                if piece.color == chess.WHITE:
                    score += knight_table[rank][file]
                else:
                    # For black, flip the table vertically.
                    score -= knight_table[7 - rank][file]
        return score
