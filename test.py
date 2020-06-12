from jeu_de_la_vie import lancer_jeu_console, lire_fichier
from os import path

# on stocke l'endroit ou est notre programme.
project_folder = path.dirname(__file__)

a_tester = {
    "regles_de_base.txt" : 1,
    "balise.txt" : 1,
    "bateau.txt" : 1,
    "bloc.txt" : 1,
    "clignotant.txt" : 1,
    "grenouille.txt" : 1,
    "mare.txt" : 1,
    "pain.txt" : 1,
    "test1.txt" : 4,
    "test2.txt" : 2,
    "test3.txt" : 6,
    "test4.txt" : 4,
    "test5.txt" : 17
}

for structure, iterations in a_tester.items():
    structure_finale = lire_fichier(path.join(project_folder, "tests/grilles_finales/" + structure))
    structure = lire_fichier(path.join(project_folder, "tests/grilles_test/" + structure))

    assert lancer_jeu_console(iterations, structure, False) == structure_finale

print("Tout s'est bien déroulé !")