from jeu_de_la_vie import lancer_jeu_console, lire_fichier
from os import path

# on stocke l'endroit ou est notre programme.
project_folder = path.dirname(__file__)

# on créer un dictionnaire avec des le nom du fichier à tester en clef et le nombre
# d'itérations à faire pour que le test soit celui prévu
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
    # on lit le fichier qui nous donne la structure finale
    structure_finale = lire_fichier(path.join(project_folder, "tests/grilles_finales/" + structure))
    # et on lit le fichier qui nous donne la structure de base
    structure = lire_fichier(path.join(project_folder, "tests/grilles_test/" + structure))

    # on fait le test
    assert lancer_jeu_console(iterations, structure, False) == structure_finale

print("Tout s'est bien déroulé !")
