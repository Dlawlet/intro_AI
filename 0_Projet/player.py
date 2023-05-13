import random
from setup import *
import pion_classe


class Player():
    def __init__(self,id, color, name, pion_nbr):
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
    
    def decrement_pion_nbr(self):
        self.pion_nbr -= 1

    def add_line(self, line):
        self.alligned_nodes.append(line)
    def delete_line(self,node):
        #We have to find the node in the list. If it's in the list, we delete it.
        for line in self.alligned_nodes:
            if node in line:
                print("Suppresion of the line : ", line, " in the list of alligned nodes")
                self.alligned_nodes.remove(line)
    
    def choose_node_to_delete(self, ennemy_nodes_id_list):
        key = None
        return key
class Player_IA(Player):
    def __init__(self, id, color, name, pion_nbr):
        super().__init__(id, color, name, pion_nbr)
    
class Human(Player):
    def choose_node_to_delete(self, ennemy_nodes_id_list):
        key = None
        while key not in ennemy_nodes_id_list:
                node_data = None
                while node_data == None:
                    node_data = self.game.playing_event_handler()
                key = node_data["id"]
        return key
    def play_phase_0_Human(self,node_data):
            """
                Rien de compliqué. Cette fonction permet de placer les pions sur le plateau.
                    Pour ce faire, on change la couleur du noeud et du pion.
                On return le node_data pour pouvoir le utiliser dans la fonction play_the_turn().
                    Ce n'est pas grâve si on return None car on ne l'utilise pas dans la fonction play_the_turn()
                    et qu'on traite le cas où on return None dans la fonction play_the_turn().
            """
            #print("Phase 0, on place les pions")
            if isinstance(node_data["piece"],pion_classe.Pion) and node_data["piece"].getColor() == BRWON:
                print(f'Voici le noeud sélectionné: {node_data["id"]}')
                self.get_nodes_id()[node_data["id"]] = node_data["id"]
                self.game.change_piece_color(node_data=node_data)
                self.game.decrement_player_pions()
                self.game.accessible_nodes.remove(node_data["id"])
                self.game.is_there_winner(node_data)
                self.game.switch_player()
                print("")

                
            else:
                print("Vous ne pouvez pas placer de pion ici")
    def play_phase_1_Human(self,node_data):
        """
            Un peu plus compliqué. Cette fonction permet de déplacer les pions sur le plateau.
                Pour ce faire, on échange les pions de deux noeuds si et seulement si les deux noeuds
                sont adjacents et que l'un des deux noeuds est vide.
        """
        
        #print("Phase 1, on déplace les pions")
        if len(self.game.temp_list)==0:
            if isinstance(node_data["piece"],pion_classe.Pion) and node_data["piece"].getColor() == BRWON:
                print("Veulliez sélectionner un PREMIER pion aillant déja une couleur")
            else:
                self.game.temp_list.append(node_data)
                print("Vous avez sélectionné le pion", node_data["id"])
            return None
        else:
            if len(self.game.temp_list)==1 and self.game.temp_list[0]["id"] != node_data["id"]:
                self.game.temp_list.append(node_data)
                if self.game.check_if_nodes_are_adjacent(self.game.temp_list[0],self.game.temp_list[1]):
                    self.game.switch_pieces_nodes()
                    self.game.is_there_winner(node_data)
                    self.game.switch_player()
                    
                else:
                    print("Vous ne pouvez pas échanger ces pions car ils ne sont pas adjacents")
            else:
                print("Vous ne pouvez pas échanger ces pions car ils sont identiques")
            
            self.game.temp_list = [] #Dès qu'une erreur est faite, on vide la liste temporaire
    def play(self,game):
        """
            Cette fonction permet de jouer un tour, elle recoit en input le noeud sur lequel on a cliqué.
            Elle est appelée dans la fonction run().
            Elle permet de gérer les deux phases du jeu:
                - Phase 0: Placement des pions
                - Phase 1: Echange des pions
        """
        self.game = game
        node_data = None
        while node_data == None:
            node_data = self.game.playing_event_handler()

        if(self.game.phase == 0):
            self.play_phase_0_Human(node_data=node_data)
        elif (self.game.phase==1):
            self.play_phase_1_Human(node_data=node_data)
