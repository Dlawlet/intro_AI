from player import *
import pion_classe
from setup import *
from time import sleep
import random

class Random_IA(Player_IA):
    def choose_random_node(self,nodes_id_list):
        """
        This function allows the AI to select a random node on the board. 
        It generates a random number between 0 and the number of nodes on the board. 
        It then returns the node corresponding to this number.
        """
        random_key = random.choice(nodes_id_list)
        return random_key
    
    def choose_node_to_delete(self, ennemy_nodes_id_list):
        # This function seeks to remove nodes that are in the corners.
        random_key = random.choice(ennemy_nodes_id_list)
        return random_key
    
    def choose_node_to_fill(self, free_nodes_id_list):
        # This function optimizes node filling.
        random_key = random.choice(free_nodes_id_list)
        return random_key
    
    def choose_node_to_move(self, game_state):
        # This function optimizes the movement of pieces.
        accessible_nodes = game_state[0] 
        ennemy_nodes = game_state[1]

        random_key = random.choice(accessible_nodes)
        return random_key

    def choose_random_node_IA(self):
        """
        This function allows the AI to select a random node on the board. 
        It generates a random number between 0 and the number of nodes on the board. 
        It then returns the node corresponding to this number.
        """
        list_of_keys = list(self.game.nodes.keys())
        random_key = self.choose_random_node(list_of_keys)
        my_node = self.game.nodes[random_key]
        return my_node
        
    def play_phase_0_IA(self):
        """
        This function allows the AI to place a piece on the board. 
        It changes the color of the node and the piece.
        """
        node_data = self.choose_random_node_IA()
        
        while (isinstance(node_data["piece"],pion_classe.Pion) and node_data["piece"].getColor() != BRWON):
            node_data = self.choose_random_node_IA()

        self.get_nodes_id()[node_data["id"]] = node_data["id"]
        if node_data["piece"].getColor() == BRWON:
            self.game.change_piece_color(node_data)
            self.game.decrement_player_pions()
            self.game.accessible_nodes.remove(node_data["id"])
            self.game.is_there_winner(node_data)
            self.game.switch_player()
            
    def play_phase_1_IA(self):
        didnt_play = True
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
                    break
            current_player_list_ID.pop(current_player_list_ID.index(random_key))
            if(len(current_player_list_ID) == 0):
                didnt_play = False
                self.game.game_over(self.game.ennemy_player_name())
                
        self.game.switch_player()
        
    def play(self, game):
        """
        This function allows to play a turn, it receives the node on which we clicked as input.
        It is called in the run() function.
        It allows to manage the two phases of the game:
            - Phase 0: Placing the pawns
            - Phase 1: Exchanging the pawns
        """
        self.game = game
        
        if self.game.phase == 0:
            self.play_phase_0_IA()  # call the function for phase 0
            
        elif self.game.phase == 1:
            self.play_phase_1_IA()  # call the function for phase 1
