import pygame 
pygame.init()

# images ---------------------------------------------------
icon = pygame.image.load('assets/turtle.png')

    # acceuil / choix carte
jouer_img = pygame.image.load('assets/bouton_jouer.png')

parametre_img = pygame.image.load('assets/bouton_parametre.png')

carte_plage_img = pygame.image.load('assets/carte_plage.png')
carte_plage_img_grand = pygame.transform.scale(carte_plage_img, (365, 336)) # largeur hauteur, cf figma
carte_plage_img_petit = pygame.transform.scale(carte_plage_img, (273, 252))

carte_nuit_img = pygame.image.load('assets/carte_nuit.png')
carte_nuit_img_grand = pygame.transform.scale(carte_nuit_img, (320, 340))
carte_nuit_img_petit = pygame.transform.scale(carte_nuit_img, (232, 237))

carte_foret_img = pygame.image.load('assets/carte_foret.png')
carte_foret_img_grand = carte_foret_img
carte_foret_img_petit = pygame.transform.scale(carte_foret_img, (207,216))

logo_app = pygame.image.load('assets/logo_clash_turtle.png')

precedent_img = pygame.image.load('assets/precedent.png')

    # paramètres
ecran_acceuil = pygame.image.load('assets/ecran_acceuil.png')
bg_parametre_img = pygame.image.load('assets/parametres.png')

son_ok = pygame.image.load('assets/son_ok.png')
son_moyen = pygame.image.load('assets/son_moyen.png')
son_nop = pygame.image.load('assets/son_nop.png')

j1 = pygame.image.load('assets/1_joueur.png')
j2 = pygame.image.load('assets/2_joueurs.png')

facile = pygame.image.load('assets/facile.png')
difficile = pygame.image.load('assets/difficile.png')

    # pre-jeu
titre_pre_jeu = pygame.image.load('assets/titre_pre_jeu.png')
touches = pygame.image.load('assets/touches.png')
commencer = pygame.image.load('assets/commencer.png')

    # jeu
overlay = pygame.image.load('assets/fond_overlay.png')

interdit = pygame.image.load('assets/interdit.png')

    # pre-questions
titre_pre_questions = pygame.image.load('assets/titre_pre_questions.png')
touches_pre_questions = pygame.image.load('assets/touches_pre_questions.png')

    # quesitions
liste_questions = [{"q":"9+4 = 12","r": "Faux"},{"q":"5x0 = 0","r": "Vrai"},{"q":"8-6 = 2","r": "Vrai"},
{"q":"4x4 = 14","r": "Faux"},{"q":"4+5 = 8","r": "Faux"},{"q":"7x5 = 49","r":"Faux"},{"q":"4x7 = 28","r":"Vrai"},
{"q":"3x8 = 27","r":"Faux"},{"q":"5x9 = 45","r":"Vrai"},{"q":"1x1 =2","r":"Faux"} ,{"q":"6x6 = 46","r":"Faux"},
{"q":"8x8 = 64","r":"Vrai"},{"q":"25+7 = 32","r":"Vrai"},{"q":"15+14 = 41","r":"Faux"},{"q":"15+5 = 20","r":"Vrai"},
{"q":"12-3 = 8","r":"Faux"},{"q":"un calcule","r":"Faux"},{"q":"un héléphant","r":"Faux"},{"q":"une pome","r":"Faux"},
{"q":"des bateaux","r":"Vrai"},{"q":"la fete","r":"Faux"},{"q":"milles","r":"Faux"},{"q":"une partie","r":"Vrai"},
{"q":"beaucoups","r":"Faux"},{"q":"tantôt","r":"Vrai"},{"q":"comment","r":"Vrai"},{"q":"jamait","r":"Faux"},
{"q":"parfois","r":"Vrai"},{"q":"une boulle","r":"Faux"},{"q":"voilà","r":"Vrai"},{"q":"un moulain","r":"Faux"},
{"q":"un craillon","r":"Faux"},{"q":"un ordinateur","r":"Vrai"},{"q":"des marteaus","r":"Faux"},
{"q":"des chevaux","r":"Vrai"},{"q":"des vélo","r":"Faux"},{"q":"un bombon","r":"Faux"},{"q":"des hélicoptères","r":"Vrai"},
{"q":"des cailloux","r":"Vrai"},{"q":"des hibous","r":"Faux"},{"q":"des clous","r":"Vrai"},{"q":"des fous","r":"Vrai"},
{"q":"9+9 = 18","r":"Vrai"},{"q":"18+5 = 25","r":"Faux"},{"q":"30+20 = 50","r":"Vrai"},{"q":"4+6 = 10","r":"Vrai"},
{"q":"10+25 = 45","r":"Faux"},{"q":"20x10 = 200","r":"Vrai"},{"q":"70+7 = 77","r":"Vrai"},{"q":"21+2 = 24","r":"Faux"},
{"q":"6+6 = 66","r":"Faux"},{"q":"5x9 = 45","r":"Vrai"},{"q":"7-5 = 2","r":"Vrai"},{"q":"12-2 = 9","r":"Faux"},
{"q":"19-5 = 15","r":"Faux"},{"q":"100-100 = 0","r":"Vrai"},{"q":"10+90 = 100","r":"Vrai"},{"q":"20-3 = 13","r":"Faux"},
{"q":"10-5 = 5","r":"Vrai"},{"q":"8-7 = 1","r":"Vrai"},{"q":"15-5 = 8","r":"Faux"},{"q":"14-5 = 9","r":"Vrai"},
{"q":"8x8 = 64","r":"Vrai"},{"q":"9x1 = 10","r":"Faux"},{"q":"2x20 = 40","r":"Vrai"},{"q":"7x3 = 21","r":"Vrai"},
{"q":"6x5 = 35","r":"Faux"},{"q":"5x7 = 35","r":"Vrai"},{"q":"9x0 = 0","r":"Vrai"},{"q":"2x8 = 16","r":"Vrai"},
{"q":"4x9 = 36","r":"Vrai"},{"q":"4x100 = 400","r":"Vrai"},{"q":"4x100 = 500","r":"Faux"},{"q":"une adition","r":"Faux"},
{"q":"des girafes","r":"Vrai"},{"q":"des poires","r":"Vrai"},{"q":"des bulle","r":"Faux"},{"q":"la campagnes","r":"Faux"},
{"q":"un centime","r":"Vrai"},{"q":"un pantalon","r":"Vrai"},{"q":"une soustracsion","r":"Faux"},{"q":"des hartichauds","r":"Faux"},
{"q":"les tortues","r":"Vrai"},{"q":"une cour","r":"Vrai"},{"q":"j’avait","r":"Faux"},{"q":"tu manges","r":"Vrai"},
{"q":"les chaussetes","r":"Faux"},{"q":"du pain","r":"Vrai"},{"q":"un stylo","r":"Vrai"},{"q":"des livre","r":"Faux"},
{"q":"il travaille","r":"Vrai"},{"q":"nous arrivont","r":"Faux"},{"q":"ils changes","r":"Faux"}]

    # post-jeu
medailles_img = pygame.image.load('assets/medailles.png')
bouton_retour_au_menu_img = pygame.image.load('assets/bouton_retour_au_menu.png')
bouton_rejouer_img = pygame.image.load('assets/bouton_rejouer.png')

# polices d'écritures --------------------------------------
font = "assets/mochiy_pop_p_one.ttf"

# couleurs -------------------------------------------------
fond_jeu = (206,255,205)