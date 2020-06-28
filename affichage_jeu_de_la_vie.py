from tkinter import *
from tkinter.ttk import Combobox
from tkinter.simpledialog import askinteger
from tkinter.filedialog import askopenfilename, asksaveasfilename
from tkinter.messagebox import showerror
from os import path, listdir
from random import randrange
import jeu_de_la_vie as jdlv
import sys

# on stocke l'endroit ou est notre programme.
project_folder = path.dirname(__file__)


# ==============================================================================
# Fonctions relatives à l'interaction entre l'interface et l'utilisateur
# ==============================================================================


def idx_to_coord(i, j):
    """Converti les coordonnées de la grille en coordonnées du canevas.

    :param i: Indice de ligne.
    :type i: int.
    :param j: Indice de colonne.
    :type j: int.

    :returns: Les coordonnées des deux points pour remplir le rectangle.
    :rtype: un tuple contenant deux tuples.
    """
    # pour éviter que notre curseur soit déplacé
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
    Affiche également la grille dans le terminal.
    
    :param grid: grille du jeu.
    :type grid: list.
    """
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


def restart(event=None):
    """Remet à neuf la grille et l'interface graphique (bouton play/pause & compteur)."""
    global grille, n_generations, id_test, pause
    
    root.after_cancel(after_id)

    # on supprime l'image actuellement affichée dans le canvas
    play_canvas.delete(id_test)
    # on affiche celle qu'on souhaite à la place
    id_test = play_canvas.create_image(width_images/2, height_images/2, image=play_image)
    pause = False

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
    """Permet de jouer en boucle la simulation du jeu de la vie.
    
    :param boucle: spécifie si la fonction doit se répéter.
    :type boucle: bool.
    """
    global grille, n_generations, after_id

    # on ajoute une génération au label, et on l'actualise
    n_generations += 1
    VarLabelGenerations.set(n_generations)

    grille = jdlv.une_generation(grille)
    print("{}e génération :".format(n_generations))
    display_grid(grille)

    if boucle:
        # et on refait appel à cette fonction la fonction
        after_id = root.after(vitesse_affichage, en_boucle)

    if jdlv.verifie_si_grille_vide(grille):
        # si la grille est entièrement vide (bordures comprises), il est inutile de continuer
        restart()


def play(event=None):
    """Fonction qui fait se développer la grille en boucle."""
    global id_test, pause

    if pause:
        # on arrête l'affichage
        root.after_cancel(after_id)

        # on supprime l'image actuellement affichée dans le canvas
        play_canvas.delete(id_test)
        # on affiche celle qu'on souhaite à la place
        id_test = play_canvas.create_image(width_images/2, height_images/2, image=play_image)
        pause = False
    else:
        # on supprime l'image actuellement affichée dans le canvas
        play_canvas.delete(id_test)
        # on affiche celle qu'on souhaite à la place
        id_test = play_canvas.create_image(width_images/2, height_images/2, image=pause_image)
        pause = True
        en_boucle()
    

# ================================================================
# Bonus : importations de grilles, génération aléatoire, etc
# ================================================================
            

def sauvegarder_grille(grille, file_name):
    """Sauvegarde la grille en un fichier texte.
    
    :param grille: grille à sauvergarder.
    :type: list.
    :param file_name: chemin absolu où stocker le fichier texte. 
    :type: str.
    """
    with open(file_name, 'w') as fichier:
        for l in range(jdlv.rab_bordure, len(grille) - jdlv.rab_bordure):
            for c in range(jdlv.rab_bordure, len(grille[0]) - jdlv.rab_bordure):
                # on écrit chaque case de la grille une à une dans le fichier
                fichier.write(str(grille[l][c]))
            fichier.write('\n')

    print("Sauvegarde réussie ! Emplacement : {}.".format(file_name))


def lire_fichier(fichier):
    """Lit le fichier et retourne la grille qu'il contient."""
    # ou ouvre le fichier en lecture
    with open(fichier, "r") as fichier:
        # on retourne une liste par compréhension contenant chaque ligne qu'on lit du fichier.
        return [[int(x) for x in line.strip()] for line in fichier]

    
