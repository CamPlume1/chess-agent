import chess
from app.strategies.evaluators.abstract_evaluator import PositionEvaluator
from models.neural_network.neural_network import NeuralNetworkModel

class NeuralNetworkEvaluator(PositionEvaluator):
    def evaluate(self, board: chess.Board) -> float:
        if board.is_game_over():
            print("End State Found")
            print("State Evaluation: ", super()._game_over_evaluation(board))
            return super()._game_over_evaluation(board)
        
        return NeuralNetworkModel.evaluate_fen(board.fen(), "models/neural_network/neural_network.pth")