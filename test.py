from jeu_de_la_vie import lancer_jeu_console, lire_fichier
from os import path

# on stocke l'endroit ou est notre programme.
project_folder = path.dirname(__file__)

# on créer un dictionnaire avec des le nom du fichier à tester en clef et le nombre
# d'itérations à faire pour que le test soit celui prévu
a_tester = {
    "regles_de_base.txt" : 1,     # structure qui teste les règles de bases du jeu de la vie
    "bateau.txt" : 1,             # structure stable
    "bloc.txt" : 1,               # structure stable
    "mare.txt" : 1,               # structure stable
    "pain.txt" : 1,               # structure stable
    "cthulhu.txt" : 1,            # grande structure stable (composée de 45 cellules vivantes)
    "balise.txt" : 1,             # structure oscillante de période 2
    "clignotant.txt" : 1,         # structure oscillante de période 2
    "grenouille.txt" : 1,         # structure oscillante de période 2
    "pulsar.txt" : 3,             # structure oscillante de période 3
    "pentadecathlon.txt" : 15,    # structure oscillante de période 15

    # structures quelconques dont on connait la prédisposition des cellules au bout de n itérations
    "test1.txt" : 4,
    "test2.txt" : 2,
    "test3.txt" : 6,
    "test4.txt" : 4,
    "test5.txt" : 17,
    "test6.txt" : 63,
}

for structure, iterations in a_tester.items():
    # et on lit le fichier qui nous donne la structure de base
    structure_de_base = lire_fichier(path.join(project_folder, "tests/grilles_test/" + structure))
    # on lit le fichier qui nous donne la structure finale
    structure_finale = lire_fichier(path.join(project_folder, "tests/grilles_finales/" + structure))

    # et on fait notre test
    assert lancer_jeu_console(iterations, structure_de_base, False) == structure_finale
    print(structure, "testé !")

print("\nTout s'est bien déroulé !")
