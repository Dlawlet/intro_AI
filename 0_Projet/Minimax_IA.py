from player import *
import pion_classe
from setup import *
from time import sleep
import random

class Minimax_IA(Player):

    def evaluate_board(self, game_state):
        # Evaluation function to assign a score to the game state
        # You can customize this function based on your strategy
        # and game-specific heuristics

        # Check if the current player has won
        if self.game.is_winner(self):
            return 100

        # Check if the opponent has won
        if self.game.is_winner(self.game.get_opponent(self)):
            return -100

        # Calculate the number of mills for the current player
        player_mills = self.game.get_num_mills(self)
        opponent_mills = self.game.get_num_mills(self.game.get_opponent(self))

        # Assign scores based on the number of mills and pieces
        score = (player_mills - opponent_mills) * 10 + (self.get_num_pieces() - self.game.get_opponent(self).get_num_pieces())
        return score

    def get_available_moves(self, game_state):
        # Retrieve a list of available moves from the current game state
        # You can implement the logic to generate all possible moves
        # based on the current positions of the pieces

        moves = []
        player_nodes = game_state[0]  # Accessible nodes for the current player

        # Generate all possible moves by iterating over the player's nodes
        for node_id in player_nodes:
            # Iterate over the adjacent nodes
            for adjacent_id in self.game.get_adjacent_nodes(node_id):
                # Check if the adjacent node is empty
                if self.game.is_empty_node(adjacent_id):
                    moves.append((node_id, adjacent_id))

        return moves

    def make_move(self, game_state, move):
        # Apply the move to the game state and return the new state
        node_id, adjacent_id = move
        new_state = game_state.copy()

        # Update the positions of the pieces
        new_state[0].remove(node_id)
        new_state[0].append(adjacent_id)

        return new_state

    def minimax(self, game_state, depth, maximizing_player):
        if depth == 0 or self.game.game_over():
            return self.evaluate_board(game_state)

        if maximizing_player:
            max_eval = float('-inf')
            for move in self.get_available_moves(game_state):
                new_state = self.make_move(game_state, move)
                eval = self.minimax(new_state, depth - 1, False)
                max_eval = max(max_eval, eval)
            return max_eval
        else:
            min_eval = float('inf')
            for move in self.get_available_moves(game_state):
                new_state = self.make_move(game_state, move)
                eval = self.minimax(new_state, depth - 1, True)
                min_eval = min(min_eval, eval)
            return min_eval

    def choose_best_move(self, game_state):
        best_score = float('-inf')
        best_move = None
        for move in self.get_available_moves(game_state):
            new_state = self.make_move(game_state, move)
            score = self.minimax(new_state, self.max_depth, False)
            if score > best_score:
                best_score = score
                best_move = move
        return best_move

    def play(self, game):
        self.game = game

        if self.game.phase == 0:
            # Implement logic for phase 0
            pass
        elif self.game.phase == 1:
            best_move = self.choose_best_move(self.game.get_current_state())
            # Apply the best move to the game state and perform the necessary actions
            self.make_move(self.game.get_current_state(), best_move)
            # Switch player and update the game phase if needed
