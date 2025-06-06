import torch
import torch.nn as nn
from torch.utils.data import Dataset

class ChessDataset(Dataset):
    def __init__(self, X, y):
        self.X = torch.tensor(X, dtype=torch.float32)
        self.y = torch.tensor(y, dtype=torch.float32)

    def __len__(self):
        return len(self.X)

    def __getitem__(self, i):
        return self.X[i], self.y[i]
    
class ChessEvaluationNeuralNetwork(nn.Module):
    def __init__(self, input_size):
        super().__init__()
        self.model = nn.Sequential(
            nn.Linear(input_size, 256),
            nn.ReLU(),
            nn.Linear(256, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        return self.model(x)

class NeuralNetworkModel:
    _model = None
    _input_size = None

    @staticmethod
    def fen_to_feature_array(fen: str):
        game_attributes = fen.split()

        assert len(game_attributes) == 6

        board, turn, castling, en_passant, halfmove, fullmove = game_attributes

        piece_map = {
            'p': -100, 'n': -300, 'b': -325, 'r': -500, 'q': -900, 'k': -10000,
            'P': 100, 'N': 300, 'B': 325, 'R': 500, 'Q': 900, 'K': 10000
        }

        board_vector = []
        for row in board.split('/'):
            row_data = []
            for ch in row:
                if ch.isdigit():
                    row_data.extend([0] * int(ch))
                else:
                    row_data.append(piece_map[ch])
            board_vector.extend(row_data)

        turn_val = 0 if turn == 'w' else 1

        castling_vec = [int(c in castling) for c in 'KQkq']

        if en_passant != '-':
            file = ord(en_passant[0]) - ord('a')
            rank = int(en_passant[1]) - 1
            en_passant_val = rank * 8 + file
        else:
            en_passant_val = -1

        halfmove_val = int(halfmove)
        fullmove_val = int(fullmove)

        return board_vector + [turn_val] + castling_vec + [en_passant_val, halfmove_val, fullmove_val]
    
    @staticmethod
    def evaluate_fen(fen: str, model_path: str):
        if NeuralNetworkModel._model is None:
            print("Loading neural network model")
            features = NeuralNetworkModel.fen_to_feature_array(fen)
            input_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)
            NeuralNetworkModel._input_size = input_tensor.shape[1]

            model = ChessEvaluationNeuralNetwork(NeuralNetworkModel._input_size)
            model.load_state_dict(torch.load(model_path))
            model.eval()
            NeuralNetworkModel._model = model

        features = NeuralNetworkModel.fen_to_feature_array(fen)
        input_tensor = torch.tensor(features, dtype=torch.float32).unsqueeze(0)

        with torch.no_grad():
            prediction = NeuralNetworkModel._model(input_tensor)

        return prediction.item()
