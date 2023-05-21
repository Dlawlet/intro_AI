import pion_classe  # Importing required modules
from setup import *
import copy
class Player():
    def __init__(self, id, color, name, pion_nbr):
        self.id = id
        self.color = color
        self.name = name
        self.pion_nbr = pion_nbr
        self.nodes_id = {}
        self.possible_moves = {}
        self.alligned_nodes = []

    def get_id(self):
        return self.id

    def get_color(self):
        return self.color

    def get_name(self):
        return self.name

    def get_pion_nbr(self):
        return self.pion_nbr

    def get_nodes_id(self):
        return self.nodes_id
    
    def add_line(self, line):
        self.alligned_nodes.append(line)
    
    def delete_line(self, node):
        # We have to find the node in the list. If it's in the list, we delete it.
        for line in self.alligned_nodes:
            if node in line:
                self.alligned_nodes.remove(line)
    
    def choose_node_to_delete(self, ennemy_nodes_id_list):
        # Implement this method as per requirements
        key = None
        return key
    
    def decrement_pion_nbr(self):
        self.pion_nbr -= 1

    def create_copy(self):
        copyu = Player(self.id, self.color, self.name, self.pion_nbr)
        copyu.nodes_id = copy.deepcopy(self.nodes_id)
        copyu.possible_moves = copy.deepcopy(self.possible_moves)
        copyu.alligned_nodes = copy.deepcopy(self.alligned_nodes)
        return copyu
    
class Player_IA(Player):
    def __init__(self, id, color, name, pion_nbr):
        super().__init__(id, color, name, pion_nbr)
class Human(Player):
    def choose_node_to_delete(self, ennemy_nodes_id_list):
        # Implement this method as per requirements
        key = None
        while key not in ennemy_nodes_id_list:
            node_data = None
            while node_data is None:
                node_data = self.game.playing_event_handler()
            key = node_data["id"]
        return key

    def play_phase_0_Human(self, node_data):
        """
            This function allows the player to place the pawns on the board.
            To do this, we change the color of the node and pawn.
            We return the node_data so that it can be used in the play_the_turn() function.
            If we return None, it is not a problem as we do not use it in the play_the_turn() function
            and handle the case where we return None in the play_the_turn() function.
        """
        if isinstance(node_data["piece"], pion_classe.Pion) and node_data["piece"].getColor() == BRWON:
            self.get_nodes_id()[node_data["id"]] = node_data["id"]
            self.game.change_piece_color(node_data=node_data)
            self.game.decrement_player_pions()
            self.game.accessible_nodes.remove(node_data["id"])
            self.game.is_there_winner(node_data)
            self.game.switch_player()

    def play_phase_1_Human(self, node_data):
        """
        This function is used to move the pawns on the board. To do this, we exchange the pawns of two nodes if and only if 
        the two nodes are adjacent and one of the nodes is empty.
        """
        if len(self.game.temp_list) == 0:
            if isinstance(node_data["piece"], pion_classe.Pion) and node_data["piece"].getColor() == BRWON:
                print("Please select a FIRST pawn that already has a color.")
            else:
                self.game.temp_list.append(node_data)
                print("You have selected the pawn", node_data["id"])
            return None
        else:
            if len(self.game.temp_list) == 1 and self.game.temp_list[0]["id"] != node_data["id"]:
                self.game.temp_list.append(node_data)
                if self.game.check_if_nodes_are_adjacent(self.game.temp_list[0], self.game.temp_list[1]):
                    self.game.switch_pieces_nodes()
                    self.game.is_there_winner(node_data)
                    self.game.switch_player()
                else:
                    print("You cannot exchange these pawns because they are not adjacent.")
            else:
                print("You cannot exchange these pawns because they are identical.")
            
            self.game.temp_list = [] # As soon as an error is made, we empty the temporary list
    
    def play(self, game):
        """
        This function allows you to play a turn, it receives the node on which we clicked as input. 
        It is called in the run() function. It allows to manage the two phases of the game:
            - Phase 0: Placement of pawns
            - Phase 1: Exchange of pawns
        """
        self.game = game
        node_data = None
        while node_data is None:
            node_data = self.game.playing_event_handler()

        if self.game.phase == 0:
            self.play_phase_0_Human(node_data=node_data)
        elif self.game.phase == 1:
            self.play_phase_1_Human(node_data=node_data)
        
        # Implement this method as per requirements
        key = None
        return key