def import_prefabs(fichier):
    """Permet d'importer une grille préfabriquée."""
    global nlignes, ncolonnes, grille

    # on lit le fichier qui contient la grille :
    grille_structure = lire_fichier(fichier)

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
        # on prévient l'utilisateur de la taille nécessaire pour afficher la structure
        taille_req = "{}x{}".format(len(grille_structure), len(grille_structure[0]))
        showerror("Erreur : taille", "Taille minimum requise : {}.".format(taille_req))
        print("erreur\ntaille minimum requise : {}.".format(taille_req))


def choix_fichier(event):
    """Récupère le choix de l'tuilisateur dans la combobox et importe le fichier du même nom."""
    # on récupère l'élément choisi
    choix = listeCombo.get()

    # si l'élément est celui-ci, alors l'utilisateur veut choisir lui même le fichier
    if choix == "Choisir...":
        # on ouvre une boite de dialogue pour demander le fichier à l'utilisateur
        choix = askopenfilename(title="Charger ma grille",
                                initialdir=path.join(project_folder, "saves/"))

        # en cas d'annulation, on ne fait rien
        if choix == '':
            return
    else:
        choix = path.join(project_folder, "prefabs/{}.txt".format(choix))
        
    # on nettoie la grille pour éviter une superposition chaotique des structures
    restart()
    # on envoie le chemin absolu du fichier à cette fonction pour l'ouvrir et l'afficher
    import_prefabs(choix)


def ask_to_save(grille, event=False):
    """Demande à l'utilisateur de sauvegarder sa grille à l'aide d'une boite de dialogue.
    
    :param grille: grille de jeu.
    :type grille: list.
    """
    # on récupère le chemin absolu où l'utilisateur veut sauvegarder son fichier 
    file_name = asksaveasfilename(title="Sauvergarder ma grille", 
                                  defaultextension='.txt',
                                  filetypes = [("Fichier Texte", "*.txt"),
                                               ("Tous les fichiers", "*.*")],
                                  initialdir=path.join(project_folder, "saves/"))

    # s'il n'y a pas d'annulation, on sauvegarde la grille à l'emplacement précis.
    if file_name != '':
        sauvegarder_grille(grille, file_name)


def generation_aleatoire_de_grille(event=False):
    """Génère une grille dont les cellules vivantes (1) sont aléatoirement disposée.
    
    :param pourcentage: pourcentages de cellules vivantes dans la grille.
    :type pourcentage: float.
    """
    global grille
    grille = jdlv.grille_vide(nlignes, ncolonnes)

    pourcentage = askinteger("Génération aléatoire", "Quel sera le pourcentage de cellules vivantes ?")
    if not 0 <= pourcentage <= 100:
        showerror("Erreur", "Non compris entre 0 et 100 !")

    # en cas d'annulation, on ne fait rien
    if pourcentage == None:
        return

    for l in range(nlignes):
        for c in range(ncolonnes):
            if randrange(100) < pourcentage:
                grille[l][c] = 1

    display_grid(grille)

    return grille


def change_speed(v):
    """Fonction qui change la vitesse de la méthode after lorsque
    l'utilisateur déplace le slider (Scale)."""
    global vitesse_affichage

    if slider.get() < 1:
        vitesse_affichage = 1
    else:
        vitesse_affichage = slider.get()



# ======================================================
#               Exécution du programme
# ======================================================



if __name__ == "__main__":

    # jdlv.rab_bordure correspond aux bordures non visibles par l'utilisateur
    # donc, les entiers sont les bordures visibles par l'utilisateur
    nlignes = 55 + (jdlv.rab_bordure * 2)
    ncolonnes = 70 + (jdlv.rab_bordure * 2)
    grille = jdlv.grille_vide(nlignes, ncolonnes)

    # grid_size est la variable qui définit la taille du côté d'un carré (donc sa largeur et sa longueur)
    grid_size = 12

    # largeur et hauteur du canvas
    cwidth = (ncolonnes - (jdlv.rab_bordure * 2)) * grid_size
    cheight = (nlignes - (jdlv.rab_bordure * 2)) * grid_size

    # variable qui permet de stopper l'exécution en boucle de l'affichage de la fenêtre
    after_id = "after#0"

    # variable qui permet de gérer la vitesse d'actualisation de la grille
    vitesse_affichage = 2

    # variable qui permet de savoir si le jeu est en pause ou non
    pause = False

    # variable qui nous permet de compter le nombre de générations
    n_generations = 0

