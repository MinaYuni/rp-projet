import time
import utils

from WordleMindProblem import WordleMindProblem


if __name__ == "__main__":
    print("========== Bienvenue dans Wordle Mind ========== \n")

    file_path = "./dico.txt"
    dictionnaire = utils.lire_dictionnaire(file_path)

    n = 3
    mot_secret = utils.generer_mot_secret(n, dictionnaire)
    print("mot secret: {}".format(mot_secret))

    maxsize = 5
    maxgen = 20

    WMP = WordleMindProblem(mot_secret, dictionnaire)

    print("\n----- Algo Génétique -----\n")

    temps_debut_ag = time.perf_counter()
    nb_tentatives_ag = WMP.resolution_par_algo_genetique(maxsize, maxgen)
    temps_fin_ag = time.perf_counter()

    temps_total_ag = temps_fin_ag - temps_debut_ag

    print("\n----- RAC -----\n")

    temps_debut_rac = time.perf_counter()
    nb_tentatives_rac = WMP.resolution_par_CSP_A1()
    temps_fin_rac = time.perf_counter()

    temps_total_rac = temps_fin_rac - temps_debut_rac

    print("\n----- FIN -----\n")

    print("Temps AG: {:.5f} s\tNb tentatives: {}".format(temps_total_ag, nb_tentatives_ag))
    print("Temps RAC: {:.5f} s\tNb tentatives: {}".format(temps_total_rac, nb_tentatives_rac))
