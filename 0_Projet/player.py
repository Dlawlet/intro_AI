import random

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