# ========================================= 
#                 FENETRE
# ========================================= 

    root = Tk()
    root.title("Jeu de la vie")
    root.iconphoto(True, PhotoImage(file=path.join(project_folder, "assets", "icon.png")))
    root.geometry("{}x{}+0+0".format(cwidth + 500, cheight))
    root.resizable(False, False)


# ========================================= 
#        Barre de widget de gauche
# ========================================= 

    # on créer la frame principale de la fenêtre
    setting_frame = Frame(root, width=400, bg="#404040", bd=3, relief='raised')
    setting_frame.pack(fill="both", expand=True, side="left")


    # Création d'une variable de contrôle qui permet de modifier le text du label sans 
    # avoir à passer par une fonction.
    VarLabelGenerations = StringVar()
    VarLabelGenerations.set(n_generations)

    # un label pour afficher les victoires/matchs nuls
    generation_label = Label(setting_frame, width=5, height=2, textvariable=VarLabelGenerations,
                            font=("Arial", 20), bg="#404040", fg="red", bd=5, relief='sunken')
    generation_label.pack(expand=True)


    # on créer une frame pour y mettre la combobox
    combo_frame = Frame(setting_frame, bg="#404040")
    combo_frame.pack(expand=True)

    labelChoix = Label(combo_frame, text="Importer\nune structure :", bg="#404040", 
                      fg="white",font=("Arial", 15, "bold"))
    labelChoix.pack()

    # on charge le nom de toutes les structures préfabriquées dans une liste sans leur extension .txt
    liste = [f[:len(f)-4] for f in listdir(path.join(project_folder, "prefabs/"))]
    liste.append("Choisir...")

    listeCombo = Combobox(combo_frame, values=liste)
    listeCombo.pack()

    listeCombo.bind("<<ComboboxSelected>>", choix_fichier)

    # données pour afficher les images
    retrecicement_images = 5
    width_images = 512/retrecicement_images
    height_images = 512/retrecicement_images

    # on créer l'image pour sauvergarder notre grille
    save_image = PhotoImage(file=path.join(project_folder, "assets/save.png")).subsample(retrecicement_images)
    save_canvas = Canvas(setting_frame, width=width_images, height=height_images, 
                        bg="#404040", bd=0, highlightthickness=0)
    save_canvas.create_image(width_images/2, height_images/2, image=save_image)
    save_canvas.bind("<Button-1>", lambda event: ask_to_save(grille=grille))
    save_canvas.pack()

    # on créer l'image pour fermer la fenêtre.
    quit_image = PhotoImage(file=path.join(project_folder, "assets/quit.png")).subsample(retrecicement_images)
    quit_canvas = Canvas(setting_frame, width=width_images, height=height_images, 
                        bg="#404040", bd=0, highlightthickness=0)
    quit_canvas.create_image(width_images/2, height_images/2, image=quit_image)
        
    quit_canvas.bind("<Button-1>", sys.exit)
    quit_canvas.pack(expand=True)


# ========================================= 
#          Canvas de la grille
# ========================================= 

    # creation du canevas (le bg bleu sert à remarquer les possibles imperfections du .pack())
    canvas = Canvas(root, bg='blue', width=cwidth-60, height=cheight, highlightthickness=0)
    canvas.pack(fill="both", expand=True, side="left")

    # si on clique sur le canevas, on appelle la fonction clic_canevas
    canvas.bind("<Button-1>", lambda event: clic_canevas(event, "left"))
    canvas.bind("<Button-3>", lambda event: clic_canevas(event, "right"))

    # on dessine la grille et on stocke les cases (pour les modifier plus tard)
    cellules = [[canvas.create_rectangle(idx_to_coord(l, c), outline="gray") 
                for l in range(nlignes)] for c in range(ncolonnes)]


