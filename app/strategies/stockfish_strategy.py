import chess
import chess.engine
from chess import WHITE, Board, Color
from app.strategies.abstrategy import Strategy


class StockfishStrategy(Strategy):
    def __init__(
        self,
        board: Board = None,
        side: Color = WHITE,
        stockfish_path: str = "/usr/local/bin/stockfish",
        skill_level: int = 5,
        uci_elo: int = 1600,
        move_time: float = 0.1
    ):
        super().__init__(board=board, side=side)
        self.stockfish_path = stockfish_path
        self.skill_level = skill_level
        self.uci_elo = uci_elo
        self.move_time = move_time
        self._engine = None

    def _ensure_engine(self):
        if self._engine is None:
            self._engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)
            self._engine.configure({
                "Skill Level": self.skill_level,
                "UCI_LimitStrength": True,
                "UCI_Elo": self.uci_elo
            })

    def select_move(self):
        self._ensure_engine()
        result = self._engine.play(self.board, chess.engine.Limit(time=self.move_time))
        return result.move

    def __del__(self):
        try:
            if self._engine is not None:
                self._engine.quit()
        except Exception:
            pass
