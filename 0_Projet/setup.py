import pion_classe
import pygame
import time
import math


# Define colors
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BRWON = (139,69,19)
def setup_screen():
    # Set up the game window
    screen_width = 425
    screen_height = 400
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("My Game")

    return screen
def are_good_neighbor(current_node_ID,neighbor_node_ID):
    res = True
    #first line
    if current_node_ID == 0:
        if neighbor_node_ID not in [1,9]:
            res = False
    elif current_node_ID == 1:
        if neighbor_node_ID not in [0,2,4]:
            res = False
    elif current_node_ID == 2:
        if neighbor_node_ID not in [1,14]:
            res = False

    #second line
    elif current_node_ID == 3:
        if neighbor_node_ID not in [4,10]:
            res = False
    elif current_node_ID == 4:
        if neighbor_node_ID not in [1,3,5,7]:
            res = False
    elif current_node_ID == 5:
        if neighbor_node_ID not in [4,13]:
            res = False

    #third line
    elif current_node_ID == 6:
        if neighbor_node_ID not in [7,11]:
            res = False
    elif current_node_ID == 7:
        if neighbor_node_ID not in [4,6,8]:
            res = False
    elif current_node_ID == 8:
        if neighbor_node_ID not in [7,12]:
            res = False

    #fourth line
    elif current_node_ID == 9:
        if neighbor_node_ID not in [0,10,21]:
            res = False
    elif current_node_ID == 10:
        if neighbor_node_ID not in [3,9,11,18]:
            res = False
    elif current_node_ID == 11:
        if neighbor_node_ID not in [6,10,15]:
            res = False
    elif current_node_ID == 12:
        if neighbor_node_ID not in [8,13,17]:
            res = False
    elif current_node_ID == 13:
        if neighbor_node_ID not in [5,12,14,20]:
            res = False
    elif current_node_ID == 14:
        if neighbor_node_ID not in [2,13,23]:
            res = False

    #fifth line
    elif current_node_ID == 15:
        if neighbor_node_ID not in [11,16]:
            res = False
    elif current_node_ID == 16:
        if neighbor_node_ID not in [15,17,19]:
            res = False
    elif current_node_ID == 17:
        if neighbor_node_ID not in [12,16]:
            res = False

    #sixth line
    elif current_node_ID == 18:
        if neighbor_node_ID not in [10,19]:
            res = False
    elif current_node_ID == 19:
        if neighbor_node_ID not in [16,18,20,22]:
            res = False
    elif current_node_ID == 20:
        if neighbor_node_ID not in [13,19]:
            res = False

    #seventh line
    elif current_node_ID == 21:
        if neighbor_node_ID not in [9,22]:
            res = False
    elif current_node_ID == 22:
        if neighbor_node_ID not in [19,21,23]:
            res = False
    elif current_node_ID == 23:
        if neighbor_node_ID not in [14,22]:
            res = False
    return res
def find_neighbours(nodes_dict):
        # Loop over all nodes multiple times to find neighbours. Not very efficient, but it works. To optimize!
        for node_id, node_data in nodes_dict.items():
            for neighbor_id, neighbor_data in nodes_dict.items():
                if neighbor_id != node_id:
                    node_x, node_y = node_data["rect"].center
                    neighbor_x, neighbor_y = neighbor_data["rect"].center
                    distance = math.sqrt((node_x - neighbor_x)**2 + (node_y - neighbor_y)**2)
                    #distance <= 50 and (node_x == neighbor_x or node_y == neighbor_y)
                    if are_good_neighbor(node_id,neighbor_id):
                        node_data["neighbours"].append(neighbor_id)
                    #if distance <= 150  and (node_x == neighbor_x or node_y == neighbor_y):
def create_node(node_id_start, node_size):
    """Create a dictionary of nodes.
    We cheat by hardcoding the positions of the nodes.
    The idea that each nodes start with brown color and got a brwon piece. Once we put a new piece,
        we change the current one to the wanted color. Each time we'll change the piece color,
        the node gonna also change it's color (for a better display)
    :param node_id_start: the id of the first node
    :param node_size: the size of the node
    :param node_margin: the space between nodes
    :param rows: the number of rows
    :param columns: the number of columns
    :return: a dictionary of nodes
    """

    positions = [(50,50),(200,50),(350,50),
                (100,100),(200,100),(300,100),
                (150,150),(200,150),(250,150),
                (50,200),(100,200),(150,200),(250,200),(300,200),(350,200),
                (150,250),(200,250),(250,250),
                (100,300),(200,300),(300,300),
                (50,350),(200,350),(350,350)]
    nodes = {}
    for position in positions:
        node_rect = pygame.Rect(position[0], position[1], node_size, node_size)
        node_piece = pion_classe.Pion(BRWON,position[0],position[1])
        nodes[node_id_start] = {"id":node_id_start,"rect": node_rect, "color": BRWON,"neighbours": [],"piece": node_piece}
        node_id_start += 1
    find_neighbours(nodes)# Find neighboring nodes

    return nodes
   