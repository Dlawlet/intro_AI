from player import *
import pion_classe 
from setup import *
from time import sleep
import random
import math

class Minimax_IA(Player_IA):  
    def choose_node_to_delete(self, ennemy_nodes_id_list):
        # this function use the minimax algorithm to choose the best node to delete
        
        returned_key = None
        return returned_key
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
   
    def score_board(self, game, mode=1):
        """
        This function is used to compute the score of the board.
        There is 3 modes of computation different by the weigth given to selected board features:
        mode 1 give 100 to the number of pawns in line, 10 to the number of pawns and 1 to the number of possible moves
        mode 2 give more importance to the corners
        """
        # mode 1
        if mode == 1:
            score = 0
            score += len(game.current_player().alligned_nodes)*100
            score += len(list(game.current_player().get_nodes_id().keys()))*10
            score -= len(game.ennemy_player_alligned_nodes())*100
            if len(game.ennemy_player_alligned_nodes()) != 0:
                print("yoooooooooooooooooooooo")
                print("On test des trucs")
            score -= len(list(game.ennemy_player_dict().keys()))
        
            return score  
        # mode 2
        elif mode == 2:
            score = random.randint(0,100)
            return score
    def minimax(self, depth, alpha, beta, maximizingPlayer, pruning, phase, possibles_moves, mode, game):
        """
        This function is used to compute the best move for the AI.
        It uses the minimax algorithm with alpha-beta pruning.
        """
        if depth == 0 :
            print("#"*20)
            print("le score de min max est: ", self.score_board(game,mode))
            
            return None, self.score_board(game,mode)
        if maximizingPlayer:
            value = -math.inf
        else:
            value = math.inf
        for node_data in possibles_moves:
            from gameClass import Game_copy
            cp_board = Game_copy(game)
            cp_board.is_in_allignement(node_data)
            """ if depth == 0 :
                print("#"*20)
                print("le score de min max est: ", self.score_board(game,mode))
                
                return None, self.score_board(game,mode) """
            # we have to make sure that both player one and two of the cpboard act as minimax_IA
            """ if not isinstance(cp_board.first_player, Minimax_IA):
                cp_board.first_player = Minimax_IA(0,RED,"RED",cp_board.first_player.get_pion_nbr())
            if not isinstance(cp_board.second_player, Minimax_IA):
                cp_board.second_player = Minimax_IA(1,BLUE,"BLUE",cp_board.second_player.get_pion_nbr()) """
            if phase == 0:
                cp_board.current_player().add_node(node_data["id"])
                cp_board.change_piece_color(node_data)
                cp_board.decrement_player_pions()
                cp_board.accessible_nodes.remove(node_data["id"])
                cp_board.is_in_allignement(node_data)
                if depth == 0 :
                    print("#"*20)
                    print("le score de min max est: ", self.score_board(game,mode))
                    return None, self.score_board(game,mode)
                cp_board.switch_player()
                cp_board.is_in_allignement(node_data)
            if phase == 0:
                print("dans le phase 0 apres node_data")
                possibles_moves = cp_board.get_accessible_nodes_data()
                cp_board.is_in_allignement(node_data)
                new_value = self.minimax(depth-1, alpha, beta, not maximizingPlayer, pruning, phase, possibles_moves, mode, cp_board)[1]
                cp_board.is_in_allignement(node_data)
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
        cp_board.is_in_allignement(node_data)
        return noeud, value
    
    def play_phase_0_IA(self):
        """
            Cette fonction fait en sorte que l'IA place un pion sur le plateau. Pour ce faire, on change 
                la couleur du noeud et du pion.
        """
        print("dans le play_phase_0_IA")
        possibles_moves = self.game.get_accessible_nodes_data()
        node_data = self.minimax(5, -math.inf, math.inf, True, True,0, possibles_moves, 1, self.game)[0]

        self.get_nodes_id()[node_data["id"]] = node_data["id"]
        self.game.is_in_allignement(node_data)
        print(f'Le joueur {self.name} a sélectionné le noeud: {node_data["id"]} de couleur {self.game.translate_to_color(node_data["piece"].getColor())}')
        if node_data["piece"].getColor() == BRWON:
            self.game.change_piece_color(node_data)
            
            self.game.decrement_player_pions()
            self.game.accessible_nodes.remove(node_data["id"])
            self.game.is_there_winner(node_data)
            self.game.switch_player()
            
        else:
            print("Vous ne pouvez pas placer de pion ici")
        print("")
        print("hors du play_phase_0_IA")
    def play_phase_1_IA(self):
        didnt_play = True
        print(f"l'IA {self.name} va chercher deux noeuds à échanger")
        current_player_list_ID = list(self.get_nodes_id().keys())
        while(didnt_play):
            random_key = self.choose_random_node(current_player_list_ID)
            my_node = self.game.nodes[random_key]
            for neigbour_id in my_node["neighbours"]:
                if self.game.piece_can_switch(my_node,self.game.nodes[neigbour_id]):

                    self.game.temp_list.append(my_node)
                    self.game.temp_list.append(self.game.nodes[neigbour_id])
                    self.game.switch_pieces_nodes()

                    self.game.is_there_winner(self.game.nodes[neigbour_id])

                    
                    didnt_play = False
                    break #Otherwise we would continue to check on all neighbours!!!
            current_player_list_ID.pop(current_player_list_ID.index(random_key))
            if(len(current_player_list_ID) == 0):
                print(f"l'IA {self.name} n'a pas pu échanger deux noeuds")
                didnt_play = False
                self.game.game_over(self.game.ennemy_player_name())

                
        print(f"l'IA {self.name} a échangé deux noeuds")
        print("")
        self.game.switch_player()
    def play(self,game):
        """
            Cette fonction permet de jouer un tour, elle recoit en input le noeud sur lequel on a cliqué.
            Elle est appelée dans la fonction run().
            Elle permet de gérer les deux phases du jeu:
                - Phase 0: Placement des pions
                - Phase 1: Echange des pions
        """
        print(f"l'IA va jouer")
        self.game = game
        
        if(self.game.phase == 0):
            print(f"l'IA est dans la phase 0")
            self.play_phase_0_IA()
            
        elif(self.game.phase == 1):
            self.play_phase_1_IA()