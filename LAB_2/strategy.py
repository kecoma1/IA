"""Strategies for two player games.

   Authors:
        Fabiano Baroni <fabiano.baroni@uam.es>,
        Alejandro Bellogin <alejandro.bellogin@uam.es>
        Alberto Suárez <alberto.suarez@uam.es>
"""

from __future__ import annotations  # For Python 3.7

from abc import ABC, abstractmethod
from typing import List

import numpy as np

from game import TwoPlayerGame, TwoPlayerGameState
from heuristic import Heuristic


class Strategy(ABC):
    """Abstract base class for player's strategy."""

    def __init__(self, verbose: int = 0) -> None:
        """Initialize common attributes for all derived classes."""
        self.verbose = verbose

    @abstractmethod
    def next_move(
        self,
        state: TwoPlayerGameState,
        gui: bool = False,
    ) -> TwoPlayerGameState:
        """Compute next move."""

    def generate_successors(
        self,
        state: TwoPlayerGameState,
    ) -> List[TwoPlayerGameState]:
        """Generate state successors."""
        assert isinstance(state.game, TwoPlayerGame)
        successors = state.game.generate_successors(state)
        assert successors  # Error if list is empty
        return successors


class RandomStrategy(Strategy):
    """Strategy in which moves are selected uniformly at random."""

    def next_move(
        self,
        state: TwoPlayerGameState,
        gui: bool = False,
    ) -> TwoPlayerGameState:
        """Compute next move."""
        successors = self.generate_successors(state)
        return np.random.choice(successors)


class ManualStrategy(Strategy):
    """Strategy in which the player inputs a move."""

    def next_move(
        self,
        state: TwoPlayerGameState,
        gui: bool = False,
    ) -> TwoPlayerGameState:
        """Compute next move."""
        successors = self.generate_successors(state)

        assert isinstance(state.game, TwoPlayerGame)
        if gui:
            index_successor = state.game.graphical_input(state, successors)
        else:
            index_successor = state.game.manual_input(successors)

        next_state = successors[index_successor]

        if self.verbose > 0:
            print('My move is: {:s}'.format(str(next_state.move_code)))

        return next_state


class MinimaxStrategy(Strategy):
    """Minimax strategy."""

    def __init__(
        self,
        heuristic: Heuristic,
        max_depth_minimax: int,
        verbose: int = 0,
    ) -> None:
        """Initialize depth of the search & heuristic."""
        super().__init__(verbose)
        self.heuristic = heuristic
        self.max_depth_minimax = max_depth_minimax

    def next_move(
        self,
        state: TwoPlayerGameState,
        gui: bool = False,
    ) -> TwoPlayerGameState:
        """Compute next state in the game."""

        successors = self.generate_successors(state)

        minimax_value = -np.inf

        for successor in successors:
            if self.verbose > 1:
                print('{}: {}'.format(state.board, minimax_value))

            successor_minimax_value = self._min_value(
                successor,
                self.max_depth_minimax,
            )
            if (successor_minimax_value > minimax_value):
                minimax_value = successor_minimax_value
                next_state = successor

        if self.verbose > 0:
            if self.verbose > 1:
                print('\nGame state before move:\n')
                print(state.board)
                print()
            print('Minimax value = {:.2g}'.format(minimax_value))

        return next_state

    def _min_value(
        self,
        state: TwoPlayerGameState,
        depth: int,
    ) -> float:
        """Min step of the minimax algorithm."""
        if state.end_of_game or depth == 0:
            minimax_value = self.heuristic.evaluate(state)

        else:
            minimax_value = np.inf

            successors = self.generate_successors(state)
            for successor in successors:
                if self.verbose > 1:
                    print('{}: {}'.format(state.board, minimax_value))

                successor_minimax_value = self._max_value(
                    successor, depth - 1,
                )
                if (successor_minimax_value < minimax_value):
                    minimax_value = successor_minimax_value

        if self.verbose > 1:
            print('{}: {}'.format(state.board, minimax_value))

        return minimax_value

    def _max_value(
        self,
        state: TwoPlayerGameState,
        depth: int,
    ) -> float:
        """Max step of the minimax algorithm."""
        if state.end_of_game or depth == 0:
            minimax_value = self.heuristic.evaluate(state)

        else:
            minimax_value = -np.inf

            successors = self.generate_successors(state)
            for successor in successors:
                if self.verbose > 1:
                    print('{}: {}'.format(state.board, minimax_value))

                successor_minimax_value = self._min_value(
                    successor, depth - 1,
                )
                if (successor_minimax_value > minimax_value):
                    minimax_value = successor_minimax_value

        if self.verbose > 1:
            print('{}: {}'.format(state.board, minimax_value))

        return minimax_value


class MinimaxAlphaBetaStrategy(Strategy):
    """Minimax alpha-beta strategy."""

    def __init__(
        self,
        heuristic: Heuristic,
        max_depth_minimax: int,
        verbose: int = 0,
    ) -> None:
        super().__init__(verbose)
        self.heuristic = heuristic
        self.max_depth_minimax = max_depth_minimax

    def next_move(
        self,
        state: TwoPlayerGameState,
        gui: bool = False,
    ) -> TwoPlayerGameState:
        """Compute next state in the game."""
        successors = self.generate_successors(state)

        alpha = -np.inf
        beta = np.inf

        for successor in successors:
            if self.verbose > 1:
                print('{}: {}'.format(state.board, alpha))

            successor_alpha_beta_value = self._min_value(
                successor,
                alpha,
                beta,
                self.max_depth_minimax,
            )
            if (successor_alpha_beta_value > alpha):
                alpha = successor_alpha_beta_value
                next_state = successor

        if self.verbose > 0:
            if self.verbose > 1:
                print('\nGame state before move:\n')
                print(state.board)
                print()
            print('Alpha value = {:.2g}'.format(alpha))

        return next_state

    def _min_value(
        self,
        state: TwoPlayerGameState,
        alpha: float,
        beta: float,
        depth: int,
    ) -> float:
        """Min step of the alpha beta algorithm."""
        if state.end_of_game or depth == 0:
            phi = self.heuristic.evaluate(state)
        else:
            phi = np.inf

            successors = self.generate_successors(state)
            for successor in successors:
                if self.verbose > 1:
                    print('{}: {}'.format(state.board, phi))

                successor_alpha = self._max_value(
                    successor, alpha, beta, depth - 1
                )

                # Minimizing the max value
                if (successor_alpha < phi):
                    phi = successor_alpha

                # Pruning
                if phi <= alpha:
                    return phi

                beta = min(beta, phi)

        if self.verbose > 1:
            print('{}: {}'.format(state.board, beta))

        return phi

    def _max_value(
        self,
        state: TwoPlayerGameState,
        alpha: float,
        beta: float,
        depth: int,
    ) -> float:
        """Min step of the alpha beta algorithm."""
        if state.end_of_game or depth == 0:
            phi = self.heuristic.evaluate(state)
        else:
            phi = -np.inf

            successors = self.generate_successors(state)
            for successor in successors:
                if self.verbose > 1:
                    print('{}: {}'.format(state.board, phi))

                successor_beta = self._min_value(
                    successor, alpha, beta, depth - 1
                )

                # Maximizing the min value
                if (successor_beta > phi):
                    phi = successor_beta

                # Pruning
                if phi >= beta:
                    return phi

                alpha = max(alpha, phi)

        if self.verbose > 1:
            print('{}: {}'.format(state.board, beta))

        return phi
