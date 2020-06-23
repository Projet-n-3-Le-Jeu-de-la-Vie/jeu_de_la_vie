from tkinter import *
from tkinter.ttk import Combobox
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror
from os import path, system, listdir
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
    i -= jdlv.rab_bordure
    j -= jdlv.rab_bordure
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
    return (y // grid_size + jdlv.rab_bordure,
            x // grid_size + jdlv.rab_bordure)


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
    jdlv.affiche(grid)

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
    global grille, n_generations
    
    root.after_cancel(after_id)

    # on vide la grille et on l'affiche
    grille = jdlv.grille_vide(nlignes, ncolonnes)
    display_grid(grille)

    # on réinitialise les nombre de génération à 0 et on actualise l'affichage
    n_generations = 0
    VarLabelGenerations.set(n_generations)


# ================================================
# Fonctions pour faire jouer la simulation
# ================================================


def en_boucle(boucle=True):
    """Permet de jouer en boucle la simulation du jeu de la vie."""
    global grille, n_generations, after_id

    grille = jdlv.une_generation(grille)
    display_grid(grille)

    # on ajoute une génération au label, et on l'actualise
    n_generations += 1
    VarLabelGenerations.set(n_generations)

    if boucle:
        # et on refait appel à cette fonction la fonction
        after_id = root.after(2, en_boucle)

    if jdlv.verifie_si_grille_vide(grille):
        # si la grille est entièrement vide (bordures comprises), il est inutile de continuer
        clean_grid()


def play(event=None):
    """Fonction qui fait se développer la grille en boucle."""
    global id_test, pause

    if pause:
        root.after_cancel(after_id)
        play_canvas.delete(id_test)
        id_test = play_canvas.create_image(width_images/2, height_images/2, image=play_image)
        pause = False
    else:
        play_canvas.delete(id_test)
        id_test = play_canvas.create_image(width_images/2, height_images/2, image=pause_image)
        pause = True
        en_boucle()
    

# ================================================================
# Bonus : importations de grilles, génération aléatoire, etc
# ================================================================

    
def import_prefabs(fichier):
    """Permet d'importer une grille préfabriquée."""
    global nlignes, ncolonnes, grille

    # on lit le fichier qui contient la grille :
    grille_structure = jdlv.lire_fichier(fichier)
    # on vérifie que la grille a la place de contenir la structure
    if len(grille) - (jdlv.rab_bordure * 2) >= len(grille_structure) and \
       len(grille[0]) - (jdlv.rab_bordure * 2) >= len(grille_structure[0]):
        # on parcourt la grille contenant la structure
        for l in range(len(grille_structure)):
            for c in range(len(grille_structure[0])):
                if grille_structure[l][c] == 1:
                    # on dessine dans la zone visible
                    grille[l + jdlv.rab_bordure][c + jdlv.rab_bordure] = 1
        display_grid(grille)
    else:
        taille_req = "{}x{}".format(len(grille_structure), len(grille_structure[0]))
        showerror("Erreur : taille", "Taille minimum requise : {}.".format(taille_req))
        print("erreur\ntaille minimum requise : {}.".format(taille_req))


def generation_aleatoire_de_grille(event=False):
    """Génère une grille dont les cellules vivantes (1) sont aléatoirement disposée."""
    global grille
    grille = jdlv.grille_vide(nlignes, ncolonnes)

    for ligne in range(nlignes):
        for colonne in range(ncolonnes):
            if randint(1, 6) == 1:
                grille[ligne][colonne] = 1

    display_grid(grille)
    return grille


def choix_fichier(event):
    choix = listeCombo.get()
    clean_grid()
    if choix == "Choisir...":
        choix = askopenfilename(title="Charger ma grille",
                                initialdir=path.join(project_folder, "prefabs/"))
        if choix == '':
            return
    else:
        choix = path.join(project_folder, "prefabs/{}".format(choix))

    import_prefabs(choix)


def ask_to_save(grille, event=False):
    file_name = asksaveasfilename(title="Sauvergarder ma grille", 
                                  defaultextension='.txt',
                                  filetypes = [("Fichier Texte", "*.txt"),
                                               ("Tous les fichiers", "*.*")],
                                  initialdir=path.join(project_folder, "saves/"))
    if file_name != '':
        jdlv.sauvegarder_grille(grille, file_name)


nlignes = 25 + (jdlv.rab_bordure * 2)
ncolonnes = 47 + (jdlv.rab_bordure * 2)
grille = jdlv.grille_vide(nlignes, ncolonnes)

# grid_size est la variable qui définit la taille du côté d'un carré (donc sa largeur et sa longueur)
grid_size = 25
cwidth = (ncolonnes - (jdlv.rab_bordure * 2)) * grid_size
cheight = (nlignes - (jdlv.rab_bordure * 2)) * grid_size

if __name__ == "__main__":

    # variable qui permet de stopper l'exécution en boucle de l'affichage de la fenêtre
    after_id = "after#0"

    # variable qui permet de savoir si le jeu est en pause ou non
    pause = False

    # variable qui nous permet de compter le nombre de générations
    n_generations = 0

    # =================
    # FENETRE
    # =================

    root = Tk()
    root.title("Jeu de la vie")
    root.iconbitmap(path.join(project_folder, "assets/icon.ico"))
    root.geometry("{}x{}".format(cwidth + 200, cheight + 150))
    root.resizable(False, False)

    main_frame = Frame(root)
    main_frame.pack(side="right", fill="both")

    # creation du canevas
    canvas = Canvas(main_frame, bg='gray', width=cwidth, height=cheight, highlightthickness=0)
    canvas.pack()

    # si on clique sur le canevas, on appelle la fonction clic_canevas
    canvas.bind("<Button-1>", lambda event: clic_canevas(event, "left"))
    canvas.bind("<Button-3>", lambda event: clic_canevas(event, "right"))

    # on dessine la grille et on stocke les cases (pour les modifier plus tard)
    cellules = [[canvas.create_rectangle(idx_to_coord(l, c), outline="gray") for l in range(nlignes)] for c in range(ncolonnes)]


    evolution_frame = Frame(main_frame, bg="#707070", bd=3, relief='ridge')
    evolution_frame.pack(fill="both", expand=True)

    retrecicement_images = 5
    width_images = 512/retrecicement_images
    height_images = 512/retrecicement_images

    # on créer l'image pour mettre la grille à l'état d'origine.
    restart_image = PhotoImage(file=path.join(project_folder, "assets/restart.png")).subsample(retrecicement_images)
    restart_canvas = Canvas(evolution_frame, width=width_images, height=height_images, bg="#707070", bd=0, highlightthickness=0)
    restart_canvas.create_image(width_images/2, height_images/2, image=restart_image)
        
    restart_canvas.bind("<Button-1>", clean_grid)
    restart_canvas.pack(expand=True, side="left")

    # on créer l'image pour mettre en pause ou pour reprendre la simulation du jeu
    play_image = PhotoImage(file=path.join(project_folder, "assets/play.png")).subsample(retrecicement_images)
    play_canvas = Canvas(evolution_frame, width=width_images, height=height_images, bg='#707070', bd=0, highlightthickness=0)
    id_test = play_canvas.create_image(width_images/2, height_images/2, image=play_image)

    play_canvas.bind("<Button-1>", play)
    play_canvas.pack(expand=True, side="left")

    # on charge l'image de pause, sans l'afficher
    pause_image = PhotoImage(file=path.join(project_folder, "assets/pause.png")).subsample(retrecicement_images)

    # on créer l'image pour passer à la génération suivante
    next_image = PhotoImage(file=path.join(project_folder, "assets/next.png")).subsample(retrecicement_images)
    next_canvas = Canvas(evolution_frame, width=width_images, height=height_images, bg="#707070", bd=0, highlightthickness=0)
    next_canvas.create_image(width_images/2, height_images/2, image=next_image)
        
    next_canvas.bind("<Button-1>", lambda event: en_boucle(False))
    next_canvas.pack(expand=True, side="left")


    # on créer la frame principale de la fenêtre
    setting_frame = Frame(root, bg="#404040", bd=3, relief='raised')
    setting_frame.pack(fill="both", expand=True)


    # Création d'une variable de contrôle qui permet de modifier le text du label sans 
    # avoir à passer par une fonction.
    VarLabelGenerations = StringVar()
    VarLabelGenerations.set(n_generations)

    # un label pour afficher les victoires/matchs nuls
    generation_label = Label(setting_frame, width=5, height=2, textvariable=VarLabelGenerations, font=("Arial", 20), bg="#404040", fg="red", bd=5, relief='sunken')
    generation_label.pack(expand=True)


# on créer une frame pour y mettre la combobox
    combo_frame = Frame(setting_frame, bg="#404040")
    combo_frame.pack(expand=True)

    labelChoix = Label(combo_frame, text="Importer\nune structure :", bg="#404040", fg="white", font=("Arial", 15))
    labelChoix.pack()

    liste = [fichier for fichier in listdir(path.join(project_folder, "prefabs/"))]
    liste.append("Choisir...")

    listeCombo = Combobox(combo_frame, values=liste)
    listeCombo.pack()

    listeCombo.bind("<<ComboboxSelected>>", choix_fichier)


    # on créer l'image pour générer une grille aléatoire
    random_image = PhotoImage(file=path.join(project_folder, "assets/random.png")).subsample(retrecicement_images)
    random_canvas = Canvas(setting_frame, width=width_images, height=height_images, bg="#404040", bd=0, highlightthickness=0)
    random_canvas.create_image(width_images/2, height_images/2, image=random_image)
        
    random_canvas.bind("<Button-1>", generation_aleatoire_de_grille)
    random_canvas.pack()

    # on créer l'image pour sauvergarder notre grille
    save_image = PhotoImage(file=path.join(project_folder, "assets/save.png")).subsample(retrecicement_images + 2)
    save_canvas = Canvas(setting_frame, width=width_images, height=height_images, bg="#404040", bd=0, highlightthickness=0)
    save_canvas.create_image(width_images/2, height_images/2, image=save_image)
        
    save_canvas.bind("<Button-1>", lambda event: ask_to_save(grille))
    save_canvas.pack()

    # on créer l'image pour fermer la fenêtre.
    quit_image = PhotoImage(file=path.join(project_folder, "assets/quit.png")).subsample(retrecicement_images)
    quit_canvas = Canvas(setting_frame, width=width_images, height=height_images, bg="#404040", bd=0, highlightthickness=0)
    quit_canvas.create_image(width_images/2, height_images/2, image=quit_image)
        
    quit_canvas.bind("<Button-1>", sys.exit)
    quit_canvas.pack(expand=True)

    display_grid(grille)

    root.mainloop()