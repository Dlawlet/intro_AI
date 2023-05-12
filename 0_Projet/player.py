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
    
