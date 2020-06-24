from os import path

# on stocke l'endroit ou est notre programme.
project_folder = path.dirname(__file__)

def grille_vide(lignes, colonnes):
    """Création d'une grille ne contenant que des 0.
    
    :param lignes: nombre de ligne dans la grille.
    :type lignes: int.
    :param colonnes: nombre de colonnes dans la grille.
    :type colonnes: int.
    
    :return: grille de jeu.
    :rtype: list.
    """
    return [[0] * (colonnes) for x in range(lignes)]


def verifie_si_grille_vide(grille):
    """Regarde si la grille donée est vide.
    
    :param grille: Grille de jeu.
    :type grille: list.
    
    :returns: si la grille est vide.
    :rtype: bool.
    """
    # on parcourt toutes les cases de la grille
    for lignes in grille:
        for case in lignes:
            # si on remarque une seule cellule vivante,
            # alors la grille n'est pas vide.
            if '1' in str(case):
                return False
    return True


def compte_voisines_vivantes(grille, x, y):
    """Compte le nombre de cellules vivantes autour d'une cellule de la grille.

    :param grille: Grille des cellules.
    :type grille: list.
    :param x: colonne où se trouve la cellule autour de laquelle on souhaite compter les cellules vivantes.
    :type x: int.
    :param y: ligne où se trouve la cellule autour de laquelle on souhaite compter les cellules vivantes.
    :type y: int.

    :return: Le nombre de cellules vivantes autour de la cellule observée.
    :rtype: int.
    """
    voisines = 0
    
    # on parcourt toutes les cases voisines de la case donnée :
    for i in range(x-1, x+2):
        for j in range(y-1, y+2):
            # si l'emplacement qu'on regarde n'est pas celui de la cellule et qu'on ne sort pas du tableau :
            if not (i == x and j == y) and 0 <= i < len(grille) and 0 <= j < len(grille[0]):
                voisines += grille[i][j]

    return voisines


def affiche(grille):
    """Affichage de la grille de jeu.

    :param grille: Table de jeu.
    :type grille: list.
    """
    for ligne in range(len(grille)):
        for colonne in range(len(grille[0])):
            print(grille[ligne][colonne], end=' ')
        print()
    print()


def une_generation(grille):
    """Réalise une génération du jeu de la vie.
    
    :param grille: grille de jeu.
    :type grille: list.

    :return: grille contenant la nouvelle génération.
    :rtype: list.
    """
    lignes = len(grille)
    colonnes = len(grille[0])

    # cette grille tampon nous permet de ne pas directement modifier la grille de base pour ne pas
    # influer sur le nombre de voisins pendant l'exécution du programme
    grille_tampon = grille_vide(lignes, colonnes)

    # on parcourt toute la grille
    for l in range(lignes):
        for c in range(colonnes):
            # on compte le nombre de voisines vivantes (1) autour de la case donnée
            nvoisines = compte_voisines_vivantes(grille, l, c)

            # Règle de la naissance :
            if nvoisines == 3:
                grille_tampon[l][c] = 1
            # Une cellule avec 2 ou trois voisins reste en vie.
            if grille[l][c] == 1 and (nvoisines == 2 or nvoisines == 3):
                grille_tampon[l][c] = 1
            # Règles de solitude et de surpopulation :
            if nvoisines < 2 or nvoisines > 3:
                grille_tampon[l][c] = 0

    return grille_tampon


def reponse_entier(question, vmin, vmax):
    """Pose une question à l'utilisateur dont la réponse est un entier
    compris dans l'intervalle [vmin ; vmax]. vmin >= 0.
    La question est reposée tant que la réponse n'est pas correcte.

    :param question: la question à poser.
    :type question: str.
    :param vmin: la valeur minimale possible (>=0).
    :type vmin: int.
    :param vmax: la valeur maximale possible (>= vmin).
    :type vmax: int.
    :returns: l'entier choisi.
    :rtype: int.
    """
    # cette fonction est reprise du premier projet
    while vmin >= 0:      #on vérifie bien si vmin >= 0 ; permet également de faire une boucle infinie dans le cas où l'utilisateur répondrait mal.
        entier = input(question + ' [{};{}] '.format(vmin, vmax))

        try:
            entier = int(entier)
            assert entier >= vmin and entier <= vmax
            return entier     #si toutes les conditions du bloc try sont passées avec succès, on retourne entier
        except ValueError:     #si la variable 'entier' ne peut être convertie en int --> ValueError donc erreur de type entré par l'utilisateur
            print("Erreur de type !")
        except AssertionError:     #si l'entier n'est pas compris entre [vmin;vmax] --> AssertionError donc l'utilisateur a mal entré son entier
            print("L'entier saisi n'est pas compris entre [{};{}]".format(vmin, vmax))


def lancer_jeu_console(nb_etapes, grille, affichage=True):
    """Lance une simulation du jeu de la vie de Conway dans le terminal.
    
    :param nb_etapes: nombres de générations que va subir la grille.
    :type nb_etapes: int.
    :param grille: liste contenant les cellules vivantes (1) ou mortes (0).
    :type grille: list.
    :param afichage: précise si on affiche la grille.
    :type affichage: bool.
    
    :returns: grille ayant subi 'nb_etapes' générations.
    :rtype: list.
    """
    for x in range(nb_etapes):
        # on fait passer une génération à la grille
        grille = une_generation(grille)
        # si on veut afficher la grille :
        if affichage:
            print("{}e génération".format((x + 1)))
            affiche(grille)

    return grille


# variable qui permet de générer une bordure supplémentaire sur la grille.
rab_bordure = 4

if __name__ == "__main__":
    # On créer la grille de base en y rajoutant une bordure que l'utilisateur ne verra pas :
    grille = grille_vide(14 + (rab_bordure * 2), 36 + (rab_bordure * 2))

    # et on modifie nous-même les cases...
    grille[rab_bordure][rab_bordure] = 9
    grille[10 + rab_bordure][2 + rab_bordure] = 1
    grille[9 + rab_bordure][3 + rab_bordure] = 1
    grille[9 + rab_bordure][4 + rab_bordure] = 1
    grille[10 + rab_bordure][4 + rab_bordure] = 1
    grille[11 + rab_bordure][4 + rab_bordure] = 1

    # on affiche la grille
    affiche(grille)

    # On demande à l'utilisateur combien de fois il souhaite observer d'étapes
    nb_etapes = reponse_entier("Combien voulez-vous observer d'étapes ?", 1, 10 ** 5)
    # et on exécute le programme
    lancer_jeu_console(nb_etapes, grille)