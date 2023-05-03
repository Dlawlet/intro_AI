from bot import Bot
import copy
from common import MINIMAX, EMPTY, ROW_COUNT, COLUMN_COUNT, WINDOW_LENGTH
import random
import math


class MiniMax(Bot):
    """
    """

    def __init__(self, game, depth, pruning=True):
        super().__init__(game, bot_type=MINIMAX, depth=depth, pruning=pruning)

    def drop_piece(self, position, row, col, piece):
        """
        Drop a piece  at the specified position
        :param position: position with all the pieces that have been placed
        :param col: one of the row of the position
        :param col: one of the column of the position
        :param piece: 1 or -1 depending on whose turn it is
        """
        position[col][row] = piece

    def winning_move(self, position, piece):
        """
        """

    def is_terminal_node(self, position):
        """
        """
        

    def score_board(self, window, piece):
        """
        """
        score = 0 
        score+=nb_pion_inline*100
        score+=nb_pion*10 
        score+=nb_deplacemnt_possible

        return score

    def minimax(self, position, depth, alpha, beta, maximizingPlayer, pruning):
        """
        Main function of minimax, called whenever a move is needed.
        Recursive function, depth of the recursion being determined by the parameter depth.
        :param depth: number of iterations the Minimax algorith will run for
            (the larger the depth the longer the algorithm takes)
        :alpha: used for the pruning, correspond to the lowest value of the range values of the node
        :beta: used for the pruning, correspond to the hihest value of the range values of the node
        :maximizingPlayer: boolean to specify if the algorithm should maximize or minimize the reward
        :pruning: boolean to specify if the algorithm uses the pruning
        :return: column where to place the piece
        """
        valid_locations = self.get_valid_locations(position)
        is_terminal = self.is_terminal_node(position)

        if depth == 0:
            return (None, self.score_position(position, self._game._turn))
        elif is_terminal:
            if self.winning_move(position, self._game._turn):
                return (None, math.inf)
            elif self.winning_move(position, self._game._turn * -1):
                return (None, -math.inf)
            else:  # Game is over, no more valid moves
                return (None, 0)


        if maximizingPlayer:
            value = -math.inf
            turn = 1
        else:
            value = math.inf
            turn = -1

        for position in noeud_vides:
            if (chech_if_noeud_is_neighbour(position)):
                b_copy = copy.deepcopy(position)

                self.drop_piece(b_copy, noeud, self._game._turn * turn)
                new_score = self.minimax(
                    b_copy, depth - 1, alpha, beta, not maximizingPlayer, pruning
                )[1]

                if maximizingPlayer:
                    if new_score > value:
                        value = new_score
                       noeud = position
                    alpha = max(alpha, value)
                else:
                    if new_score < value:
                        value = new_score
                        noeud = position
                    beta = min(beta, value)

                if pruning:
                    if alpha >= beta:
                        break
            else: 
                break
        return noeud, value
