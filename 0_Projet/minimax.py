from player import *
import pion_classe 
from setup import *
from time import sleep
import random
import math

class Minimax_IA(Player_IA):  
    def __init__(self, id, color, name, pion_nbr, mode=1):
        super().__init__(id, color, name, pion_nbr)
        self.mode = mode
    def choose_node_to_delete(self, ennemy_nodes_id_list):
        random_key = random.choice(ennemy_nodes_id_list)
        return random_key
    
    def choose_node_to_fill(self, free_nodes_id_list):
        # this function use the minimax algorithm to choose the best node to fill
        returned_key = (free_nodes_id_list)
        return returned_key
    def choose_node_to_move(self, game_state):
        accessible_nodes = game_state[0] #Attention type(accessible_nodes) = list
        ennemy_nodes = game_state[1] #Attention type(ennemy_nodes) = list

        
        #Cette fonction va optimiser le déplacement des pions.
        random_key = random.choice(accessible_nodes)
        return random_key
   
    def score_board(self, game,maximizingPlayer,mode=1):
        """
        This function is used to compute the score of the board.
        There is 3 modes of computation different by the weigth given to selected board features:
        mode 1 give 100 to the number of pawns in line, 10 to the number of pawns and 1 to the number of possible moves
        mode 2 give more importance to the corners
        """
        # mode 1
        if mode == 1:
            if not maximizingPlayer:
                score = 0
                score += len(game.current_player().alligned_nodes)*200
                score += len(list(game.current_player().get_nodes_id().keys()))*10
                score -= len(game.ennemy_player_alligned_nodes())*200
                score -= len(list(game.ennemy_player_dict().keys()))
            else:
                score = 0
                score -= len(game.current_player().alligned_nodes)*200
                score -= len(list(game.current_player().get_nodes_id().keys()))*10
                score += len(game.ennemy_player_alligned_nodes())*200
                score += len(list(game.ennemy_player_dict().keys()))
        
            return score  
        # mode 2
        elif mode == 2:
            if not maximizingPlayer:
                score = 0
                score += len(game.current_player().alligned_nodes)*50
                score += len(list(game.current_player().get_nodes_id().keys()))*10
                score -= len(game.ennemy_player_alligned_nodes())*200
                score -= len(list(game.ennemy_player_dict().keys()))
            else:
                score = 0
                score -= len(game.current_player().alligned_nodes)*50
                score -= len(list(game.current_player().get_nodes_id().keys()))*10
                score += len(game.ennemy_player_alligned_nodes())*200
                score += len(list(game.ennemy_player_dict().keys()))
            return score
        # mode 3
        elif mode == 3:
            if not maximizingPlayer:
                score = 0
                for id in game.current_player().get_nodes_id():
                    if id in [0, 2, 21, 23, 3, 5, 18, 20]:
                        score += 50
                score += len(game.current_player().alligned_nodes)*50
                score += len(list(game.current_player().get_nodes_id().keys()))*10
                score -= len(game.ennemy_player_alligned_nodes())*200
                score -= len(list(game.ennemy_player_dict().keys()))
            else:
                score = 0
                for id in game.current_player().get_nodes_id():
                    if id in [0, 2, 21, 23, 3, 5, 18, 20]:
                        score -= 50
                score -= len(game.current_player().alligned_nodes)*50
                score -= len(list(game.current_player().get_nodes_id().keys()))*10
                score += len(game.ennemy_player_alligned_nodes())*200
                score += len(list(game.ennemy_player_dict().keys()))
            return score
    def minimax(self, depth, alpha, beta, maximizingPlayer, pruning, phase, possibles_moves, mode, game):
        """
        This function is used to compute the best move for the AI.
        It uses the minimax algorithm with alpha-beta pruning.
        """
        if depth == 0 :
            print("#"*20)
            print("le score de min max est: ", self.score_board(game,maximizingPlayer,mode))
            return None, self.score_board(game,maximizingPlayer,mode)
            
        if maximizingPlayer:
            value = -math.inf
        else:
            value = math.inf
        for node_data in possibles_moves:
            from gameClass import Game_copy
            cp_board = Game_copy(game)
            if phase == 0:
                cp_board.current_player().add_node(node_data["id"])
                cp_board.change_piece_color(node_data)
                cp_board.decrement_player_pions()
                cp_board.accessible_nodes.remove(node_data["id"])
                if cp_board.is_in_allignement(node_data):
                    print("le noeud est dans un alignement")
                    print(f"la longueur de la liste des noeuds allignés de l'ennemi est: {len(cp_board.ennemy_player_alligned_nodes())}")
                    print(f"la longueur de la liste des noeuds allignés de l'ennemi est: {len(cp_board.current_player().alligned_nodes)}")
                    return node_data, self.score_board(game,maximizingPlayer,mode)
                cp_board.switch_player()   

            if phase == 0:
                possibles_moves = cp_board.get_accessible_nodes_data()
                new_value = self.minimax(depth-1, alpha, beta, not maximizingPlayer, pruning, phase, possibles_moves, mode, cp_board)[1]
                cp_board.reset_piece_color(node_data)
                cp_board.current_player().delete_node(node_data["id"])
               
                    
            if maximizingPlayer:
                if new_value > value:
                    value = new_value
                    noeud = node_data
                alpha = max(alpha, value)
            else:
                if new_value < value:
                    value = new_value
                    noeud = node_data
                beta = min(beta, value)

            if pruning:
                    if alpha >= beta:
                        break
            
        return noeud, value
    
    def play_phase_0_IA(self):
        """
            Cette fonction fait en sorte que l'IA place un pion sur le plateau. Pour ce faire, on change 
                la couleur du noeud et du pion.
        """
        possibles_moves = self.game.get_accessible_nodes_data()
        if self.game.accessible_nodes == [] or self.game.current_player().get_pion_nbr() == 0:
            self.game.game_over(self.game.current_player())
            return
        node_data = self.minimax(self.depth, -math.inf, math.inf, True, True,0, possibles_moves, self.mode, self.game)[0]
        self.game.reset_piece_color(node_data)
        self.game.current_player().delete_node(node_data["id"])
        self.get_nodes_id()[node_data["id"]] = node_data["id"]
        if node_data["piece"].getColor() == BRWON:
            self.game.change_piece_color(node_data)
            
            self.game.decrement_player_pions()
            self.game.accessible_nodes.remove(node_data["id"])
            self.game.is_there_winner(node_data)
            self.game.switch_player()
            
        else:
            print("Vous ne pouvez pas placer de pion ici")
    
    def play(self,game):
        """
            Cette fonction permet de jouer un tour, elle recoit en input le noeud sur lequel on a cliqué.
            Elle est appelée dans la fonction run().
            Elle permet de gérer les deux phases du jeu:
                - Phase 0: Placement des pions
                - Phase 1: Echange des pions
        """
        self.game = game
        self.depth = 2
        
        if(self.game.phase == 0):
            self.play_phase_0_IA()
