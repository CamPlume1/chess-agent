import chess
from app.strategies.evaluators.abstract_evaluator import PositionEvaluator
from models.cnn.cnn import ConvolutionInputModel

class ConvolutionalNetworkEvaluator(PositionEvaluator):
    def evaluate(self, board: chess.Board) -> float:
        if board.is_game_over():
            print("End State Found")
            print("State Evaluation: ", super()._game_over_evaluation(board))
            return super()._game_over_evaluation(board)
        
        return ConvolutionInputModel.evaluate_fen(board.fen(), "models/cnn/convolutional_network.pth")