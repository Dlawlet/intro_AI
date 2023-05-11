import random
import setup


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
    
class Player_IA(Player):
    def __init__(self, id, color, name, pion_nbr):
        super().__init__(id, color, name, pion_nbr)
    
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
