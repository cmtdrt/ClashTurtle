#programme du jeu Clash Turtle
#si main.py ne fonctionne pas, faire clique droit sur le dossier "Clash Turtle" puis "ouvrir avec" ide


# Setup Python ----------------------------------------------- #
import datetime
from math import sqrt
import time
import pyscroll
import pytmx
import pygame
pygame.init()
pygame.font.init()
from pygame.locals import *
import objets                          # fonction qui pourrait servir pour le tableau des scores
from charger_assets import *           #permet de gagner en lisibilitee ici
# from pyvidplayer import Video        #ne fonctionne pas chez moi


# Setup pygame/window ---------------------------------------- #
mainClock = pygame.time.Clock()                        # declaration de la clock
largeur, hauteur = 450, 800                            # utile pour centrer une image par ex
screen = pygame.display.set_mode((largeur, hauteur))   # variable relative a la fenetre
pygame.display.set_icon(icon)


#variables principales --------------------------------------- #
img_carte_selectionnee = carte_plage_img_grand            # memoire du changement de carte
data_carte_selectionnee = {"chemin" : "map_plage/plageV2.tmx", "musique" : "assets/curiosidad.wav", "zoom_min" : [0.32,1.89], "zoom_max" : 1.4 , "depart" : [270,600]}
son_selectionne = son_ok
joueur_selectionne = j2
difficulte_selectionne = facile

#musique de fond -- en .wav
pygame.mixer.music.load("assets/curiosidad.wav")          #utiliser mixer.Sound pour les bruitages
pygame.mixer.music.play(-1)                            # -1 = en boucle


def tirage_couleurs():
    global tortue_2_img_grand, tortue_2_img, tortue_1_img_grand, tortue_1_img
    liste_couleurs = ["rouge", "bleu", "bleu_ciel", "grise", "jaune", "noir", "orange", "rose", "violette"]
    couleurs_choisies = random.sample(liste_couleurs, 2)

    tortue_2_img_grand = pygame.image.load('assets/tortue_' + couleurs_choisies[0] + '.png')
    tortue_2_img = pygame.transform.scale(tortue_2_img_grand, (20,20))
    tortue_1_img_grand = pygame.image.load('assets/tortue_' + couleurs_choisies[1] + '.png')
    tortue_1_img = pygame.transform.scale(tortue_1_img_grand, (20,20))


def menu_principal():
    global img_carte_selectionnee
    pygame.display.set_caption('Clash Turtle - Menu principal')   #titre de la fenetre

    # mise en page ------------------------------------------- #
    # mettre en dehors de la boucle tout les element fixes, qui ne bougeront pas
    screen.fill(fond_jeu)                           # fond de la fenetre
    screen.blit(logo_app, (133, 30))                # blit = afficher quelque chose sur la fenetre cf ligne 17

    bouton_jouer = screen.blit(jouer_img, (39,531)) # afficher l'image et stocker ses coordonnees dans la variable
    bouton_parametre = screen.blit(parametre_img, (26,26))
    if img_carte_selectionnee != carte_foret_img_grand: # gerer la difference de taille avec la derniere carte
        bouton_carte = screen.blit(img_carte_selectionnee, (61,203))
    else:
        bouton_carte = screen.blit(carte_foret_img_grand, (80, 250))

    while True: # boucle du jeu
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:                 # commandes relatives aux touches
                if event.key == K_ESCAPE:
                    pygame.quit()
            if event.type == MOUSEBUTTONDOWN:         # commandes relatives a la souris
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()

        if click:                                     # interaction avec les bouttons
            if bouton_jouer.collidepoint((mx, my)):
                tirage_couleurs()
                if joueur_selectionne == j2:
                    pre_jeu()
                else:
                    jeu()
            if bouton_carte.collidepoint((mx, my)):
                choix_carte()
            if bouton_parametre.collidepoint((mx, my)):
                parametres()

        pygame.display.update()
        mainClock.tick(60)


