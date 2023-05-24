from setup import *
import random
from time import sleep
from Random_IA import *
from minimax import *
import copy
import pion_classe

class Setup_manager():
    """
        Cette classe permet de gérer le jeu.
        Lorsque le jeu commence, on crée les noeuds et on les affiche. Un noeud est un point brun,
        sur lequel on peut placer un pion et chaque pion a une couleur initialement blanche. La couleur du 
        pion change en fonction du joueur qui joue et ainsi donne sa couleur au noeud. Pour un joli 
        affichage, chaque noeud est relié à ses voisins par une ligne.

    """
    def __init__(self):
        
        pygame.init() #Initialize Pygame
        self.running = True #Variable pour savoir si le jeu est en cours
        self.who_play = 0
        self.nodes = create_node(node_id_start=0, node_size=15) #Create the nodes with neighbohood
        self.screen = setup_screen()
        
        self.phase = 0 #0: placement, 1: déplacement
        self.winner_name = None #Id du gagnant
        self.pion_nbr = 3 #Nombre de pions par joueur
        self.first_player = None
        self.second_player = None

        self.accessible_nodes = list(self.nodes.keys()) #Liste des noeuds accessibles
        self.temp_list = [] #Permet l'échange de pions pour la deuxieme phase

    ### Fonction pour afficher dans le terminal
    def print_nodes(self,nodes_dict):
        for node_id, node_data in nodes_dict.items():
            print(node_id, node_data)

    ### Fonction pour gérer les évènements (clavier, souris)
    def have_to_quit(self,event):
        if event.type == pygame.QUIT:
            self.running = False
            print("We hope you had fun!")
            pygame.quit() #not clean quit
            
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                print("We hope you had fun!")
                pygame.quit() #not clean quit
    
    def playing_event_handler(self):
        # Handle events
        # C'est le tour de l'humain
        for event in pygame.event.get():
            self.have_to_quit(event)
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    #Juste confort pour afficher les modif dans le terminal
                    self.print_nodes(self.nodes)

            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Check if a node was clicked
                pos = pygame.mouse.get_pos()
                for node_id, node_data in self.nodes.items():
                    if node_data["rect"].collidepoint(pos):
                        return(node_data)
class Player_manager(Setup_manager):
    def __init__(self):
        super().__init__()

        ### Fonction pour gérer le jeu

    def translate_to_color(self,color):
        if color == RED:
            return "RED"
        elif color == BLUE:
            return "BLUE"
        elif color == BRWON:
            return "BRWON"
        else:
            return "Error"
    
    def current_player_name(self):
        """
           Cette fonction permet de connaitre le nom du joueur en cours
        """
        if self.who_play == 0:
            return self.first_player.get_name()
        else:
            return self.second_player.get_name()
    def current_player_color(self):
        """
            cette fonction permet de connaitre la couleur du joueur en cours
        """
        if self.who_play == 0:
            #print("Player RED just played")
            return self.first_player.get_color()
        else:
            #print("Player BLUE just played")
            return self.second_player.get_color()
    def current_player_dict(self):
        """
            this function allows to know the dictionary of the current player
        """
        if self.who_play == 0:
            return self.first_player.get_nodes_id()
        else:
            return self.second_player.get_nodes_id()
    def current_player(self):
        """
            this function allows to know the current player
        """
        if self.who_play == 0:
            return self.first_player
        else:
            return self.second_player
    
    def ennemy_player_name(self):
        """
            this function allows to know the name of the ennemy player
        """
        if self.who_play == 0:
            return self.second_player.get_name()
        else:
            return self.first_player.get_name()
    def ennemy_player_color(self):
        """
            This function allows to know the color of the player who is not playing
        """
        if self.who_play == 0:
            return self.second_player.get_color()
        else:
            return self.first_player.get_color()
    def ennemy_player_dict(self):
        """
           this function allows to know the dictionary of the ennemy player
        """
        if self.who_play == 0:
            return self.second_player.get_nodes_id()
        else:
            return self.first_player.get_nodes_id()
    def ennemy_player(self):
        """
           this function allows to know the ennemy player
        """
        if self.who_play == 0:
            return self.second_player
        else:
            return self.first_player

    def ennemy_player_alligned_nodes(self):
        """
            this function allows to know the alligned nodes of the ennemy player
        """
        if self.who_play == 0:
            return self.second_player.alligned_nodes
        else:
            return self.first_player.alligned_nodes  
    
    def switch_player(self):
        """
           this function allows to switch the current player
        """
        if self.who_play == 0:
            self.who_play = 1
        else:
            self.who_play = 0
    
    def who_won(self):
        winner_name = None
        self.current_player().calculate_own_points() #On calcule les points du joueur en cours
        self.ennemy_player().calculate_own_points() #On calcule les points du joueur ennemi
        if  self.current_player().get_points() > self.ennemy_player().get_points() :
            winner_name = self.current_player_name()
        else:
            winner_name = self.ennemy_player_name()
        
        print("LE GRAND WINNER EEEEEEEST: ",winner_name)
        return winner_name
        
    def decrement_player_pions(self):
        """
           this function allows to decrement the number of pions of the current player
        """
        if self.who_play == 0:
            if self.first_player.get_pion_nbr() > 0:
                self.first_player.decrement_pion_nbr()
        else:
            if self.second_player.get_pion_nbr() >0:
                self.second_player.decrement_pion_nbr()
        if self.first_player.get_pion_nbr()==0 and self.second_player.get_pion_nbr()==0:
            
            print("\n____________________________________________________________________\n")
            print(f"Voici les noeuds utilisé par le joueur RED: {self.first_player.get_nodes_id()}")
            print(f"Voici les noeuds utilisé par le joueur BLUE : {self.second_player.get_nodes_id()}")
            print(f"Voici les noeuds accessibles : {self.accessible_nodes}")

            self.game_over(self.who_won())

    def give_current_game_state(self):
        return [self.accessible_nodes,self.ennemy_player_dict()]

    def copy_nodes(self):
        """
            Cette fonction permet de faire une copie des noeuds pour pouvoir les modifier sans modifier les 
                noeuds de la partie en cours, pour cela deep copy ne fonctionne pas, il faut faire une fonction 
                qui copie les noeuds un par un en recreant les objets internes.
        """
        nodes_copy = {}
        for node_id, node_data in self.nodes.items():
            node_rect = pygame.Rect(node_data["piece"].getPosX(),node_data["piece"].getPosY(), 15,15)
            node_piece = pion_classe.Pion(node_data["piece"].getColor(),node_data["piece"].getPosX(),node_data["piece"].getPosY())
            nodes_copy[node_id] = {"id":copy.deepcopy(node_id),"rect": node_rect, "color":node_data["piece"].getColor() ,"neighbours": copy.deepcopy(node_data["neighbours"]),"possible_move_nbr":copy.deepcopy(node_data["possible_move_nbr"]),"piece": node_piece}
        return nodes_copy
    
