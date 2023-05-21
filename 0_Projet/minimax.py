from player import *
import pion_classe 
from setup import *
from time import sleep
import copy

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
   
    def score_board(self,  mode=1):
        """
        This function is used to compute the score of the board.
        There is 3 modes of computation different by the weigth given to selected board features:
        mode 1 give 100 to the number of pawns in line, 10 to the number of pawns and 1 to the number of possible moves
        mode 2 give more importance to the corners
        """
        # mode 1
        if mode == 1:
            score = 0
            for line in self.alligned_nodes:
                score += 100
            score += len(self.get_nodes_id()) 
            return score  
        # mode 2
        elif mode == 2:
            score = 0
            for line in game_state.alligned_nodes:
                if len(line) == 1:
                    score += 1
                elif len(line) == 2:
                    score += 10
                elif len(line) == 3:
                    score += 100
            score += len(game_state.get_nodes_id())
            score += len(game_state.accessible_nodes)
            return score
    def minimax(self, depth, alpha, beta, maximizingPlayer, pruning, phase, possibles_moves, mode, game):
        """
        This function is used to compute the best move for the AI.
        It uses the minimax algorithm with alpha-beta pruning.
        """
        if depth == 0 :
            print("#"*20)
            print("le score de min max est: ", self.score_board(mode))
            return None, self.score_board(mode)
        if maximizingPlayer:
            value = -math.inf
        else:
            value = math.inf
        
        for drop in possibles_moves:
            print("game address: ", id(game))
            print("dans le for de minimax")
            from gameClass import Game_copy
            cp_board = Game_copy(game)
            print("cp_board address: ", id(cp_board))
            #print couleur de tous les noeuds
            for node in cp_board.nodes.values():
                print(node["color"])
            for node in game.nodes.values():
                print(node["color"])
            # we have to make sure that both player one and two of the cpboard act as minimax_IA
            """ if not isinstance(cp_board.first_player, Minimax_IA):
                cp_board.first_player = Minimax_IA(0,RED,"RED",cp_board.first_player.get_pion_nbr())
            if not isinstance(cp_board.second_player, Minimax_IA):
                cp_board.second_player = Minimax_IA(1,BLUE,"BLUE",cp_board.second_player.get_pion_nbr()) """
            if phase == 0:
                cp_board.current_player().get_nodes_id()[drop["id"]] = drop["id"]
                cp_board.change_piece_color(drop)
                cp_board.decrement_player_pions()
                cp_board.accessible_nodes.remove(drop["id"])
                cp_board.is_there_winner(drop)
                cp_board.switch_player()
            elif phase == 1:
                pass #TODO
            elif phase == 2:
                pass #TODO
            # actualisations pour le prochain move 
            phase = cp_board.phase
            #print current player color
            print("current player color: ", cp_board.current_player().get_color())
            if phase == 0:
                print("dans le phase 0 apres drop")
                possibles_moves = cp_board.get_accessible_nodes_data()
                new_value = self.minimax(depth-1, alpha, beta, not maximizingPlayer, pruning, phase, possibles_moves, mode, cp_board)[1]
                print("out of recurive minmax")
                
            elif phase == 1:
                list_piece = cp_board.current_player_dict()
                for piece in list_piece:
                    for noeud_libre in piece["neighbour"]:
                        possibles_move = []
                        if (noeud_libre["color"] == BRWON):
                            possibles_move.append(noeud_libre)
                    new_value = self.minimax(depth-1, alpha, beta, not maximizingPlayer, pruning, phase, possibles_move, mode, cp_board)[1]

            if maximizingPlayer:
                if new_value > value:
                    value = new_value
                noeud = drop
                alpha = max(alpha, value)
            else:
                if new_value < value:
                    value = new_value
                noeud = drop
                beta = min(beta, value)

            if pruning:
                    if alpha >= beta:
                        break
            # print the cp_board address in memory
            print("end of for loop")
        print("out of for loop")
        return noeud, value
    
    def play_phase_0_IA(self):
        """
            Cette fonction fait en sorte que l'IA place un pion sur le plateau. Pour ce faire, on change 
                la couleur du noeud et du pion.
        """
        print("dans le play_phase_0_IA")
        possibles_moves = self.game.get_accessible_nodes_data()
        node_data = self.minimax(1, -math.inf, math.inf, True, True,0, possibles_moves, 1, self.game)[0]

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