def parametres():
    global son_selectionne
    global joueur_selectionne
    global difficulte_selectionne
    
    # mise en page ------------------------------------------- #
    screen.fill(fond_jeu)
    screen.blit(ecran_acceuil, (0, 0))
    parametres = screen.blit(af_parametre_img, (44, 207))
    bouton_son = screen.blit(son_selectionne, (298, 469))
    bouton_joueur = screen.blit(joueur_selectionne, (260, 356))
    bouton_difficulte = screen.blit(difficulte_selectionne, (263,421))

    while True:
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:                 # commandes relatives aux touches
                if event.key == K_ESCAPE:
                    menu_principal()
            if event.type == MOUSEBUTTONDOWN:         # commandes relatives a la souris
                if event.button == 1:
                    click = True
        
        mx, my = pygame.mouse.get_pos()

        if click:
            if parametres.collidepoint((mx, my)) == False:  # si click a cote
                menu_principal()
            
            # volume ----------------------------------------------------------
            if bouton_son.collidepoint((mx, my)) and son_selectionne == son_ok:    # gerer les diferentes niveau de volume
                son_selectionne = son_moyen
                pygame.mixer.music.set_volume(0.25)
                screen.fill((255,255,255), bouton_son)
                screen.blit(son_moyen, (298, 469))
            elif bouton_son.collidepoint((mx, my)) and son_selectionne == son_moyen:
                son_selectionne = son_nop
                pygame.mixer.music.set_volume(0)
                screen.fill((255,255,255), bouton_son)
                screen.blit(son_nop, (298, 469))
            elif bouton_son.collidepoint((mx, my)):
                son_selectionne = son_ok
                pygame.mixer.music.set_volume(1)
                screen.fill((255,255,255), bouton_son)
                screen.blit(son_ok, (298, 469))

            # mode de jeu ------------------------------------------------------
            if bouton_joueur.collidepoint((mx, my)) and joueur_selectionne == j2:
                joueur_selectionne = j1
                screen.fill((255,255,255), (260,356,130,22))
                screen.blit(j1, (260, 356))
            elif bouton_joueur.collidepoint((mx, my)) and joueur_selectionne == j1:
                joueur_selectionne = j2
                screen.fill((255,255,255), bouton_joueur)
                screen.blit(j2, (260, 356))

            # dificulté ---------------------------------------------------------
            
            if bouton_difficulte.collidepoint((mx, my)) and difficulte_selectionne == facile:
                difficulte_selectionne = difficile
                screen.fill((255,255,255), (263,421, 109,23))
                screen.blit(difficile, (263, 421))
            elif bouton_difficulte.collidepoint((mx, my)) and difficulte_selectionne == difficile:
                difficulte_selectionne = facile
                screen.fill((255,255,255), (263,421, 109,23))
                screen.blit(facile, (263, 421))


        pygame.display.update()
        mainClock.tick(60)


def pre_jeu():
    pygame.display.set_caption('Clash Turtle - A vos touches !')
    screen.fill(fond_jeu)

    screen.blit(titre_pre_jeu, (40, 65))
    screen.blit(touches, (19,543))

    bouton_precedent = screen.blit(precedent_img, (26, 26))
    # zqsd_animation = Video("ZQSD_Animation.mp4")    #cf ligne 11
    # zqsd_animation.draw(screen, (18, 543))

    check_j1, check_j2 = False, False

    while True:
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:       # (touche au dessus de entrer)
                    menu_principal()
                if event.key == K_RETURN and check_j1 and check_j2:
                    jeu()
            if event.type == MOUSEBUTTONDOWN :
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] or keys[pygame.K_DOWN] or keys[pygame.K_UP]:
            screen.fill(fond_jeu, (225,543,209,133))
            screen.blit(tortue_1_img_grand,(255,497))
            check_j1 = True
        if keys[pygame.K_z] or keys[pygame.K_q] or keys[pygame.K_s] or keys[pygame.K_d]:
            screen.fill(fond_jeu, (16,543,209,133))
            screen.blit(tortue_2_img_grand,(30,497))
            check_j2 = True
        
        if check_j1 and check_j2: 
            bouton_commencer = screen.blit(commencer, (56,330))


        if click :
            if check_j1 and check_j2:
                if bouton_commencer.collidepoint((mx,my)):
                    jeu()
            if bouton_precedent.collidepoint((mx, my)):
                menu_principal()
                
        pygame.display.update()
        mainClock.tick(60)