class Board(Player_manager):
    def __init__(self):
        super().__init__()
        ### Fonction Phase delta: Appelé dans toutes les phases
    def update_visual(self):
        if self.running:    
            # Fill the screen with black
                self.screen.fill(BLACK)
                # Draw the nodes with their id in the middle
                for node_id, node_data in self.nodes.items():
                    node_rect = node_data["rect"]
                    node_color = node_data["color"]
                    pygame.draw.rect(self.screen, node_color, node_rect)
                    font = pygame.font.Font(None, 24)
                    text_surface = font.render(str(node_id), True, WHITE)
                    text_rect = text_surface.get_rect(center=node_rect.center)
                    self.screen.blit(text_surface, text_rect)

                # Draw lines between neighboring nodes
                for node_data in self.nodes.values():
                    node_rect = node_data["rect"]
                    for neighbor_id in node_data["neighbours"]:
                        neighbor_rect = self.nodes[neighbor_id]["rect"]
                        pygame.draw.line(self.screen, GREY, node_rect.center, neighbor_rect.center, 2)

                # Update the display
                pygame.display.update()
        else:
            pygame.quit()       
    def change_piece_color(self,node_data):
        """
           this function allows to change the color of the piece and the node
        """
        if isinstance(node_data["piece"],pion_classe.Pion):
            node_data["piece"].setColor(self.current_player_color())
            node_data["color"] = self.current_player_color()
            print(f"Voici la liste des noeuds utilisés par le joueur {self.current_player_name()} : {self.current_player_dict()}")
            self.update_visual()

    def reset_piece_color( self, node_data):
        """
           this function allows to reset the color of the piece and the node
        """
        if isinstance(node_data["piece"],pion_classe.Pion):
            node_data["piece"].setColor(BRWON)
            node_data["color"] = BRWON
            self.update_visual()
        
    def nodes_share_same_position(self,node_data_positon,neighbor_1_position,neighbor_2_position):
        """
            Cette fonction vérifie si le noeud sélectionné est au centre d'un alignement de 3 noeuds voisins
            Exemple : _X_ avec X le noeud sélectionné et _ les noeuds voisins
        """
        if len(node_data_positon)==2 and len(neighbor_1_position)==2 and len(neighbor_2_position)==2:
            if node_data_positon[0]==neighbor_1_position[0] and node_data_positon[0]==neighbor_2_position[0]:
                return True
            elif node_data_positon[1]==neighbor_1_position[1] and node_data_positon[1]==neighbor_2_position[1]:
                return True
            else:
                return False
    def first_layer_are_aligned(self,node_data):
        """
            Cette fonction vérifie si les une pair de noeuds voisins au noeud sélectionné sont alignés
            et de meme couleur.
        """
        color = node_data["piece"].getColor()
        for neighbour_1_id in node_data["neighbours"]:
            neighbour_1_data= self.nodes[neighbour_1_id]

            for neighbour_2_id in node_data["neighbours"]:
                neighbour_2_data = self.nodes[neighbour_2_id]
                if neighbour_1_id != neighbour_2_id:
                    if isinstance(neighbour_1_data["piece"],pion_classe.Pion) and isinstance(neighbour_2_data["piece"],pion_classe.Pion):
                        if neighbour_1_data["piece"].getColor() == color and neighbour_2_data["piece"].getColor() == color:
                            #print(f'Voici les noeuds comparés ({node_data["id"]}:{color}),({neighbour_1_data["id"]},{neighbour_1_data["piece"].getColor()}),({neighbour_2_data["id"]},{neighbour_2_data["piece"].getColor()}) : first_layer_are_aligned')
                            node_data_position = node_data["rect"].center; node_data_id = node_data["id"]
                            neighbour_1_position = neighbour_1_data["rect"].center; neighbour_1_id = neighbour_1_data["id"]
                            neighbour_2_position = neighbour_2_data["rect"].center; neighbour_2_id = neighbour_2_data["id"]
                            if self.nodes_share_same_position(node_data_position,neighbour_1_position,neighbour_2_position):
                                current_line = [neighbour_1_id,node_data_id,neighbour_2_id]
                                self.current_player().add_line(current_line)
                                print(f"    Allignement de 3 pions en __1__ couches de la même couleur! {current_line}")
                                return True

        ### Si aucune pair de voisins (droite-gauche ou haut-bas) n'est alignée et de même couleur, on retourne False 
        return False
    def second_layer_are_aligned(self,node_data):
        """
            Cette fonction vérifie si le noeud séléctionné est à l'extremité d'un alignement de 3 noeuds 
                voisins de même couleur. Pour ce faire, nous vérifions si le noeud sélectionné est aligné
                avec un de ses voisins et si ce voisin est aligné avec un de ses voisins.
            Exemple : __X ou X__ avec X le noeud sélectionné et _ les noeuds voisins

            Si il devait y avoir un nombre arbitraire de couches, il faudrait faire une fonction récursive
                mais, ici on sait qu'on ne veut qu'un enchainement de 3 noeuds.
        """
        
        color = node_data["piece"].getColor()
        for neighbour_1_id in node_data["neighbours"]:
            neighbour_1_data = self.nodes[neighbour_1_id]
            if isinstance(neighbour_1_data["piece"],pion_classe.Pion) and neighbour_1_data["color"]==color:
                for neighbour_2_id in neighbour_1_data["neighbours"]:
                    neighbour_2_data = self.nodes[neighbour_2_id]
                    if node_data["id"] != neighbour_2_id:
                        if isinstance(neighbour_2_data["piece"],pion_classe.Pion):
                            if neighbour_2_data["color"]==color:
                                #print(f'Voici les noeuds comparés ({node_data["id"]}:{color}),({neighbour_1_data["id"]},{neighbour_1_data["piece"].getColor()}),({neighbour_2_data["id"]},{neighbour_2_data["piece"].getColor()}) : second_layer_are_aligned')
                                node_data_position = node_data["rect"].center; node_data_id = node_data["id"]
                                neighbour_1_position = neighbour_1_data["rect"].center; neighbour_1_id = neighbour_1_data["id"]
                                neighbour_2_position = neighbour_2_data["rect"].center; neighbour_2_id = neighbour_2_data["id"]
                                if self.nodes_share_same_position(node_data_position,neighbour_1_position,neighbour_2_position):
                                    current_line = [node_data_id,neighbour_1_id,neighbour_2_id]
                                    self.current_player().add_line(current_line)
                                    print(f"    Allignement de 3 pions en __2__ couches de la même couleur! {current_line}")
                                    return True
    def is_in_allignement(self,node_data):
        """
            Cette fonction permet de vérifier si un joueur a aligné 3 pions de la même couleur. Pour ce faire,
                on vérifie les noeuds adjacents au noeud sélectionné.
        """
        if isinstance(node_data["piece"],pion_classe.Pion):
            color = node_data["piece"].getColor()
            if color == BRWON:
                return False
            else:
                if self.first_layer_are_aligned(node_data):
                    ### Premier cas: Le noeud que l'ont vient de déplasser est au centre de l'alignement
                        # Donc on vérifie les noeuds droite/gauche et haut/bas 
                    return True
                elif self.second_layer_are_aligned(node_data):
                    ### Deuxieme cas: Le noeud que l'ont vient de déplasser est à l'extremité de l'alignement
                        # Donc on vérifie jusqu'à 2 noeuds de profondeur (manque de temps pour faire une fonction récursive)
                    return True
                else:
                    return False

        return False
    def is_there_winner(self,node_data):
        """
            Cette fonction permet de vérifier si un joueur a gagné. On vérifie si un joueur a aligné 3 
                pions de la même couleur. Si c'est le cas, on dit qui a gagné. Pour ce faire, on vérifie les 
                noeuds adjacents au noeud sélectionné.
            Par construciton, node_data est un noeud de COULEUR RED/BLUE
        """
        if self.is_in_allignement(node_data=node_data):
            ### On ne vérifie la couleur du noeud que si il y a eu un alignement
            self.delete_ennemy_piece()
            print("___________________________________________________________________________")
    
    def game_over(self, winner_name):
        if self.phase==0:
            print("\n\n___________________________________________________________________________")
            print(f"Youhou! Le joueur {winner_name} a gagné!")
            print("__________________________________THE END__________________________________")
            self.running = False
            self.winner_name = winner_name

    
    def delete_ennemy_piece(self):
        """
            Fonction qui permet de supprimer un pion ennemi
        """
        ennemy_dict = self.ennemy_player_dict()
        ennemy_list = list(ennemy_dict.keys())

        #change all ennemy piece color to Green
        for ennemy_key in ennemy_list:
            ennemy_data = self.nodes[ennemy_key]
            if isinstance(ennemy_data["piece"],pion_classe.Pion):
                if not self.is_in_allignement(ennemy_data):
                    ennemy_data["piece"].setColor(GREEN)
                    color = ennemy_data["color"]
                    ennemy_data["color"] = GREEN
        self.update_visual()
        
        didnt_delete = True
        while(didnt_delete):
            returned_key = self.current_player().choose_node_to_delete(ennemy_list)
            node_data = self.nodes[returned_key]
            if not self.is_in_allignement(node_data):
                #On peut supprimer le pion car en allignement
                if isinstance(node_data["piece"],pion_classe.Pion):
                    old_color = node_data["piece"].getColor()
                    node_data["piece"].setColor(BRWON)
                    node_data["color"] = BRWON
                    print(f"    ___Here's the ennemy dict: {self.ennemy_player_dict()}")
                    print(f"    ___Le joueur {self.current_player_name()} vient de supprimer le pion {returned_key} de couleur {self.translate_to_color(old_color)}")
                    self.ennemy_player_dict().pop(returned_key)
                    print(f"    ___Here's the ennemy dict: {self.ennemy_player_dict()}")
                    self.accessible_nodes.append(returned_key)
                    didnt_delete = False
                    if len(self.ennemy_player_dict()) <= 2 and self.ennemy_player().get_pion_nbr()==0:
                        self.game_over(self.current_player_name())
            else:
                print(f"{returned_key} appartient à un alignement de 3 pions de la même couleur. On ne peut pas le supprimer")

            ennemy_list.remove(returned_key)

        #switch back all ennemy piece color to their original color
        for ennemy_key in ennemy_list:
            ennemy_data = self.nodes[ennemy_key]
            if isinstance(ennemy_data["piece"],pion_classe.Pion):
                ennemy_data["piece"].setColor(color)
                ennemy_data["color"] = color
        self.update_visual()

    def get_accessible_nodes_data(self):
        accessible_nodes_data = []
        for node_id in self.accessible_nodes:
            accessible_nodes_data.append(self.nodes[node_id])
        return accessible_nodes_data
    
    def check_if_nodes_are_adjacent(self,node_data_1,node_data_2):
        if node_data_1["id"] in node_data_2["neighbours"]:
            return True
        else:
            return False
        ### Fonction Phase 0: Pose des pions
    ### Fonction Phase 1: Echange entre pions
    def print_comparaison(self,node_data_1,node_data_2,color_1,color_2,is_print):
        if is_print:
            node_data_ID_1 = node_data_1["id"]
            node_data_ID_2 = node_data_2["id"]
            
    def piece_can_switch(self,node_data_1,node_data_2,is_print=True):
        if isinstance(node_data_1["piece"],pion_classe.Pion) and isinstance(node_data_2["piece"],pion_classe.Pion):
            if node_data_1["id"] in self.current_player_dict():
                node_data_1["piece"].setColor(self.current_player_color())
                node_data_1["color"] = node_data_1["piece"].getColor()
            elif node_data_2["id"] in self.ennemy_player_dict():
                node_data_1["piece"].setColor(self.ennemy_player_color())
                node_data_1["color"] = node_data_1["piece"].getColor()

            if node_data_2["id"] in self.current_player_dict():
                node_data_2["piece"].setColor(self.current_player_color())
                node_data_2["color"] = node_data_2["piece"].getColor()
            elif node_data_2["id"] in self.ennemy_player_dict():
                node_data_2["piece"].setColor(self.ennemy_player_color())
                node_data_2["color"] = node_data_2["piece"].getColor()

            color_1 = node_data_1["piece"].getColor()
            color_2 = node_data_2["piece"].getColor()
            if (color_1 == BRWON and color_2 == BRWON) :
                print("Vous ne pouvez pas échanger ces pions car vous n'avez sélectionné que des noeuds vide")
                return False
            else:
                self.print_comparaison(node_data_1,node_data_2,color_1,color_2,is_print)
                if (color_1 == self.current_player_color() and color_2 == BRWON) :
                    #Ici, on échange les pions car on sait que l'un des deux noeuds est vide
                    return True
                else:

                    return False
        else:
            print("Error : Vous n'avez pas sélectionné deux pions")
            return False
    def switch_pieces_nodes(self):
        [node_data_1,node_data_2] = self.temp_list
        [id_1,id_2] = [node_data_1["id"],node_data_2["id"]]

        if isinstance(node_data_1["piece"],pion_classe.Pion) and isinstance(node_data_2["piece"],pion_classe.Pion):
            if self.piece_can_switch(node_data_1,node_data_2,is_print=False):
                if self.is_in_allignement(node_data_1):
                    #Si node_data_1 est en allignement ET qu'on le change de place, on perd l'allignement
                        #de ce noeud
                    self.current_player().delete_line(node_data_1)
                
                print(f"    Le joueur {self.current_player_name()} va perdre le noeud {id_1} et gagner {id_2}")

                    #Changement de couleur des pions
                old_color = node_data_1["piece"].getColor()
                node_data_1["piece"].setColor(node_data_2["piece"].getColor())
                node_data_2["piece"].setColor(old_color)
                    #Changement de couleur des noeuds
                node_data_1["color"] = node_data_1["piece"].getColor()
                node_data_2["color"] = node_data_2["piece"].getColor()
                    #Changement dans le dict
                print(f"    ___AVANT : Voici les noeuds utilisés par le joueur {self.current_player_name()} : {self.current_player_dict()}")
                self.current_player_dict()[node_data_2["id"]] = node_data_2["id"]
                self.current_player_dict().pop(id_1,None)
                print(f"    ___APRES : Voici les noeuds utilisés par le joueur {self.current_player_name()} : {self.current_player_dict()}")
                    #Changement de la liste des noeuds accessibles
                index_to_remove = self.accessible_nodes.index(id_2)
                print(f"        ___Voici les noeuds accessibles {self.accessible_nodes}")
                print(f"        Remove ID {id_2} at the index {index_to_remove}. Then add the ID {id_1}")
                self.accessible_nodes.remove(id_2)
                self.accessible_nodes.append(id_1)
                print(f"        ___Voici les nouveaux noeuds accessibles {self.accessible_nodes}")
                
                self.animation_on_switch()
                self.temp_list = []
                self.update_visual()

    def animation_on_switch(self):
        """
            Cette fonction permet de faire une animation lorsqu'on échange deux pions
            animation: un carré de la couleur de la pièce qui bouge se déplace jusqu'au noeud brun
        """
        rect = pygame.draw.rect(self.screen, self.current_player_color(), self.temp_list[0]["rect"])
        pygame.display.update()
       
        while rect.center != self.temp_list[1]["rect"].center:
        #for i in range(10):
            if self.temp_list[0]["rect"].center[0] == self.temp_list[1]["rect"].center[0]:
                if self.temp_list[0]["rect"].center[1] < self.temp_list[1]["rect"].center[1]:
                    rect.center = (rect.center[0],rect.center[1]+10)
                else:
                    rect.center = (rect.center[0],rect.center[1]-10)
            elif self.temp_list[0]["rect"].center[1] == self.temp_list[1]["rect"].center[1]:
                if self.temp_list[0]["rect"].center[0] < self.temp_list[1]["rect"].center[0]:
                    rect.center = (rect.center[0]+10,rect.center[1])
                else:
                    rect.center = (rect.center[0]-10,rect.center[1])
            self.update_visual()
            rect = pygame.draw.rect(self.screen, self.current_player_color(), rect)
            pygame.display.update()
            sleep(0.05)   
     
     
