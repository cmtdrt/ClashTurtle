import pygame

def texte(text, size, color, surface, x, y, font=None):
    """affiche un texte personnalisé sur une surface
    text: str, size: int, color, tuple de 3 int(0 <= x <= 255)
    surface: pygame.surface, x: int ou "center", y: int ou "center", font: fichier.ttf
    """
    font2 = pygame.font.Font(font, size)
    textobj = font2.render(text, 1, color)
    textrect = textobj.get_rect()
    if x == "center":
        x = surface.get_width()/2 - int(textrect.width)/2
    if y == "center":
        y = surface.get_height()/2 - int(textrect.height)/2
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)


class Joueur(pygame.sprite.Sprite):
    """classe principale du jeu
    image: ficher.png, touche: liste de touches accordées, x: int, y: int"""
    def __init__(self, image, touches, x, y):
        super().__init__()
        self.image = image
        self.touches = touches
        self.position = [x, y]
        self.old_position = self.position.copy()
        self.delta_x, self.delta_y = 0, 0
        self.rect = self.image.get_rect()
        self.rect.topleft = self.position
        self.check = [0,0,0,0]
        self.tour = 0
        self.chrono = 0
    

    def colisions(self, walls):
        """permet de gerer les colision sur des mur et de glisser dessus si possible
        walls: liste de pygame.Rect"""
        testx, testy = self.rect.copy(), self.rect.copy() 
        testx.topleft = [testx[0], self.old_position[1]]
        testy.topleft = [self.old_position[0], testy[1]]

        if testx.collidelist(walls) == -1: # test en x
            self.position = [testx[0], self.old_position[1]]
            self.delta_y *= 0.9
        elif testy.collidelist(walls) == -1: # test en y
            self.position = [self.old_position[0], testy[1]]
            self.delta_x *= 0.9
        else : # dans un coin
            self.position = self.old_position
            
        self.rect.topleft = self.position


    def update_pos(self, touche, vitesse_max, increment, frottement, image):
        """permet de faire déplacer le joueur et de simuler une inertie
        touche: liste des touches enfoncées, vittesse_max: int, increment: int,
        frotement: int < increment, image: fichier.png"""
        assert increment > frottement
        
        self.old_position = self.position.copy() # sauvegarde de la position pour colisions()

        # addition de l'incrément dans tout les sens
        if abs(self.delta_x) < vitesse_max:
            if touche[self.touches[0]]:
                    self.image = pygame.transform.rotate(image,270)
                    self.delta_x += increment
            elif touche[self.touches[1]]:
                    self.image = pygame.transform.rotate(image,90)
                    self.delta_x -= increment
                
        if abs(self.delta_y) < vitesse_max:
            if touche[self.touches[2]]:
                    self.image = image
                    self.delta_y -= increment
            if touche[self.touches[3]]:
                    self.image = pygame.transform.rotate(image,180)
                    self.delta_y += increment          

        # soustraction du frottement
        if abs(self.delta_x) <= frottement: # eviter un clignotement
            self.delta_x = 0
        elif self.delta_x < frottement :
            self.delta_x += frottement 
        elif self.delta_x > frottement:
            self.delta_x -= frottement
        
        if abs(self.delta_y) <= frottement: # eviter un clignotement
            self.delta_y = 0
        elif self.delta_y <= frottement:
            self.delta_y += frottement
        elif self.delta_y >= frottement:
            self.delta_y -= frottement


        # addition des delta finaux
        self.position[0] += self.delta_x
        self.position[1] += self.delta_y

        # mise a jour de la position
        self.rect.topleft = self.position

        
    def update_pos_simple(self, touche, increment, image):
        """permet de faire déplacer le joueur sans prendre en compte l'inertie
        touche: liste des touches enfoncées, increment: int, image: fichier.png"""

        self.old_position = self.position.copy() # sauvegarde de la position pour colisions()
        self.delta_x, self.delta_y = 0,0 # reinitialisation des delta

        # addition de l'incrément dans tout les sens
        if touche[self.touches[0]]:
            self.delta_x += increment
            self.image = pygame.transform.rotate(image,270)
        if touche [self.touches[1]]:
            self.delta_x -= increment
            self.image = pygame.transform.rotate(image,90)
        if touche[self.touches[2]]:
            self.delta_y -= increment
            self.image = image
        if touche[self.touches[3]]:
            self.delta_y += increment
            self.image = pygame.transform.rotate(image,180)

        self.position[0] += self.delta_x
        self.position[1] += self.delta_y
        
        # mise a jour de la position
        self.rect.topleft = self.position



class Joueur_questions():
    """classe secondaire du jeu servant pour la phase de questions
    image: ficher.png, touches: touche: liste de touches accordées,
    position: tuple de 2 int"""

    def __init__(self, image, touches, position):
        self.image = image
        self.touches = touches
        self.position = position
        self.choix = 0      
        
    def blit(self,screen):
        """afficher le joueur sur l'écran"""
        screen.blit(self.image, self.position)
        
    def update_choix(self, touche, image):
        """mettre a jour le choix du joueur et son orientation"""

        if touche[self.touches[0]]: # gauche
            self.choix = "Faux"
            self.image = pygame.transform.rotate(image,270)
    
        if touche [self.touches[1]]: # droite
            self.choix = "Vrai"
            self.image = pygame.transform.rotate(image,90)