"""File to test the different strategies, 
minimax and alpha beta pruning.
"""
from game import Player, TwoPlayerGameState, TwoPlayerMatch
from tictactoe import TicTacToe
from heuristic import heuristic
from strategy import (
    MinimaxAlphaBetaStrategy,
    MinimaxStrategy,
    RandomStrategy,
)
import timeit
import numpy as np
import matplotlib.pyplot as plt

class Heuristic1():
    """Dummy heuristic for testing"""
    def get_name(self) -> str:
        return "dummy"

    def evaluate(self, state: TwoPlayerGameState) -> float:
        # Use an auxiliary function.
        return self.dummy(123)

    def dummy(self, n: int) -> int:
        return n + 4


# Instantiating the heuristic object
heuristic = Heuristic1()

# Creating the game state

# Players for testing. These are irrelevant,
# just to create the game state
player1 = Player(
    name='player 1',
    strategy=RandomStrategy(0),
    delay=0,
)

player2 = Player(
    name='player 2',
    strategy=RandomStrategy(0),
    delay=0,
)

# Initialize a tic-tac-toe game.
game = TicTacToe(
    player1=player1,
    player2=player2,
    dim_board=3,
)

initial_board = np.zeros((3, 3))
initial_player = player1

# Initialize a game state.
game_state = TwoPlayerGameState(
    game=game,
    board=initial_board,
    initial_player=initial_player,
)

# Lists to store the spent times
times = []
performance_comparison = []
names = ['Minimax', 'Alpha Beta Pruning']

for i in range(1, 5):
    # Strategies to be tested.
    minimax_test = MinimaxStrategy(heuristic, i, 0)
    alphabeta_test = MinimaxAlphaBetaStrategy(heuristic, i, 0)

    # Testing Minimax
    minimax_time = timeit.timeit(lambda: minimax_test.next_move(game_state, False), number=10)
    times.append(minimax_time)
    print('Minimax test. Depth: '+str(i)+', time spent: '+str(minimax_time))

    # Testing AlphaBeta
    alphabeta_time = timeit.timeit(lambda: alphabeta_test.next_move(game_state, False), number=10)
    times.append(alphabeta_time)
    print('Alpha beta pruning. Depth: '+str(i)+', time spent: '+str(alphabeta_time))

    performance = minimax_time/alphabeta_time
    print('Alpha beta pruning is '+str(performance)+' times faster at depth '+str(i)+'\n')
    performance_comparison.append(performance)

    # Plotting the data
    plt.bar(names, times)
    plt.ylabel('Time spent')
    plt.show()

    # Resetting resources
    plt.clf()
    times.clear()

# Plotting the performance during the previous tests
plt.plot(performance_comparison)
plt.ylabel('Alpha beta performance over minimax')
plt.show()