class Game(Board):
    
    def run(self, first="Random_IA", second="Random_IA"):
        # Game loop
        node_color = BLUE #n'importe quelle couleur fonctionne, c'est juste pour initialiser
        print(f"Here are the players : {first} and {second}")
        match first:
                    case "Random_IA":
                        self.first_player = Random_IA(0,RED,"RED",self.pion_nbr)
                    case "Minimax":
                        self.first_player = Minimax_IA(0,RED,"RED",self.pion_nbr,1)
                    case "Minimax1":
                        self.first_player = Minimax_IA(0,RED,"RED",self.pion_nbr,1)
                    case "Minimax2":
                        self.first_player = Minimax_IA(0,RED,"RED",self.pion_nbr,2)
                    case "Minimax3":
                        self.first_player = Minimax_IA(0,RED,"RED",self.pion_nbr,3)
                    case "Human":
                        self.first_player = Human(0,RED,"RED",self.pion_nbr)
                    case _:
                        print("Error: first_player is not a valid player")
                        print("Use one of the following: Random_IA, Minimax,Minimax1,Minimax2,Minimax3, Montecarlo, Human")
                        return

        match second:
                    case "Random_IA":
                        self.second_player = Random_IA(1,BLUE,"BLUE",self.pion_nbr)
                    case "Minimax":
                        self.second_player = Minimax_IA(0,BLUE,"BLUE",self.pion_nbr,1)
                    case "Minimax1":
                        self.second_player = Minimax_IA(0,BLUE,"BLUE",self.pion_nbr,1)
                    case "Minimax2":
                        self.second_player = Minimax_IA(0,BLUE,"BLUE",self.pion_nbr,2)
                    case "Minimax3":
                        self.second_player = Minimax_IA(0,BLUE,"BLUE",self.pion_nbr,3)
                    case "Human":
                        self.second_player = Human(1,BLUE,"BLUE",self.pion_nbr)
                    case _:
                        print("Error: second_player is not a valid player")
                        print("Use one of the following: Random_IA, Minimax,Minimax1,Minimax2,Minimax3, Montecarlo, Human")
                        return
            
        while self.running:
            self.update_visual()
            if self.who_play == 0:
                # C'est le tour du joueur1
                self.first_player.play(self)
            else:
                # C'est le tour du joueur2
                self.second_player.play(self)

            # Update the display
        # Quit Pygame
        pygame.quit()
        return self.winner_name
    
