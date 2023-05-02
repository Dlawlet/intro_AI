from setup import *
import random

"""
A mmodifer:
    -REFACTOR LE CODE: 
        -Pour optimiser l'arbre de décision : noeuds_accessibles/noeuds_rouge/noeuds_bleus
            Ex : noeuds_rouge = [0,1,2,13,3,11,12] permet de facilement vérfier si rouge a perdu
            noeuds_accessibles = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14]
    -on ne peut déplacer QUE les pions de NOTRE couleur
    -A chaque allignement, on peut retirer un pion de l'adversaire 
        -sauf si il est dans un allignement
"""

class MyGame():
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
        self.nodes = create_node(0, 15) #Create the nodes with neighbohood
        self.screen = setup_screen()
        self.phase = 0 #0: placement, 1: déplacement
        self.first_player_pions = 5
        self.second_player_pions = 5

        self.temp_list = [] #Permet l'échange de pions pour la deuxieme phase
    
    
    ### Fonction pour gérer les couleurs des noeuds/pions
    ### Fonction Phase 0: Placement des pions
    def change_piece_color(self,node_data):
        """
            C'est ici que l'on change la couleur du pion AINSI que celle du node.
        """
        if isinstance(node_data["piece"],pion_classe.Pion):
            node_data["piece"].setColor(self.current_player_color())

            new_piece_color = node_data["piece"].getColor()
            node_data["color"] = new_piece_color
            #print(f"Vous venez de déposer un pion de couleur{new_piece_color}")
    
    def current_player_name(self):
        """
            Rien de compliqué. Cette fonction permet de connaitre le nom du joueur en cours
        """
        if self.who_play == 0:
            return "RED"
        else:
            return "BLUE"
    def current_player_color(self):
        """
            Rien de compliqué. Cette fonction permet de connaitre la couleur du joueur en cours
        """
        if self.who_play == 0:
            print("Player RED just played")
            return RED
        else:
            print("Player BLUE just played")
            return BLUE
    
    def switch_player(self):
        """
            Rien de compliqué, cette fonction permet de changer de joueur en cours
        """
        if self.who_play == 0:
            self.who_play = 1
        else:
            self.who_play = 0
    def decrement_player_pions(self):
        """
            Fonction qui permet de décrémenter le nombre de pions restants pour chaque joueur
            Une fois le nombre de pions à 0, on passe à la phase 1
        """
        if self.who_play == 0:
            if self.first_player_pions > 0:
                self.first_player_pions -= 1
        else:
            if self.second_player_pions>0:
                self.second_player_pions -= 1
        #print(f"Le joueur _{self.who_play}_ a encore {self.second_player_pions} pions")
        if self.first_player_pions==0 and self.second_player_pions==0:
            self.phase = 1
            print("____________________On passe à la deuxieme phase!!____________________\n")
    
    ### Fonction Phase 1: Echange entre pions
    def piece_can_switch(self,node_data_1,node_data_2):
        """
            Rien de compliqué. Cette fonction permet de savoir si l'un des deux noeuds peut échanger son pion
                avec l'autre noeud. L'echange a lieu que si et seulement si L'UN des deux noeuds est vide
        """
        if isinstance(node_data_1["piece"],pion_classe.Pion) and isinstance(node_data_2["piece"],pion_classe.Pion):
            color_1 = node_data_1["piece"].getColor()
            color_2 = node_data_2["piece"].getColor()
            if (color_1 == BRWON and color_2 == BRWON) :
                print("Vous ne pouvez pas échanger ces pions car vous n'avez sélectionné que des noeuds vide")
                return False
            else:
                if color_1 == BRWON or color_2 == BRWON :
                    #Ici, on échange les pions car on sait que l'un des deux noeuds est vide
                    return True
                else:
                    print("Vous ne pouvez déposer ce pion ici car aucun noeud n'est vide")
                    return False
        else:
            print("Error : Vous n'avez pas sélectionné deux pions")
            return False
    def switch_pieces_nodes(self):
        """
            Rien de compliqué. Cette fonction permet d'échanger les pions de deux noeuds
        """

        node_data_1 = self.temp_list[0]
        node_data_2 = self.temp_list[1]
        if isinstance(node_data_1["piece"],pion_classe.Pion) and isinstance(node_data_2["piece"],pion_classe.Pion):
            if self.piece_can_switch(node_data_1,node_data_2):
                temp = node_data_1["piece"].getColor()
                node_data_1["piece"].setColor(node_data_2["piece"].getColor())
                node_data_2["piece"].setColor(temp)

                node_data_1["color"] = node_data_1["piece"].getColor()
                node_data_2["color"] = node_data_2["piece"].getColor()
                print("Vous avez échangé les pions")
    def check_if_nodes_are_adjacent(self,node_data_1,node_data_2):
        """
            Rien de compliqué. Cette fonction permet de savoir si deux noeuds sont adjacents basé sur leur 
                id et le fait que chaque noeud ait une liste de ses voisins
        """
        if node_data_1["id"] in node_data_2["neighbours"]:
            return True
        else:
            return False
    
    ### Fonction Phase 1: Verification de victoire
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
                            print(f'Voici les noeuds comparés ({node_data["id"]}:{color}),({neighbour_1_data["id"]},{neighbour_1_data["piece"].getColor()}),({neighbour_2_data["id"]},{neighbour_2_data["piece"].getColor()})')
                            node_data_position = node_data["rect"].center
                            neighbour_1_position = neighbour_1_data["rect"].center
                            neighbour_2_position = neighbour_2_data["rect"].center
                            if self.nodes_share_same_position(node_data_position,neighbour_1_position,neighbour_2_position):
                                print("Allignement de 3 pions en __1__ couches de la même couleur!")
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
                                    print(f'Voici les noeuds comparés ({node_data["id"]}:{color}),({neighbour_1_data["id"]},{neighbour_1_data["piece"].getColor()}),({neighbour_2_data["id"]},{neighbour_2_data["piece"].getColor()})')
                                    node_data_position = node_data["rect"].center
                                    neighbour_1_position = neighbour_1_data["rect"].center
                                    neighbour_2_position = neighbour_2_data["rect"].center
                                    if self.nodes_share_same_position(node_data_position,neighbour_1_position,neighbour_2_position):
                                        print("Allignement de 3 pions en __2__ couches de la même couleur!")
                                        return True
    def check_allignement(self,node_data):
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
        """
        if self.check_allignement(node_data=node_data):
            ### On ne vérifie la couleur du noeud que si il y a eu un alignement
            if node_data["piece"].getColor() == RED:
                print("Le joueur ROUGE a gagné!")
            else:
                print("Le joueur BLEU a gagné!")
            #self.running = False
            print("Fin du jeu")
    
    ### Fonction qui permet de faire des plays en tant qu'IA
    def choose_random_node_IA(self):
        """
            Cette fonction permet de choisir un noeud aléatoire sur le plateau. Pour ce faire, on génère 
                un nombre aléatoire entre 0 et le nombre de noeuds sur le plateau. On retourne ensuite 
                le noeud correspondant à ce nombre.
        """
        node_data_id = random.randint(0,len(self.nodes)-1)
        return self.nodes[node_data_id]
    def play_phase_0_IA(self):
        """
            Cette fonction fait en sorte que l'IA place un pion sur le plateau. Pour ce faire, on change 
                la couleur du noeud et du pion.
        """

        node_data = self.choose_random_node_IA()
        print(f'Voici le noeud sélectionné: {node_data["id"]}')
        while (isinstance(node_data["piece"],pion_classe.Pion) and node_data["piece"].getColor() != BRWON):
            node_data = self.choose_random_node_IA()
            print(f'Voici le noeud sélectionné: {node_data["id"]}')
        if node_data["piece"].getColor() == BRWON:
            self.change_piece_color(node_data)
            self.decrement_player_pions()
            self.switch_player()
            print("")

            self.is_there_winner(node_data)
        else:
            print("Vous ne pouvez pas placer de pion ici")
    def play_phase_1_IA(self): 
        self.switch_player()
    def play_the_turn_IA(self):
        """
            Cette fonction permet de jouer un tour, elle recoit en input le noeud sur lequel on a cliqué.
            Elle est appelée dans la fonction run().
            Elle permet de gérer les deux phases du jeu:
                - Phase 0: Placement des pions
                - Phase 1: Echange des pions
        """
        if(self.phase == 0):
            self.play_phase_0_IA()
        elif(self.phase == 1):
            self.play_phase_1_IA()
              
    ### Fonction qui permet de faire des plays en tant que joueur
    def play_phase_0(self,node_data):
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
            self.change_piece_color(node_data=node_data)
            self.decrement_player_pions()
            self.switch_player()
            print("")

            self.is_there_winner(node_data)
        else:
            print("Vous ne pouvez pas placer de pion ici")
    def play_phase_1(self,node_data):
        """
            Un peu plus compliqué. Cette fonction permet de déplacer les pions sur le plateau.
                Pour ce faire, on échange les pions de deux noeuds si et seulement si les deux noeuds
                sont adjacents et que l'un des deux noeuds est vide.
        """
        
        #print("Phase 1, on déplace les pions")
        if len(self.temp_list)==0:
            if isinstance(node_data["piece"],pion_classe.Pion) and node_data["piece"].getColor() == BRWON:
                print("Veulliez sélectionner un PREMIER pion aillant déja une couleur")
            else:
                self.temp_list.append(node_data)
                print("Vous avez sélectionné le pion", node_data["id"])
            return None
        else:
            if len(self.temp_list)==1 and self.temp_list[0]["id"] != node_data["id"]:
                self.temp_list.append(node_data)
                if self.check_if_nodes_are_adjacent(self.temp_list[0],self.temp_list[1]):
                    self.switch_pieces_nodes()
                    self.switch_player()

                    self.is_there_winner(self.temp_list[0])
                else:
                    print("Vous ne pouvez pas échanger ces pions car ils ne sont pas adjacents")
            else:
                print("Vous ne pouvez pas échanger ces pions car ils sont identiques")
            
            self.temp_list = [] #Dès qu'une erreur est faite, on vide la liste temporaire
    def play_the_turn_human(self,node_data):
        """
            Cette fonction permet de jouer un tour, elle recoit en input le noeud sur lequel on a cliqué.
            Elle est appelée dans la fonction run().
            Elle permet de gérer les deux phases du jeu:
                - Phase 0: Placement des pions
                - Phase 1: Echange des pions
        """
        if(self.phase == 0):
            self.play_phase_0(node_data=node_data)
        elif (self.phase==1):
            self.play_phase_1(node_data=node_data)
    
    
    ### Fonction pour afficher dans le terminal
    def print_nodes(self,nodes_dict):
        for node_id, node_data in nodes_dict.items():
            print(node_id, node_data)
    ### Fonction pour gérer les évènements (clavier, souris)
    def have_to_quit(self,event):
        if event.type == pygame.QUIT:
            self.running = False
            print("We hope you had fun!")
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.running = False
                print("We hope you had fun!")
    
    ### Fonction pour gérer le jeu
    def run(self):
        # Game loop
        node_color = RED #n'importe quelle couleur fonctionne, c'est juste pour initialiser
        while self.running:

            if self.who_play == 1:
                # C'est le tour de l'IA
                self.play_the_turn_IA()
            else:
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
                            """
                            node_id is the key, node_data is the value of the dictionary
                            rect is the key, the corresponding value is the rectangle node
                            color is the key and the corresponding value is the color of the node"""
                            if node_data["rect"].collidepoint(pos):
                                self.play_the_turn_human(node_data)

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

        # Quit Pygame
        pygame.quit()