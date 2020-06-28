from affichage_jeu_de_la_vie import lire_fichier
from jeu_de_la_vie import lancer_jeu_console
from os import path

# on stocke l'endroit ou est notre programme.
project_folder = path.dirname(__file__)

# on créer un dictionnaire avec des le nom du fichier à tester en clef et le nombre
# d'itérations à faire en valeur pour que le test soit celui prévu
a_tester = {
    "regles_de_base.txt" : 1,     # structure qui teste les règles de bases du jeu de la vie
    "bateau.txt" : 1,             # structure stable
    "bigs.txt" : 1,               # structure stable
    "bloc.txt" : 1,               # structure stable
    "mare.txt" : 1,               # structure stable
    "pain.txt" : 1,               # structure stable
    "cthulhu.txt" : 1,            # grande structure stable (composée de 45 cellules vivantes)

    "balise.txt" : 2,             # structure oscillante de période 2
    "clignotant.txt" : 2,         # structure oscillante de période 2
    "grenouille.txt" : 2,         # structure oscillante de période 2
    "Lunettes.txt" : 2,           # structure oscillante de période 2
    "machine à laver.txt" : 2,    # structure oscillante de période 2
    "Why not.txt" : 2,            # structure oscillante de période 2
    "Grenouille 2.txt" : 3,       # structure oscillante de période 3
    "pulsar.txt" : 3,             # structure oscillante de période 3
    "Croix.txt" : 3,              # structure oscillante de période 3
    "Wavefront.txt" : 4,          # structure oscillante de période 4
    "Fontaine.txt" : 4,           # structure oscillante de période 4
    "101.txt" : 5,                # structure oscillante de période 5
    "coeur.txt" : 5,              # structure oscillante de période 5
    "volcan.txt" : 5,             # structure oscillante de période 5
    "Fiole.txt" : 8,              # structure oscillante de période 8
    "pentadecathlon.txt" : 15,    # structure oscillante de période 15

    # structures quelconques dont on connait la prédisposition des cellules au bout de n itérations
    "test1.txt" : 4,
    "test2.txt" : 2,
    "test3.txt" : 6,
    "test4.txt" : 4,
    "test5.txt" : 17,
    "test6.txt" : 63,
}

def tester():
    """Fonction de test du Jeu de la Vie."""
    tests_reussis = int()
    total = len(a_tester)
    i = 0

    # on parcourt toutes les clefs et valeurs du dictionnaire :
    for structure, iterations in a_tester.items():
        print("{}/{}\t".format(i + 1, total),
                (structure + " " * 20)[:20], "\t", end="")
        try:
            # et on lit le fichier qui nous donne la structure de base
            structure_de_base = lire_fichier(path.join(project_folder, "prefabs/" + structure))
            # on lit le fichier qui nous donne la structure finale
            structure_finale = lire_fichier(path.join(project_folder, "tests/" + structure))

            # on effectue notre test
            assert lancer_jeu_console(iterations, structure_de_base, False) == structure_finale

            # si on passe le test :
            tests_reussis += 1
            print("OK")
        except AssertionError:
            # sinon on affiche qu'il y a eu une erreur.
            print("échec /!\\")

        i += 1

    print("—" * 35 + "\nSynthèse : {}/{} tests passés ({:.01f}%)".format(tests_reussis, total,
                                                                    tests_reussis/total*100))

if __name__ == "__main__":
    tester()