class Game_copy():
    def __init__(self, game):
        
        self.running = game.running #Variable pour savoir si le jeu est en cours
        self.who_play = game.who_play
        self.nodes = game.copy_nodes() #Dictionnaire des noeuds
        self.phase = game.phase #0: placement, 1: déplacement
        self.winner_name = game.winner_name #Id du gagnant
        self.pion_nbr = game.pion_nbr #Nombre de pions par joueur

        self.first_player = game.first_player.create_copy()
        self.second_player = game.second_player.create_copy()

        self.accessible_nodes = copy.deepcopy(game.accessible_nodes) 
        self.temp_list = [] #Liste temporaire pour stocker les noeuds sélectionnés

    def translate_to_color(self,color):
        if color == RED:
            return "RED"
        elif color == BLUE:
            return "BLUE"
        elif color == BRWON:
            return "BRWON"
        else:
            return "Error"
    def current_player_name(self):
        if self.who_play == 0:
            return self.first_player.get_name()
        else:
            return self.second_player.get_name()
    def current_player_color(self):
      
        if self.who_play == 0:
            #print("Player RED just played")
            return self.first_player.get_color()
        else:
            #print("Player BLUE just played")
            return self.second_player.get_color()
    def ennemy_player_color(self):
      
        if self.who_play == 0:
            return self.second_player.get_color()
        else:
            return self.first_player.get_color()
    def current_player_dict(self):
       
        if self.who_play == 0:
            return self.first_player.get_nodes_id()
        else:
            return self.second_player.get_nodes_id()
    def current_player(self):    
        if self.who_play == 0:
            return self.first_player
        else:
            return self.second_player      
    def ennemy_player_dict(self):
      
        if self.who_play == 0:
            return self.second_player.get_nodes_id()
        else:
            return self.first_player.get_nodes_id()
    def ennemy_player_name(self):
        if self.who_play == 0:
            return self.second_player.get_name()
        else:
            return self.first_player.get_name()      
    def ennemy_player(self):
        """
           this function allows to know the ennemy player
        """
        if self.who_play == 0:
            return self.second_player
        else:
            return self.first_player

    
    def switch_player(self):
    
        if self.who_play == 0:
            self.who_play = 1
        else:
            self.who_play = 0
    

    def who_won(self):
        winner_name = None
        self.current_player().calculate_own_points() #On calcule les points du joueur en cours
        self.ennemy_player().calculate_own_points() #On calcule les points du joueur ennemi
        if  self.current_player().get_points() > self.ennemy_player().get_points() :
            winner_name = self.current_player_name()
        else:
            winner_name = self.ennemy_player_name()
        
        print("LE GRAND WINNER EEEEEEEST: ",winner_name)
        return winner_name
    def decrement_player_pions(self):
      
        if self.who_play == 0:
            if self.first_player.get_pion_nbr() > 0:
                self.first_player.decrement_pion_nbr()
        else:
            if self.second_player.get_pion_nbr() >0:
                self.second_player.decrement_pion_nbr()
        if self.first_player.get_pion_nbr()==0 and self.second_player.get_pion_nbr()==0:
            
            print("\n____________________________________________________________________\n")
            print(f"Voici les noeuds utilisé par le joueur RED: {self.first_player.get_nodes_id()}")
            print(f"Voici les noeuds utilisé par le joueur BLUE : {self.second_player.get_nodes_id()}")
            print(f"Voici les noeuds accessibles : {self.accessible_nodes}")

            self.game_over(self.who_won())

    def change_piece_color(self,node_data):
        """
            C'est ici que l'on change la couleur du pion AINSI que celle du node.
        """
        if isinstance(node_data["piece"],pion_classe.Pion):
            node_data["piece"].setColor(self.current_player_color())

            #new_piece_color = node_data["piece"].getColor()
            node_data["color"] = self.current_player_color()
            #print(f"Vous venez de déposer un pion de couleur{new_piece_color}")
           

    def nodes_share_same_position(self,node_data_positon,neighbor_1_position,neighbor_2_position):
        """
            Cette fonction vérifie si le noeud sélectionné est au centre d'un alignement de 3 noeuds voisins
            Exemple : _X_ avec X le noeud sélectionné et _ les noeuds voisins
        """
        if len(node_data_positon)==2 and len(neighbor_1_position)==2 and len(neighbor_2_position)==2:
            if node_data_positon[0]==neighbor_1_position[0] and node_data_positon[0]==neighbor_2_position[0]:
                return True
            elif node_data_positon[1]==neighbor_1_position[1] and node_data_positon[1]==neighbor_2_position[1]:
                return True
            else:
                return False
    def first_layer_are_aligned(self,node_data):
        """
            Cette fonction vérifie si les une pair de noeuds voisins au noeud sélectionné sont alignés
            et de meme couleur.
        """
        color = node_data["piece"].getColor()
        for neighbour_1_id in node_data["neighbours"]:
            neighbour_1_data= self.nodes[neighbour_1_id]
            # si le noeud voisin est dans la liste des noeuds utilisés par le joueur mettre sa couleur à la couleur du joeur
            if neighbour_1_id in self.current_player_dict():
                neighbour_1_data["piece"].setColor(self.current_player_color())
                #neighbour_1_data["color"] = self.current_player_color()

            for neighbour_2_id in node_data["neighbours"]:
                neighbour_2_data = self.nodes[neighbour_2_id]
                # si le noeud voisin est dans la liste des noeuds utilisés par le joueur mettre sa couleur à la couleur du joeur
                if neighbour_2_id in self.current_player_dict():
                    neighbour_2_data["piece"].setColor(self.current_player_color())
                    #neighbour_2_data["color"] = self.current_player_color()

                if neighbour_1_id != neighbour_2_id:
                    print(f"Voici les noeuds comparés ({node_data['id']}:{color}),({neighbour_1_data['id']},{neighbour_1_data['piece'].getColor()}),({neighbour_2_data['id']},{neighbour_2_data['piece'].getColor()})")
                    if isinstance(neighbour_1_data["piece"],pion_classe.Pion) and isinstance(neighbour_2_data["piece"],pion_classe.Pion):
                        if neighbour_1_data["piece"].getColor() == color and neighbour_2_data["piece"].getColor() == color:
                            #print(f'Voici les noeuds comparés ({node_data["id"]}:{color}),({neighbour_1_data["id"]},{neighbour_1_data["piece"].getColor()}),({neighbour_2_data["id"]},{neighbour_2_data["piece"].getColor()}) : first_layer_are_aligned')
                            node_data_position = node_data["rect"].center; node_data_id = node_data["id"]
                            neighbour_1_position = neighbour_1_data["rect"].center; neighbour_1_id = neighbour_1_data["id"]
                            neighbour_2_position = neighbour_2_data["rect"].center; neighbour_2_id = neighbour_2_data["id"]
                            if self.nodes_share_same_position(node_data_position,neighbour_1_position,neighbour_2_position):
                                current_line = [neighbour_1_id,node_data_id,neighbour_2_id]
                                if current_line not in self.current_player().alligned_nodes:
                                    self.current_player().add_line(current_line)
                                    #print(f"    Allignement de 3 pionsseaux en __1__ couches de la même couleur! {current_line}")
                                    #print(" game address : ",id(self))
                                return True

        ### Si aucune pair de voisins (droite-gauche ou haut-bas) n'est alignée et de même couleur, on retourne False 
        return False
    def second_layer_are_aligned(self,node_data):
        """
            Cette fonction vérifie si le noeud séléctionné est à l'extremité d'un alignement de 3 noeuds 
                voisins de même couleur. Pour ce faire, nous vérifions si le noeud sélectionné est aligné
                avec un de ses voisins et si ce voisin est aligné avec un de ses voisins.
            Exemple : __X ou X__ avec X le noeud sélectionné et _ les noeuds voisins

            Si il devait y avoir un nombre arbitraire de couches, il faudrait faire une fonction récursive
                mais, ici on sait qu'on ne veut qu'un enchainement de 3 noeuds.
        """
        
        color = node_data["piece"].getColor()
        for neighbour_1_id in node_data["neighbours"]:
            neighbour_1_data = self.nodes[neighbour_1_id]
            if neighbour_1_id in self.current_player_dict():
                neighbour_1_data["piece"].setColor(self.current_player_color())
                #neighbour_1_data["color"] = self.current_player_color()
            if isinstance(neighbour_1_data["piece"],pion_classe.Pion) and neighbour_1_data["color"]==color:
                for neighbour_2_id in neighbour_1_data["neighbours"]:
                    neighbour_2_data = self.nodes[neighbour_2_id]
                    if neighbour_2_id in self.current_player_dict():
                        neighbour_2_data["piece"].setColor(self.current_player_color())
                        #neighbour_2_data["color"] = self.current_player_color()
                    if node_data["id"] != neighbour_2_id:
                        if isinstance(neighbour_2_data["piece"],pion_classe.Pion):
                            if neighbour_2_data["color"]==color:
                                #print(f"Voici les noeuds comparés ({node_data['id']}:{color}),({neighbour_1_data['id']},{neighbour_1_data['piece'].getColor()}),({neighbour_2_data['id']},{neighbour_2_data['piece'].getColor()})")
                                node_data_position = node_data["rect"].center; node_data_id = node_data["id"]
                                neighbour_1_position = neighbour_1_data["rect"].center; neighbour_1_id = neighbour_1_data["id"]
                                neighbour_2_position = neighbour_2_data["rect"].center; neighbour_2_id = neighbour_2_data["id"]
                                if self.nodes_share_same_position(node_data_position,neighbour_1_position,neighbour_2_position):
                                    current_line = [node_data_id,neighbour_1_id,neighbour_2_id]
                                    if current_line not in self.current_player().alligned_nodes:
                                        self.current_player().add_line(current_line)
                                        #print(f"    Allignement de 3 pionsseaux en __2__ couches de la même couleur! {current_line}")
                                        #print(" game address : ",id(self))
                                    return True
    def is_in_allignement(self,node_data):
        """
            Cette fonction permet de vérifier si un joueur a aligné 3 pions de la même couleur. Pour ce faire,
                on vérifie les noeuds adjacents au noeud sélectionné.
        """
        if isinstance(node_data["piece"],pion_classe.Pion):
            color = node_data["piece"].getColor()
            if color == BRWON:
                return False
            else:
                if self.first_layer_are_aligned(node_data):
                    ### Premier cas: Le noeud que l'ont vient de déplasser est au centre de l'alignement
                        # Donc on vérifie les noeuds droite/gauche et haut/bas 
                    return True
                elif self.second_layer_are_aligned(node_data):
                    ### Deuxieme cas: Le noeud que l'ont vient de déplasser est à l'extremité de l'alignement
                        # Donc on vérifie jusqu'à 2 noeuds de profondeur (manque de temps pour faire une fonction récursive)
                    return True
                else:
                    return False

        return False
    def is_there_winner(self,node_data):
        """
            Cette fonction permet de vérifier si un joueur a gagné. On vérifie si un joueur a aligné 3 
                pions de la même couleur. Si c'est le cas, on dit qui a gagné. Pour ce faire, on vérifie les 
                noeuds adjacents au noeud sélectionné.
            Par construciton, node_data est un noeud de COULEUR RED/BLUE
        """
        if self.is_in_allignement(node_data=node_data):
            ### On ne vérifie la couleur du noeud que si il y a eu un alignement
            self.delete_ennemy_piece()
            print("___________________________________________________________________________")
    
    def game_over(self, winner_name):
        if self.phase==0:
            print("\n\n___________________________________________________________________________")
            print(f"Youhou! Le joueur {winner_name} a gagné!")
            print("__________________________________THE END__________________________________")
            self.running = False
            self.winner_name = winner_name

    
    def delete_ennemy_piece(self):
        """
            Fonction qui permet de supprimer un pion ennemi
        """
        ennemy_dict = self.ennemy_player_dict()
        ennemy_list = list(ennemy_dict.keys())

        #change all ennemy piece color to Green
        for ennemy_key in ennemy_list:
            ennemy_data = self.nodes[ennemy_key]
            if isinstance(ennemy_data["piece"],pion_classe.Pion):
                if not self.is_in_allignement(ennemy_data):
                    ennemy_data["piece"].setColor(GREEN)
                    color = ennemy_data["color"]
                    ennemy_data["color"] = GREEN
        
        didnt_delete = True
        while(didnt_delete):
            returned_key = self.current_player().choose_node_to_delete(ennemy_list)
            node_data = self.nodes[returned_key]
            if not self.is_in_allignement(node_data):
                #On peut supprimer le pion car en allignement
                if isinstance(node_data["piece"],pion_classe.Pion):
                    old_color = node_data["piece"].getColor()
                    node_data["piece"].setColor(BRWON)
                    node_data["color"] = BRWON
                    self.ennemy_player_dict().pop(returned_key)
                    self.accessible_nodes.append(returned_key)
                    didnt_delete = False
                    if len(self.ennemy_player_dict()) <= 2 and self.ennemy_player().get_pion_nbr()==0:
                        self.game_over(self.current_player_name())
            else:
                print(f"{returned_key} appartient à un alignement de 3 pionsseaux de la même couleur. On ne peut pas le supprimer")

            ennemy_list.remove(returned_key)

        #switch back all ennemy piece color to their original color
        for ennemy_key in ennemy_list:
            ennemy_data = self.nodes[ennemy_key]
            if isinstance(ennemy_data["piece"],pion_classe.Pion):
                ennemy_data["piece"].setColor(color)
                ennemy_data["color"] = color

    def get_accessible_nodes_data(self):
        accessible_nodes_data = []
        for node_id in self.accessible_nodes:
            accessible_nodes_data.append(self.nodes[node_id])
        return accessible_nodes_data
    
    def check_if_nodes_are_adjacent(self,node_data_1,node_data_2):
        if node_data_1["id"] in node_data_2["neighbours"]:
            return True
        else:
            return False
        ### Fonction Phase 0: Pose des pions
    ### Fonction Phase 1: Echange entre pions
    def print_comparaison(self,node_data_1,node_data_2,color_1,color_2,is_print):
        if is_print:
            node_data_ID_1 = node_data_1["id"]
            node_data_ID_2 = node_data_2["id"]
            print(f"    {self.current_player_name()} vient de comparer {node_data_ID_1}/{node_data_ID_2} avec comme couleur {self.translate_to_color(color_1)}/{self.translate_to_color(color_2)}")
    def piece_can_switch(self,node_data_1,node_data_2,is_print=True):
        if isinstance(node_data_1["piece"],pion_classe.Pion) and isinstance(node_data_2["piece"],pion_classe.Pion):
            if node_data_1["id"] in self.current_player_dict():
                node_data_1["piece"].setColor(self.current_player_color())
                node_data_1["color"] = node_data_1["piece"].getColor()
            elif node_data_2["id"] in self.ennemy_player_dict():
                node_data_1["piece"].setColor(self.ennemy_player_color())
                node_data_1["color"] = node_data_1["piece"].getColor()

            if node_data_2["id"] in self.current_player_dict():
                node_data_2["piece"].setColor(self.current_player_color())
                node_data_2["color"] = node_data_2["piece"].getColor()
            elif node_data_2["id"] in self.ennemy_player_dict():
                node_data_2["piece"].setColor(self.ennemy_player_color())
                node_data_2["color"] = node_data_2["piece"].getColor()

            color_1 = node_data_1["piece"].getColor()
            color_2 = node_data_2["piece"].getColor()
            if (color_1 == BRWON and color_2 == BRWON) :
                print("Vous ne pouvez pas échanger ces pions car vous n'avez sélectionné que des noeuds vide")
                return False
            else:
                self.print_comparaison(node_data_1,node_data_2,color_1,color_2,is_print)
                if (color_1 == self.current_player_color() and color_2 == BRWON)  :
                    #Ici, on échange les pions car on sait que l'un des deux noeuds est vide
                    return True
                else:

                    return False
        else:
            print("Error : Vous n'avez pas sélectionné deux pions")
            return False
    def switch_pieces_nodes(self):

        #Rappel: Lors de l'appel de cette fonction, le premier noeud est TOUJOURS celui de couleur (celui qui 
        # va bouger) et le deuxième est TOUJOURS celui brun!

        [node_data_1,node_data_2] = self.temp_list
        [id_1,id_2] = [node_data_1["id"],node_data_2["id"]]

        if isinstance(node_data_1["piece"],pion_classe.Pion) and isinstance(node_data_2["piece"],pion_classe.Pion):
            if self.piece_can_switch(node_data_1,node_data_2,is_print=False):
                if self.is_in_allignement(node_data_1):
                    #Si node_data_1 est en allignement ET qu'on le change de place, on perd l'allignement
                        #de ce noeud
                    self.current_player().delete_line(node_data_1)

                    #Changement de couleur des pions
                old_color = node_data_1["piece"].getColor()
                node_data_1["piece"].setColor(node_data_2["piece"].getColor())
                node_data_2["piece"].setColor(old_color)
                    #Changement de couleur des noeuds
                node_data_1["color"] = node_data_1["piece"].getColor()
                node_data_2["color"] = node_data_2["piece"].getColor()
                    #Changement dans le dict
                self.current_player_dict()[node_data_2["id"]] = node_data_2["id"]
                self.current_player_dict().pop(id_1,None)
                    #Changement de la liste des noeuds accessibles
                index_to_remove = self.accessible_nodes.index(id_2)
                self.accessible_nodes.remove(id_2)
                self.accessible_nodes.append(id_1)
                
                self.temp_list = []
    def copy_nodes(self):

        """
            Cette fonction permet de faire une copie des noeuds pour pouvoir les modifier sans modifier les 
                noeuds de la partie en cours, pour cela deep copy ne fonctionne pas, il faut faire une fonction 
                qui copie les noeuds un par un en recreant les objets internes."""
        nodes_copy = {}
        for node_id, node_data in self.nodes.items():
            node_rect = pygame.Rect(node_data["piece"].getPosX(),node_data["piece"].getPosY(), 15,15)
            node_piece = pion_classe.Pion(node_data["piece"].getColor(),node_data["piece"].getPosX(),node_data["piece"].getPosY())
            nodes_copy[node_id] = {"id":copy.deepcopy(node_id),"rect": node_rect, "color":node_data["piece"].getColor() ,"neighbours": copy.deepcopy(node_data["neighbours"]),"possible_move_nbr":copy.deepcopy(node_data["possible_move_nbr"]),"piece": node_piece}
            #print data neighbours
        return nodes_copy
    
    def ennemy_player_alligned_nodes(self):
        if self.who_play == 0:
            return self.second_player.alligned_nodes
        else:
            return self.first_player.alligned_nodes

    def reset_piece_color( self, node_data):
        if isinstance(node_data["piece"],pion_classe.Pion):
            node_data["piece"].setColor(BRWON)
            node_data["color"] = BRWON