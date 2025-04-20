import numpy as np
import torch
import torch.nn as nn
from torch.utils.data import Dataset
import pandas as pd
import torch.nn.init as init


# Dataset helper class
class ChessDataset(Dataset):

    # X board, x meta already converted to tensors prior to init, as is Y
    def __init__(self, X, Y):
        self.X = X
        self.Y = Y

    def __len__(self):
        return len(self.Y)

    def __getitem__(self, i):
        board = self.X['board_vec'][i]
        meta = self.X['meta_vec'][i]
        label = self.Y[i]
        return board, meta, label

# The Vibe model
class ChessEvaluationConvolutionalNetwork(nn.Module):
    def __init__(self):
        super().__init__()

       # Process relative position of pieces
        # Process relative position of pieces
        self.conv_layers = nn.Sequential(
            nn.Conv2d(12, 18, kernel_size=3, padding=1),
            nn.LeakyReLU(negative_slope=0.01), 
            nn.Conv2d(18, 32, kernel_size=3, padding=1),
            nn.LeakyReLU(negative_slope=0.01),
            nn.Flatten(),
            nn.Linear(2048, 256)
        )

        # Processes who's turn, castling ability, and en passant target squares
        self.metadata_layers = nn.Sequential(
            nn.Linear(5, 16),
            nn.LeakyReLU(negative_slope=0.01),
            nn.LayerNorm(16)
        )

        self.combined_layers = nn.Sequential(
            nn.Linear(272, 32),
            nn.LeakyReLU(negative_slope=0.01), 
            nn.Linear(32, 1)
        )

    def forward(self, x_board, x_meta):
        x_board = self.conv_layers(x_board)
        x_meta = self.metadata_layers(x_meta)
        output = self.combined_layers(torch.cat((x_board, x_meta), dim=1))
        return output

# This class handles operations regarding converting board representations to acceptable inputs to the convolutional network
class ConvolutionInputModel:

    _model = None


    # Outputs a 12 * 8 * 8 vector with the board, and 4 meta features [turn, w_castle, black castle, en_passant_target_square]
    @staticmethod
    def fen_to_feature_array(fen: str):

        # Piece encodings. Lowercase = black, n = knight
        PIECES_TO_CHANNEL = {
            'P': 0, 'N': 1, 'B': 2, 'R': 3, 'Q': 4, 'K': 5,
            'p': 6, 'n': 7, 'b': 8, 'r': 9, 'q': 10, 'k': 11
        }

        # Initialize empty 12×8×8 array (all zeros)
        board_features = np.zeros((12, 8, 8), dtype=np.float32)
        meta_features = np.zeros(5, dtype=np.float32)
        
        # Split FEN string to get board position (first part before space)
        fen_split = fen.split(' ')
        board = fen_split[0]
        turn = fen_split[1]
        castling = fen_split[2]
        
        # Split the board representation by ranks (rows)
        ranks = board.split('/')

        for rank_index, rank in enumerate(ranks):
            file_index = 0
            for char in rank:
                if char.isdigit():
                    file_index += int(char)
                else:
                    channel = PIECES_TO_CHANNEL[char]
                    board_features[channel, rank_index, file_index] = 1
                    file_index += 1

        # Encode turn, 0 for white
        meta_features[0] = 0 if turn == 'w' else 1
        
        # Encode castling info
        meta_features[1] = 1 if 'K' in castling else 0  
        meta_features[2] = 1 if 'k' in castling else 0 
        meta_features[3] = 1 if 'Q' in castling else 0
        meta_features[4] = 1 if 'q' in castling else 0

        return torch.from_numpy(board_features).unsqueeze(0), torch.from_numpy(meta_features).unsqueeze(0)

        
      
    # TODO: use a saved model to print the output of a usage of this function
    @staticmethod
    def evaluate_fen(fen: str, model_path: str):
        if ConvolutionInputModel._model is None:
            print("Loading convolutional model")
            model = ChessEvaluationConvolutionalNetwork()
            model.load_state_dict(torch.load(model_path))
            model.eval()
            ConvolutionInputModel._model = model

        board_features, meta_features = ConvolutionInputModel.fen_to_feature_array(fen)

        with torch.no_grad():
            prediction = ConvolutionInputModel._model(board_features, meta_features)

        return prediction.item()
    


# # Example usage: evaluating a FEN string on a saved model 
# fen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1'  # Example FEN
# model_path = 'convolutional_network.pth'  # Path to the saved model

# # Evaluating the FEN using CPU or GPU-> Just gives NAN
# device = 'cuda' if torch.cuda.is_available() else 'cpu'
# evaluation_result = ConvolutionInputModel.evaluate_fen(fen, model_path, device)
# print(f"Model evaluation result: {evaluation_result}")

    


    
