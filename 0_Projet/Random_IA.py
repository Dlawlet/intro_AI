
from player import *
import pion_classe 
from setup import *
from time import sleep

class Random_IA(Player_IA):
    def choose_random_node(self,nodes_id_list):
        """
            Cette fonction permet de choisir un noeud aléatoire sur le plateau. Pour ce faire, on génère 
                un nombre aléatoire entre 0 et le nombre de noeuds sur le plateau. On retourne ensuite 
                le noeud correspondant à ce nombre.
        """
        random_key = random.choice(nodes_id_list)
        return random_key
    
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

    def choose_random_node_IA(self):
            """
                Cette fonction permet de choisir un noeud aléatoire sur le plateau. Pour ce faire, on génère 
                    un nombre aléatoire entre 0 et le nombre de noeuds sur le plateau. On retourne ensuite 
                    le noeud correspondant à ce nombre.
            """

            list_of_keys = list(self.game.nodes.keys())
            random_key = self.choose_random_node(list_of_keys)
            ###random_key = self.current_player().choose_node_to_move(self.give_current_game_state())
            
            my_node = self.game.nodes[random_key]
            return my_node
        
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