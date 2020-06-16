from tkinter import *
from os import path, system
from random import randint
from pprint import pprint
import jeu_de_la_vie as jdlv
import time
import sys

# on stocke l'endroit ou est notre programme.
project_folder = path.dirname(__file__)


# ===============================================================
# Fonctions relatives au calculs de coordonnées de la grille
# ===============================================================


def idx_to_coord(i, j):
    """Converti les coordonnées de la grille en coordonnées du canevas.

    :param i: Indice de ligne.
    :type i: int.
    :param j: Indice de colonne.
    :type j: int.

    :returns: Les coordonnées des deux points pour remplir le rectangle.
    :rtype: un tuple contenant deux tuples.
    """
    # on calcule d'abord les coordonnées des points
    x1 = grid_size * j - 1
    y1 = grid_size * i - 1
    x2 = grid_size * j + grid_size - 1
    y2 = grid_size * i + grid_size - 1
    return (x1, y1), (x2, y2)


def coord_to_idx(x, y):
    """Converti les coordonnées du canevas en coordonnées de la grille.

    :param x: Abscisse.
    :type x: int.
    :param y: Ordonnée.
    :type y: int.

    :returns: Les coordonnées de la grille.
    :rtype: tuple.
    """
    return (y // grid_size, x // grid_size)


# ==============================================================================
# Fonctions relatives à l'interaction entre l'interface et l'utilisateur
# ==============================================================================


def clic_canevas(event, click_side):
    """Modifie l'affichage de la grille lors du clic sur le canvas.

    :param click_side: le côté clické de la souris.
    :type clicl_side: str.
    """
    global grille
    x, y = event.x, event.y
    i, j = coord_to_idx(x, y)

    # si on clique dans la grille affichée (sans les bordures):
    if jdlv.rab_bordure <= i < len(grille) - jdlv.rab_bordure and \
        jdlv.rab_bordure <= j < len(grille[0]) - jdlv.rab_bordure:

        if click_side == "left":
            grille[i][j] = 1
            couleur = "black"
        else:
            grille[i][j] = 0
            couleur = "white"

        canvas.itemconfig(cellules[j][i], fill=couleur)
        jdlv.affiche(grille)


def display_grid(grid):
    """Affiche la grille de tableaux de python dans le canvas de Tkinter.
    Affiche également la grille dans le terminal."""
    # On l'affiche dans le terminal
    jdlv.affiche(grille)

    # On l'affiche dans le canvas de Tkinter
    for l in range(jdlv.rab_bordure, nlignes - jdlv.rab_bordure):
        for c in range(jdlv.rab_bordure, ncolonnes - jdlv.rab_bordure):

            if grid[l][c] == 1:
                couleur = "black"
            else:
                couleur = "white"

            canvas.itemconfig(cellules[c][l], fill=couleur)


def clean_grid(event=None):
    """Nettoie la grille."""
    global grille, play_flag, n_generations

    # on arrête l'exécution en boucle de la fonction en_boucle()
    play_flag = False

    # on vide la grille et on l'affiche
    grille = jdlv.grille_vide(nlignes, ncolonnes)
    display_grid(grille)

    # on réinitialise les nombre de génération à 0 et on actualise l'affichage
    n_generations = 0
    VarLabelGenerations.set(n_generations)


# ================================================
# Fonctions pour faire jouer la simulation
# ================================================


def en_boucle():
    """Permet de jouer en boucle la simulation du jeu de la vie."""
    global grille, n_generations

    if play_flag:
        # si on peut jouer :

        grille = jdlv.une_generation(grille)
        display_grid(grille)

        # on ajoute une génération au label, et on l'actualise
        n_generations += 1
        VarLabelGenerations.set(n_generations)

        # et on refait appel à cette fonction la fonction
        root.after(1, en_boucle)


def play(event=None):
    """Fonction qui fait se développer la grille en boucle."""
    global play_flag
    
    play_flag = True
    en_boucle()
    

# ================================================================
# Bonus : importations de grilles, génération aléatoire, etc
# ================================================================

    
def import_prefabs():
    """Permet d'importer une grille préfabriquée."""
    global nlignes, ncolonnes, grille

    # on lit le fichier qui contient la grille :
    fichier = path.join(project_folder, "prefabs/canon.txt")
    grille = jdlv.lire_fichier(fichier)
    display_grid(grille)


def generation_aleatoire_de_grille():
    """Génère une grille dont les cellules vivantes (1) sont aléatoirement disposée."""
    global grille
    grille = jdlv.grille_vide(nlignes, ncolonnes)

    for ligne in range(nlignes):
        for colonne in range(ncolonnes):
            if randint(1, 6) == 1:
                grille[ligne][colonne] = 1

    display_grid(grille)
    return grille


nlignes = 14 + (jdlv.rab_bordure * 2)
ncolonnes = 36 + (jdlv.rab_bordure * 2)
grille = jdlv.grille_vide(nlignes, ncolonnes)

# grid_size est la variable qui définit la taille du côté d'un carré (donc sa largeur et sa longueur)
grid_size = 25
cwidth = ncolonnes * grid_size
cheight = nlignes * grid_size

if __name__ == "__main__":

    # variable qui permet d'arrêter la simulation
    play_flag = bool()

    # variable qui nous permet de compter le nombre de générations
    n_generations = int()

    # =================
    # FENETRE
    # =================

    root = Tk()
    root.title("Jeu de la vie")
    root.geometry("{}x{}".format(cwidth + 200, cheight))

    # creation du canevas
    canvas = Canvas(root, bg='gray', width=cwidth, height=cheight, highlightthickness=0)
    canvas.pack(side="right")

    # si on clique sur le canevas, on appelle la fonction clic_canevas
    canvas.bind("<Button-1>", lambda event: clic_canevas(event, "left"))
    canvas.bind("<Button-3>", lambda event: clic_canevas(event, "right"))

    # on dessine la grille et on stocke les cases (pour les modifier plus tard)
    cellules = [[canvas.create_rectangle(idx_to_coord(l, c), outline="gray") for l in range(nlignes)] for c in range(ncolonnes)]


    # on créer la frame principale de la fenêtre
    main_frame = Frame(root, bg="#404040")
    main_frame.pack(fill="both", expand=True)


    # Création d'une variable de contrôle qui permet de modifier le text du label sans 
    # avoir à passer par une fonction.
    VarLabelGenerations = StringVar()
    VarLabelGenerations.set(n_generations)

    # un label pour afficher les victoires/matchs nuls
    generation_label = Label(main_frame, textvariable=VarLabelGenerations, font=("Arial", 20), bg="#404040", fg="red")
    generation_label.pack(expand=True)


    retrecicement_images = 5
    width_images = 512/retrecicement_images
    height_images = 512/retrecicement_images

    # on créer l'image pour mettre en pause ou pour reprendre la simulation du jeu
    play_image = PhotoImage(file=path.join(project_folder, "assets/play.png")).subsample(retrecicement_images)
    play_canvas = Canvas(main_frame, width=width_images, height=height_images, bg='#404040', bd=0, highlightthickness=0)
    play_canvas.create_image(width_images/2, height_images/2, image=play_image)

    play_canvas.bind("<Button-1>", play)
    play_canvas.pack(expand=True)

    # on créer l'image pour mettre la grille à l'état d'origine.
    restart_image = PhotoImage(file=path.join(project_folder, "assets/restart.png")).subsample(retrecicement_images)
    restart_canvas = Canvas(main_frame, width=width_images, height=height_images, bg="#404040", bd=0, highlightthickness=0)
    restart_canvas.create_image(width_images/2, height_images/2, image=restart_image)
        
    restart_canvas.bind("<Button-1>", clean_grid)
    restart_canvas.pack(expand=True)

    # on créer un bouton (à remplacer par un truc plus propre) pour générer une grille aléatoire
    random_button = Button(main_frame, text='générer', command=generation_aleatoire_de_grille)
    random_button.pack()

    # on créer un bouton (à remplacer par un truc plus propre) pour insérer la grille du canon
    import_button = Button(main_frame, text='import du canon', command=import_prefabs)
    import_button.pack()

    # on créer un bouton (à remplacer par un truc plus propre) pour sauvegarder la grille créée
    save_button = Button(main_frame, text='save', command=lambda: jdlv.sauvegarder_grille(grille))
    save_button.pack()

    display_grid(grille)

    root.mainloop()
