from game import (
    TwoPlayerGameState,
)

from tournament import (
    StudentHeuristic,
)

class MySolution1 (StudentHeuristic):

    def get_name (self) -> str:
        return "mysolution1"

    def evaluate(self, state: TwoPlayerGameState) -> float:
        return self.corners_and_walls_left(state)

    def corners_and_walls_left(self, state: TwoPlayerGameState) -> int:
        height = state.game.height
        width = state.game.width
        corners = ((1, 1), (1, height), (1, width), (height, width))

        # Each corners has a value of 4. A corner 
        # is more valuable than a wall
        total_walls_and_corners = 4*4 + height*2 + width*2

        for occupied in state.board:
            # If a corner is occupied we decrement
            if occupied in corners:
                total_walls_and_corners -= 4
            
            # If a wall is occupied we decrement
            if height in occupied or width in occupied:
                total_walls_and_corners -= 1
        
        return total_walls_and_corners


class MySolution2 (StudentHeuristic):

    def get_name (self) -> str:
        return "mysolution1"

    def evaluate(self, state: TwoPlayerGameState) -> float:
        return self.num_walls_left(state)

    def num_walls_left (self, state: TwoPlayerGameState) -> int:
        height = state.game.height
        width = state.game.width
        total_walls = height*2 + width*2

        # For each wall in the game, if it is 
        # occupied we decrement the value
        for occupied in state.board:
            if height in occupied or width in occupied:
                total_walls -= 1

        return total_walls


class MySolution3 (StudentHeuristic):

    def get_name (self) -> str:
        return "mysolution1"

    def evaluate(self, state: TwoPlayerGameState) -> float:
        return self.num_corners_left(state)

    def num_corners_left(self, state: TwoPlayerGameState) -> int:
        height = state.game.height
        width = state.game.width
        total_corners = 4
        corners = ((1, 1), (1, height), (1, width), (height, width))

        # For each corner in the game, if it is 
        # occupied we decrement the value
        for occupied in state.board:
            if occupied in corners: 
                total_corners -= 1

        return total_corners