# =======================================================================
#        Barre de droite permettant de controler la simulation
# ========================================= =============================

    # frame qui contient tous les autres widgets dans cette partie de la fenêtre
    evolution_frame = Frame(root, width=300, bg="#404040", bd=3, relief='ridge')
    evolution_frame.pack(fill="both", expand=True, side="left")

    # frame qui contient les boutons et le label
    control_buttons = Frame(evolution_frame, bg="#404040")
    control_buttons.pack(side="top", expand=True)

    # Prévient l'utilisateur de ce à quoi servent les boutons dans cette frame.
    labelControles = Label(control_buttons, text="Contrôles  :", bg="#404040", 
                          fg="white", font=("Helvetica", 20, "bold"))
    labelControles.pack()

    # frames qui permettent d'avoir un alignement des boutons agréable au regard
    row_one = Frame(control_buttons, bg="#555555")
    row_one.pack(side="top")

    row_two = Frame(control_buttons, bg="#555555")
    row_two.pack(side="bottom")

    # on créer l'image pour mettre la grille à l'état d'origine.
    restart_image = PhotoImage(file=path.join(project_folder, "assets/restart1.png")).subsample(retrecicement_images)
    restart_canvas = Canvas(row_one, width=width_images, height=height_images, 
                            bg="#656565", bd=3, relief="sunken", highlightthickness=0)
    restart_canvas.create_image(width_images/2, height_images/2, image=restart_image)

    restart_canvas.bind("<Button-1>", restart)
    restart_canvas.pack(side="left")

    # on créer l'image pour passer à la génération suivante
    next_image = PhotoImage(file=path.join(project_folder, "assets/next.png")).subsample(retrecicement_images)
    next_canvas = Canvas(row_one, width=width_images, height=height_images, 
                        bg="#656565", bd=3, relief="sunken", highlightthickness=0)
    next_canvas.create_image(width_images/2, height_images/2, image=next_image)
        
    next_canvas.bind("<Button-1>", lambda event: en_boucle(False))
    next_canvas.pack(side="left")

    # on créer l'image pour mettre en pause ou pour reprendre la simulation du jeu
    play_image = PhotoImage(file=path.join(project_folder, "assets/play1.png")).subsample(retrecicement_images)
    play_canvas = Canvas(row_two, width=width_images, height=height_images, 
                        bg='#656565', bd=3, relief="sunken", highlightthickness=0)
    id_test = play_canvas.create_image(width_images/2, height_images/2, image=play_image)

    play_canvas.bind("<Button-1>", play)
    play_canvas.pack(expand=True)

    # on charge l'image de pause, sans l'afficher
    pause_image = PhotoImage(file=path.join(project_folder, "assets/pause.png")).subsample(retrecicement_images)

    # on créer l'image pour générer une grille aléatoire
    random_image = PhotoImage(file=path.join(project_folder, "assets/random.png")).subsample(retrecicement_images)
    random_canvas = Canvas(evolution_frame, width=width_images, height=height_images, 
                          bg="#404040", bd=0, highlightthickness=0)
    random_canvas.create_image(width_images/2, height_images/2, image=random_image)
        
    random_canvas.bind("<Button-1>", generation_aleatoire_de_grille)
    random_canvas.pack(expand=True)
    slider_frame = Frame(evolution_frame, bg="#404040")
    slider_frame.pack(expand=True)

    labelSlider = Label(slider_frame, text="Vitesse  :", bg="#404040", 
                       fg="white", font=("Arial", 15, "bold"))
    labelSlider.pack()

    slider = Scale(slider_frame, orient='horizontal', bg="#404040", fg="white", 
                  from_=0, to=500, resolution=1, tickinterval=100, length=220, 
                  command=change_speed, highlightthickness=0)
    slider.pack()
    slider.set(2)
 
    # on affiche une première fois la grille
    display_grid(grille)

    root.mainloop()