def choix_carte():
    global img_carte_selectionnee
    global data_carte_selectionnee
    pygame.display.set_caption('Clash Turtle - Choix de carte')

    # mise en page ------------------------------------------- #
    screen.fill(fond_jeu)
    carte_plage = screen.blit(carte_plage_img_petit, (109, 38))
    carte_nuit = screen.blit(carte_nuit_img_petit, (110, 302))
    carte_foret = screen.blit(carte_foret_img_petit, (130, 554))
    bouton_precedent = screen.blit(precedent_img, (26, 26))

    while True:
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    pygame.quit()
            if event.type == MOUSEBUTTONDOWN:
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()

        if click:
            if carte_plage.collidepoint((mx, my)):
                if img_carte_selectionnee != carte_plage_img_grand:
                    data_carte_selectionnee = {"chemin" : "map_test/essai2.tmx", "musique" : "assets/curiosidad.wav", "zoom_min" : [0.32,1.89], "zoom_max" : 1.4 , "depart" : [270,600]}
                    pygame.mixer.music.load("assets/curiosidad.wav")
                    pygame.mixer.music.play(-1)
                    img_carte_selectionnee = carte_plage_img_grand
                menu_principal()

            if carte_nuit.collidepoint((mx, my)):
                if img_carte_selectionnee != carte_nuit_img_grand:
                    data_carte_selectionnee = {"chemin" : "IceMap/IceMap.tmx", "musique" : "assets/nuit.wav", "zoom_min" : [0.45, 0.45], "zoom_max" : 2,"depart" : [436, 863]}
                    pygame.mixer.music.load("assets/nuit.wav")
                    pygame.mixer.music.play(-1)
                    img_carte_selectionnee = carte_nuit_img_grand
                menu_principal()

            if carte_foret.collidepoint((mx, my)):
                if img_carte_selectionnee != carte_foret_img_grand:
                    data_carte_selectionnee = {"chemin" : "Foret/Forestmap.tmx", "musique" : "assets/soupe.wav", "zoom_min" : [0.32, 0.32], "zoom_max" : 2,"depart" : [625, 551]}
                    pygame.mixer.music.load("assets/soupe.wav")                      
                    pygame.mixer.music.play(-1)
                    img_carte_selectionnee = carte_foret_img_grand
                menu_principal()

            if bouton_precedent.collidepoint((mx, my)):
                menu_principal()

        pygame.display.update()
        mainClock.tick(60)


