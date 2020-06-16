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
    "cthulhu.txt" : 1,
    "pulsar.txt" : 3,
    "pentadecathlon.txt" : 15,
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

print("Tout s'est bien déroulé !")
