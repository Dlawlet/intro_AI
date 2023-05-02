class Pion:
    def __init__(self, couleur, position_x, position_y):
        self.couleur = couleur
        self.position_x = position_x
        self.position_y = position_y

    def getColor(self):
        return self.couleur
    def getPosX(self):
        return self.position_x
    def getPosY(self):
        return self.position_y
    def setPosX(self, new_x):
        self.position_x = new_x
    def setPosY(self, new_y):
        self.position_y = new_y
    def setColor(self, new_color):
        self.couleur = new_color