def jeu():
    global chrono1, chrono2
    # initialisation ---------------------------------------------------------
    pygame.display.set_caption('Clash Turtle - Course')

    #charger la carte et ses dependances
    tmx_data = pytmx.util_pygame.load_pygame(data_carte_selectionnee["chemin"])
    map_data = pyscroll.data.TiledMapData(tmx_data)
    map_layer = pyscroll.orthographic.BufferedRenderer(map_data, screen.get_size())
    #initialiser les colisions
    walls, finish, checkpoint1, checkpoint2, checkpoint3, checkpoint4, boost, slow = [], [], [], [], [], [], [], []

    for obj in tmx_data.objects:
        if obj.type == "collision":
            walls.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        if obj.type == "finish":
            finish.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        if obj.type == "checkpoint1":
            checkpoint1.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        if obj.type == "checkpoint2":
            checkpoint2.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        if obj.type == "checkpoint3":
            checkpoint3.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        
        if obj.type == "checkpoint4":
            checkpoint4.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        if obj.type == "boost":
            boost.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))

        if obj.type == "slow":
            slow.append(pygame.Rect(obj.x, obj.y, obj.width, obj.height))
        

    #charger les joueurs
    if joueur_selectionne == j2:
        tortue1 = objets.Joueur(tortue_1_img, [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN], data_carte_selectionnee["depart"][0]+20, data_carte_selectionnee["depart"][1])
        tortue2 = objets.Joueur(tortue_2_img, [pygame.K_d, pygame.K_q, pygame.K_z, pygame.K_s], data_carte_selectionnee["depart"][0]-20, data_carte_selectionnee["depart"][1]) #935, 1155
        #unifier le tout
        group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 3)
        group.add(tortue1, tortue2)
    
    else:
        tortue1 = objets.Joueur(tortue_1_img, [pygame.K_RIGHT, pygame.K_LEFT, pygame.K_UP, pygame.K_DOWN], data_carte_selectionnee["depart"][0], data_carte_selectionnee["depart"][1])
        group = pyscroll.PyscrollGroup(map_layer = map_layer, default_layer = 3)
        group.add(tortue1)
        
    pygame.mixer.music.load("assets/mario.wav")
    pygame.mixer.music.play(-1)

   

    # annimation avant course--------------------------------------------------
    t_depart = datetime.datetime.now()

    zoom = data_carte_selectionnee["zoom_min"][0]
    x_overlay = -55
    
    boost1 = 0
    boost2 = 0
    slow1 = 0
    slow2 = 0
    
    while True:
        t_now = (t_depart-datetime.datetime.now()-datetime.timedelta(seconds = 4))

        t_4 = datetime.timedelta(-1,54,0,0,59,23)

        if  t_now < t_4 and zoom < data_carte_selectionnee["zoom_max"]: 
            zoom += 0.02

        if t_now < t_4 and x_overlay < 14:
            x_overlay += 1
            
        if str(t_now)[15:16] == "0":
            break
        
        
        map_layer.zoom = zoom
        if joueur_selectionne == j2:
            group.center(((tortue1.position[0] + tortue2.position[0])/2, (tortue1.position[1] + tortue2.position[1])/2))
        else:
            group.center(tortue1.position)
        

        group.draw(screen)
        
        screen.blit(overlay, (60, x_overlay))
        objets.texte("0:00.00", 24, (0,0,0), screen, 90, x_overlay+8, font)
        objets.texte("0/3", 24, (0,0,0), screen, 285, x_overlay+8, font)
        
        objets.texte(str(t_now)[15:16], 80, (0,0,0), screen, 205, 250, font)

        pygame.display.update()
        mainClock.tick(60)
    

    # course--------------------------------------------------

    t_depart = datetime.datetime.now()
    zoom_x, zoom_y  = zoom, zoom
    lag_normal, lag_fin = 0.015, 0.015 
    # myfont = pygame.font.SysFont('Comic Sans MS', 30)
    boucle = True
    
    
    while boucle:
        # click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:
                    boucle = False
        

        # ZOOM AUTOMATIQUE ===================================================================================
        zoom, zoom_y, zoom_x = min(zoom_x, zoom_y), min(zoom_x, zoom_y), min(zoom_x, zoom_y)
        map_layer.zoom = zoom # NE PAS METTRE CETTE LIGNE APRES group.center !
        
        if joueur_selectionne == j2:
            group.center(((tortue1.position[0] + tortue2.position[0])/2, (tortue1.position[1] + tortue2.position[1])/2))
            # group.center(tortue1.rect.center)
            
            if (sqrt((tortue1.position[0] - tortue2.position[0])**2) * zoom) >= 200 and zoom > data_carte_selectionnee["zoom_min"][0]:
                zoom_x -= 0.02 if zoom_x > 1 else 0.01
            elif ((sqrt((tortue1.position[0] - tortue2.position[0])**2) * zoom) < 180) and zoom < data_carte_selectionnee["zoom_max"]: #and zoom_x <= zoom_y 
                zoom_x += 0.02 if zoom_x > 1 else 0.01
            if (sqrt((tortue1.position[1] - tortue2.position[1])**2) * zoom) >= 500 and zoom > data_carte_selectionnee["zoom_min"][1]:            
                zoom_y -= 0.02 if zoom_y > 1 else 0.01
            elif (sqrt((tortue1.position[1] - tortue2.position[1])**2) * zoom) < 480 and zoom < data_carte_selectionnee["zoom_max"]: #and zoom_y <= zoom_x
                zoom_y += 0.02 if zoom_y > 1 else 0.01
        
        else:
            if zoom < data_carte_selectionnee["zoom_max"]:
                zoom_x += 0.02 
                zoom_y += 0.02
            group.center(tortue1.position)
        

        # DEPLACEMENTS =======================================================================================
        keys = pygame.key.get_pressed()
        
        lag = (60/mainClock.get_fps())
        if joueur_selectionne == j2:
            if difficulte_selectionne == difficile:
                tortue1.update_pos(keys, lag*5, lag*(0.05+boost1+slow1), lag*0.03, tortue_1_img)
                tortue2.update_pos(keys, lag*5, lag*(0.05+ boost2+slow2), lag*0.03, tortue_2_img)
            else:
                tortue1.update_pos_simple(keys, lag*(4+boost1+slow1), tortue_1_img)
                tortue2.update_pos_simple(keys, lag*(4+boost2+slow2), tortue_2_img)
        
        else:
            if difficulte_selectionne == difficile:
                tortue1.update_pos(keys, lag*5, lag*(0.05+boost2), lag*0.03, tortue_1_img)
            else:
                tortue1.update_pos_simple(keys, lag*(4+boost1+slow1), tortue_1_img)


        # COLISIONS ==========================================================================================
        for sprite in group.sprites():
            if sprite.rect.collidelist(walls) > -1:
                sprite.colisions(walls)
                bruit = pygame.mixer.Sound("assets/collision.wav")
                bruit.play()

            if sprite.rect.collidelist(finish) >= 0:
                if sprite.check == [1,1,1,1]:
                    sprite.tour += 1
                    if sprite.tour == 1 and sprite == tortue1:
                        chrono1 = t_now
                    elif sprite.tour == 1 and sprite == tortue2:
                        chrono2 = t_now
                sprite.check = [0,0,0,0]
        
            if sprite.rect.collidelist(checkpoint1) >= 0:
                print("checkpoint1")
                sprite.check[0] = 1
            if sprite.rect.collidelist(checkpoint2) >= 0:
                print("checkpoint2")
                sprite.check[1] = 1
            if sprite.rect.collidelist(checkpoint3) >= 0:
                print("checkpoint3")
                sprite.check[2] = 1
            if sprite.rect.collidelist(checkpoint4) >= 0:
                print("checkpoint4")
                sprite.check[3] = 1
        
        boost1 = 0
        boost2 = 0        
        
        for sprite in group.sprites():
            if sprite.rect.collidelist(boost) > -1:
                # sprite.boost(boost)
                if sprite == tortue1:
                    boost1 = 2 if difficulte_selectionne == facile else 0.04
                elif sprite == tortue2:
                    boost2 = 2 if difficulte_selectionne == facile else 0.04

        slow1 = 0
        slow2 = 0        
                
        for sprite in group.sprites():
            if sprite.rect.collidelist(slow) >= 0:
                # sprite.slow(slow)
                if sprite == tortue1:
                    slow1 = -1 if difficulte_selectionne == facile else -0.015
                elif sprite == tortue2:
                    slow2 = -1 if difficulte_selectionne == facile else -0.015


        # AFFICHAGES =========================================================================================
        t_now = (datetime.datetime.now()-t_depart)

        group.draw(screen)


        if joueur_selectionne == j2:
            deriere = False if tortue1.position[1]*zoom >= 70 and tortue2.position[1]*zoom >= 70 else True
            if min(tortue1.tour, tortue2.tour) == 1: boucle = False
        if joueur_selectionne == j1:
            deriere = False if tortue1.position[1]*zoom >= 70 else True
            if tortue1.tour == 1: boucle = False

        if deriere == False:
            if x_overlay <= 14:
                x_overlay += 1
            compte_tour = max(tortue1.tour, tortue2.tour) if joueur_selectionne == j2 else tortue1.tour
            screen.blit(overlay, (60, x_overlay))
            objets.texte(str(t_now)[3:10], 24, (0,0,0), screen, 90, x_overlay+8, font)
            objets.texte(str(compte_tour) + "/3", 24, (0,0,0), screen, 285, x_overlay+8, font)

        if t_now < datetime.timedelta(seconds = 2):
            objets.texte("GO !", 80, (0,0,0), screen, 150,250, font)


        
                
        pygame.display.flip()
        # pygame.display.update()
        mainClock.tick(60)



    # annimation après course--------------------------------------------------
    while True:
            
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()


        if map_layer.zoom < data_carte_selectionnee["zoom_min"][0]:
            time.sleep(1)
            # fin_jeu(t_now, tortue_1_img_grand, tortue_2_img_grand)
            if joueur_selectionne == j2:
                pre_questions()
            else: questions()
        map_layer.zoom -= 0.01

        if x_overlay > -55:
            x_overlay -= 1


        if joueur_selectionne == j2:
            group.center(((tortue1.position[0] + tortue2.position[0])/2, (tortue1.position[1] + tortue2.position[1])/2))
        else:
            group.center(tortue1.position)
        
        keys = pygame.key.get_pressed()
        
        lag = (60/mainClock.get_fps())
        if joueur_selectionne == j2:
            if difficulte_selectionne == difficile:
                tortue1.update_pos(keys, lag*5, lag*0.05, lag*0.03, tortue_1_img)
                tortue2.update_pos(keys, lag*5, lag*0.05, lag*0.03, tortue_2_img)
            else:
                tortue1.update_pos_simple(keys, lag*2, tortue_1_img)
                tortue2.update_pos_simple(keys, lag*2, tortue_2_img)
        else:
            if difficulte_selectionne == difficile:
                tortue1.update_pos(keys, lag*5, lag*0.05, lag*0.03, tortue_1_img)
            else:
                tortue1.update_pos_simple(keys, lag*2, tortue_1_img)

        
        for sprite in group.sprites():
            if sprite.rect.collidelist(walls) > -1:
                sprite.colisions(walls)


        group.draw(screen)

        screen.blit(overlay, (60, x_overlay))
        objets.texte(str(t_now)[3:10], 24, (0,0,0), screen, 90, x_overlay+8, font)
        objets.texte("0/3", 24, (0,0,0), screen, 285, x_overlay+8, font)
        
        pygame.display.flip()
        mainClock.tick(60)


