import torch
import numpy as np

# ============== Training  parameters ==============
G = 2  # Number of games between opponents in TOPP
M = 20  # Number of model versions to cache 
EPISODES = 20  # Number of episodes to train ANET for 
LEARNING_RATE = 0.05  # Learning rate | AlphaZero used: 0.0002
MCTS_ROUNDS = 2000  # MCTS rollout games | AlphaZero used: 800
MCTS_GAMES = 1  # Number of MCTS games to play | AlphaZero used: 44 000 000
TIME_LIMIT = 100  # Time limit for MCTS | AlphaZero used: 0.0040 seconds
BATCH_SIZE = 32  # Batch size for training | AlphaZero used: 700 000
NUM_EPOCHS = 10  # Number of epochs to train for
SIGMA = 0.001 # Sigma for how likely it is to predict the winner from value head

# ================= Hardwaresettings =================
DEVICE: torch.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# ====================== Paths =======================
MCTS_PERSONAL_DATA_FILE = "data_file.csv"  # Name of the file containing the data
MCTS_MAIN_DATA_FILE = "main_data_file.csv"  # Name of the file containing the data

MCTS_DATA_PATH = "./saved_mcts"# Path to the folder containing the data
MODEL_PATH = "./saved_models"# Path to the folder containing the models

# FILENAMES
PERSONAL_FILE_NAME = MCTS_DATA_PATH + "/" + MCTS_PERSONAL_DATA_FILE # Name of the file containing the data
MAIN_FILE_NAME = MCTS_DATA_PATH + "/" + MCTS_MAIN_DATA_FILE # Name of the file containing the data

# ====================== Replay Buffer =======================
REPLAY_BUFFER_MAX_SIZE = 25  # Size of the replay buffer

# ================== Chess Values ====================
MAX_TURNS = 100  # Max number of turns in a game

def get_all_possible_moves():
    """
    Returns a list of all possible moves in chess.
    """
    squares = np.array(["a1","a2","a3","a4","a5","a6","a7","a8",
                        "b1","b2","b3","b4","b5","b6","b7","b8",
                        "c1","c2","c3","c4","c5","c6","c7","c8",
                        "d1","d2","d3","d4","d5","d6","d7","d8",
                        "e1","e2","e3","e4","e5","e6","e7","e8",
                        "f1","f2","f3","f4","f5","f6","f7","f8",
                        "g1","g2","g3","g4","g5","g6","g7","g8",
                        "h1","h2","h3","h4","h5","h6","h7","h8"])

    allmoves = np.zeros((64, 64), dtype=object)
    for i in range(64):
        for j in range(64):
            if i != j:
                allmoves[i][j] = squares[i] + squares[j]

            # Remove diagonal elements entirely
    mask = np.eye(64, dtype=bool)
    allmoves = allmoves[~mask].reshape(64, 63)
    return allmoves.flatten()
ALL_POSSIBLE_MOVES = np.asarray(get_all_possible_moves())
GAME_START_STATE = "1.,-4.,-2.,-3.,-5.,-6.,-3.,-2.,-4.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,-1.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,0.,1.,1.,1.,1.,1.,1.,1.,1.,4.,2.,3.,5.,6.,3.,2.,4."

# ===================== Neural Network settings =====================
INPUT_SIZE = 8*8 + 1 # Input size
OUTPUT_SIZE = len(ALL_POSSIBLE_MOVES) # Output siz 63*64 

NUM_RESIDUAL_BLOCKS = 3 # Number of residual blocks in the neural network | Ph.D 3 | AlphaZero 20
NUM_FILTERS = 256 # Number of filters in the residual blocks 




# ============= Validate Training params =============
for i in range(EPISODES):
    try:
        (i % (EPISODES // (M - 1)) == 0 or (i == (EPISODES - 1)))
    except ZeroDivisionError as e:
        print("[ERROR] Number of episodes must be divisible by (M - 1) or (EPISODES - 1)")
        print("[HINT] Models must be lower than the number of episodes")
        print("[TERMINATING] Please change the value of EPISODES or M")
        exit()