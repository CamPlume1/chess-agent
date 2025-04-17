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
                value = piece_values[piece.piece_type] * side_values[piece.color]
                
                material_balance += value
        return material_balance
    


    def _pawn_structure_rewards(self, board: chess.Board) -> float:
        reward = 0

        # Loop over all pawns on board.
        for square, piece in board.piece_map().items():
            if piece.piece_type == chess.PAWN:
                if piece.color == chess.WHITE:
                    if self._is_passed_pawn(board, square, chess.WHITE):
                        reward += 50
                else:
                    if self._is_passed_pawn(board, square, chess.BLACK):
                        reward -= 50
        return reward

    def _is_passed_pawn(self, board: chess.Board, square: int, color: bool) -> bool:
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
        # Reward castling, or at least preserving the possibility of castling
        score = 0

        # White king safety:
        if board.has_kingside_castling_rights(chess.WHITE) or board.has_queenside_castling_rights(chess.WHITE):
            score += 15
        else:
            white_king_square = board.king(chess.WHITE)
            # Penalize if the white king is in a central square - Not a safe space traditionally
            if white_king_square in [chess.E1, chess.D1, chess.E2, chess.D2, chess.C2, chess.F2]:
                score -= 35

        # Black king safety:
        if board.has_kingside_castling_rights(chess.BLACK) or board.has_queenside_castling_rights(chess.BLACK):
            score -= 15
        else:
            black_king_square = board.king(chess.BLACK)
            if black_king_square in [chess.E8, chess.D8, chess.E7, chess.D7, chess.F7, chess.C7]:
                score += 35

        return score

    def _piece_positioning_reward(self, board: chess.Board) -> float:
        # Positional bonuses for knights, pawns, and bishops. Uses a gradient matrix to incentivize certain positions, which should
        # help agent in early and middle games
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

        pawn_table = [
            [ 0,   0,   0,   0,   0,   0,   0,   0],
            [50,  50,  50,  50,  50,  50,  50,  50],
            [10,  10,  20,  30,  30,  20,  10,  10],
            [ 5,   5,  10,  25,  25,  10,   5,   5],
            [ 0,   0,   0,  20,  20,   0,   0,   0],
            [ 5,  -5, -10,   0,   0, -10,  -5,   5],
            [ 5,  10,  10, -20, -20,  10,  10,   5],
            [ 0,   0,   0,   0,   0,   0,   0,   0]
        ]

        bishop_table = [
            [-20, -10, -10, -10, -10, -10, -10, -20],
            [-10,   5,   0,   0,   0,   0,   5, -10],
            [-10,  10,  10,  10,  10,  10,  10, -10],
            [-10,   0,  10,  10,  10,  10,   0, -10],
            [-10,   5,   5,  10,  10,   5,   5, -10],
            [-10,   0,   5,  10,  10,   5,   0, -10],
            [-10,   0,   0,   0,   0,   0,   0, -10],
            [-20, -10, -10, -10, -10, -10, -10, -20]
        ]

        for square, piece in board.piece_map().items():
            rank = chess.square_rank(square)
            file = chess.square_file(square)
            table = None
            if piece.piece_type == chess.KNIGHT:
                table = knight_table
            elif piece.piece_type == chess.PAWN:
                table = pawn_table
            elif piece.piece_type == chess.BISHOP:
                table = bishop_table
            else:
                continue

            if piece.color == chess.WHITE:
                score += table[rank][file]
            else:
                score -= table[7 - rank][file]

        return score