def pre_questions():
    pygame.display.set_caption('Clash Turtle - Question !')
    screen.fill(fond_jeu)

    screen.blit(titre_pre_questions, (40, 65))
    screen.blit(touches_pre_questions, (19,543))

    check_j1, check_j2 = False, False

    while True:
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:
                if event.key == K_BACKSPACE:       # (touche au dessus de entrer)
                    menu_principal()
                if event.key == K_RETURN and check_j1 and check_j2:
                    questions()
            if event.type == MOUSEBUTTONDOWN :
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] or keys[pygame.K_RIGHT] :
            screen.fill(fond_jeu, (225,543,209,133))
            screen.blit(tortue_1_img_grand,(255,497))
            check_j1 = True
        if keys[pygame.K_q] or keys[pygame.K_d]:
            screen.fill(fond_jeu, (16,543,209,133))
            screen.blit(tortue_2_img_grand,(30,497))
            check_j2 = True
        
        if check_j1 and check_j2: 
            bouton_commencer = screen.blit(commencer, (56,330))

        if click :
            if check_j1 and check_j2:
                if bouton_commencer.collidepoint((mx,my)):
                    questions()
                
        pygame.display.update()
        mainClock.tick(60)


def questions():
    global tortue_1_img_grand, tortue_2_img_grand, malus1, malus2
    pygame.display.set_caption('Clash Turtle - Questions')
    
    if joueur_selectionne == j2:
        tortue1 = objets.Joueur_questions(tortue_1_img_grand, [pygame.K_RIGHT, pygame.K_LEFT], (145,324))
        tortue2 = objets.Joueur_questions(tortue_2_img_grand, [pygame.K_d, pygame.K_q], (145,550))
    else: 
        tortue1 = objets.Joueur_questions(tortue_1_img_grand, [pygame.K_RIGHT, pygame.K_LEFT], (145,442))
    
    choisies = random.sample(liste_questions, 3) # nombre de questions affichées
    malus1, malus2 = 0,0
    
    for question in choisies:
        pygame.mixer.music.load("assets/compte_a_rebours.wav")
        pygame.mixer.music.play(1)
        screen.fill(fond_jeu)
        i = 0
        if joueur_selectionne == j2:
            tortue1.image, tortue2.image = tortue_1_img_grand, tortue_2_img_grand
            tortue1.choix, tortue2.choix = 0,0
        else: 
            tortue1.image, tortue1.choix = tortue_1_img_grand, 0

        while i < 800:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()

            keys = pygame.key.get_pressed()
            
            screen.fill(fond_jeu)
            screen.fill((132,244,129), (0,0,450,i))
            objets.texte("Question !", 40, (0,0,0), screen, "center", 55, font)
            objets.texte(question["q"], 30, (0,0,0), screen, "center", 149, font)
            objets.texte("Vrai", 30, (0,0,0), screen, 46, 503, font)
            objets.texte("Faux", 30, (0,0,0), screen, 324, 503, font)

            
            tortue1.update_choix(keys, tortue_1_img_grand)
            tortue1.blit(screen)
            if joueur_selectionne == j2:
                tortue2.update_choix(keys, tortue_2_img_grand)
                tortue2.blit(screen)
                
            i += (800/(10*mainClock.get_fps()))
            mainClock.tick(60)
            pygame.display.update()
            
            
        
        if tortue1.choix != question["r"]:
            malus1 += 1
            print("raté1")
        if joueur_selectionne == j2 and tortue2.choix != question["r"]:
            malus2 += 1
            print("raté2")
        
        i = 0
        while i < 800:
            
            screen.fill((132,244,129))
            screen.fill(fond_jeu, (0,0,450,i))
            objets.texte("Réponse !", 40, (0,0,0), screen, "center", 55, font)
            objets.texte(question["q"], 30, (0,0,0), screen, "center", 149, font)
            objets.texte(question["r"], 30, (0,0,0), screen, "center", 221, font)

            tortue1.blit(screen)
            if joueur_selectionne == j2:
                tortue2.blit(screen)
            
            i += (10/3)
            mainClock.tick(60)
            pygame.display.update()
    
    fin_jeu()


