""" import copy
import random
import math
import setup

class MiniMax():
    ""
    ""

    def __init__(self, game, depth, pruning=True):
        super().__init__(game, bot_type=MINIMAX, depth=depth, pruning=pruning)

    def drop_piece(self, position, row, col, piece):
        ""
        Drop a piece  at the specified position
        :param position: position with all the pieces that have been placed
        :param col: one of the row of the position
        :param col: one of the column of the position
        :param piece: 1 or -1 depending on whose turn it is
        ""
        position[col][row] = piece

    def winning_move(self, position, piece):
        ""
        ""

    def is_terminal_node(self, position):
        ""
        ""
        

    

    
 """

from player import *
import pion_classe 
from setup import *
from time import sleep

class Minimax_IA(Player_IA):  
    def choose_node_to_delete(self, ennemy_nodes_id_list):
        #Cette fonction va chercher à retirer les noeuds qui sont dans les coins.
        random_key = random.choice(ennemy_nodes_id_list)
        return random_key
    def choose_node_to_fill(self, free_nodes_id_list):
        #Cette fonction va optimiser le remplissage des noeuds.
        random_key = random.choice(free_nodes_id_list)
        return random_key
    def choose_node_to_move(self, game_state):
        accessible_nodes = game_state[0] #Attention type(accessible_nodes) = list
        ennemy_nodes = game_state[1] #Attention type(ennemy_nodes) = list

        
        #Cette fonction va optimiser le déplacement des pions.
        random_key = random.choice(accessible_nodes)
        return random_key
   
    def score_board(self, window,node_data,game_nodes):
        ""
        ""
        score = 0 
        score+=nb_pion_inline*100
        score+=nb_pion*10 
        score+=setup.get_possible_moves_nbr(node_data,game_nodes)

        return score   
    def minimax(self, position, depth, alpha, beta, maximizingPlayer, pruning,phase):
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
        if phase == 0:
            #Viser les noeuds 0-2-21-23
            return 0
        
        if phase == 1:
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

            for noeud_libre in position["neighbour"]:
                if (noeud_libre["color"] == BROWN):
                    b_copy = copy.deepcopy(noeud_libre)

                    self.drop_piece(b_copy, noeud, self._game._turn * turn)
                    new_score = self.minimax(
                        b_copy, depth - 1, alpha, beta, not maximizingPlayer, pruning
                    )[1]

                    if maximizingPlayer:
                        if new_score > value:
                            value = new_score
                        noeud = noeud_libre
                        alpha = max(alpha, value)
                    else:
                        if new_score < value:
                            value = new_score
                            noeud = noeud_libre
                        beta = min(beta, value)

                    if pruning:
                        if alpha >= beta:
                            break
                else: 
                    break
            return noeud, value
    
    def play_phase_0_IA(self):
        """
            Cette fonction fait en sorte que l'IA place un pion sur le plateau. Pour ce faire, on change 
                la couleur du noeud et du pion.
        """

        node_data = self.choose_random_node_IA()
        
        while (isinstance(node_data["piece"],pion_classe.Pion) and node_data["piece"].getColor() != BRWON):
            print(f". /{node_data['id']}")
            node_data = self.choose_random_node_IA()

        self.get_nodes_id()[node_data["id"]] = node_data["id"]
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
        self.game = game
        if(self.game.phase == 0):
            self.play_phase_0_IA()
            
        elif(self.game.phase == 1):
            self.play_phase_1_IA()