def fin_jeu(): 
    global chrono1, chrono2
    

    # pygame.mixer.music.load("assets/marseillaise-meme.wav")
    pygame.mixer.music.play(-1)

    pygame.display.set_caption('Clash Turtle - Fin du jeu')
    screen.fill(fond_jeu)
    objets.texte("Résultat", 40, (0,0,0), screen, "center", 53, font)
    bouton_retour_au_menu = screen.blit(bouton_retour_au_menu_img,(40,664))
    bouton_rejouer = screen.blit(bouton_rejouer_img,(240,664))

    chrono1 += datetime.timedelta(seconds = 5) * malus1

    if joueur_selectionne == j2:
        # calculs
        chrono2 += datetime.timedelta(seconds = 5) * malus2

        if chrono1 <= chrono2:
            gagnant, gagnant_chrono = tortue_1_img_grand, chrono1
            deuxieme, deuxieme_chrono = tortue_2_img_grand, chrono2

        else:
            gagnant, gagnant_chrono = tortue_2_img_grand, chrono2
            deuxieme, deuxieme_chrono = tortue_1_img_grand, chrono1

        objets.texte(str(gagnant_chrono)[3:10], 30, (0,0,0), screen, "center", 126, font)
        screen.blit(medailles_img,(55,219))
        screen.blit(gagnant,(210,191))
        screen.blit(deuxieme,(210,422))
        objets.texte(str(deuxieme_chrono)[3:10], 20, (0,0,0), screen, 248, 587, font)

    else:
        screen.blit(tortue_1_img_grand,(146,269))
        objets.texte(str(chrono1)[3:10], 30, (0,0,0), screen, "center", 446, font)

    while True:
        click = False
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
            if event.type == KEYDOWN:                 # commandes relatives aux touches
                if event.key == K_ESCAPE:
                    pygame.mixer.music.load(data_carte_selectionnee["musique"])
                    pygame.mixer.music.play(-1)
                    menu_principal()
            if event.type == MOUSEBUTTONDOWN:         # commandes relatives a la souris
                if event.button == 1:
                    click = True

        mx, my = pygame.mouse.get_pos()
        
        
        if click:
            if bouton_retour_au_menu.collidepoint((mx,my)):
                pygame.mixer.music.load(data_carte_selectionnee["musique"])
                pygame.mixer.music.play(-1)
                menu_principal()
            if bouton_rejouer.collidepoint((mx, my)):
                tirage_couleurs()
                if joueur_selectionne == j2:
                    pre_jeu()
                else:
                    jeu()
        pygame.display.update()
        mainClock.tick(60)


menu_principal()