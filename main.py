import time

import utils
from WordleMindProblem import WordleMindProblem


if __name__ == "__main__":
    print("========== Bienvenue dans Wordle Mind ========== \n")

    file_path = "./dico.txt"
    dictionnaire = utils.lire_dictionnaire(file_path)

    # toutes les tailles de mot possibles
    liste_tailles = list(dictionnaire.keys())
    liste_tailles.sort()

    taille = 6   # taille du mot secret
    # génération du mot secret selon la taille voulue
    mot_secret = utils.generer_mot_secret(dictionnaire, n=taille)
    print("mot secret: {}".format(mot_secret))

    print("\n----- RAC -----\n")
    # initialisation du Wordle Mind
    WMP = WordleMindProblem(mot_secret, dictionnaire)

    temps_debut_rac = time.perf_counter()
    nb_tentatives_rac = WMP.resolution_par_CSP_A1(verbose=True)
    temps_fin_rac = time.perf_counter()

    temps_total_rac = temps_fin_rac - temps_debut_rac

    print("\n----- CSP optimisé -----\n")
    # initialisation du Wordle Mind
    WMP = WordleMindProblem(mot_secret, dictionnaire)

    temps_debut_csp_opt = time.perf_counter()
    nb_tentatives_csp_opt = WMP.resolution_par_CSP_opt(verbose=True)
    temps_fin_csp_opt = time.perf_counter()

    temps_total_csp_opt = temps_fin_csp_opt - temps_debut_csp_opt

    print("\n----- Algo Génétique -----\n")
    # initialisation du Wordle Mind
    WMP = WordleMindProblem(mot_secret, dictionnaire)

    # paramètres pour l'algo génétique
    maxsize = 5  # taille max de l'ensemble E
    maxgen = 20  # nombre de générations

    temps_debut_ag = time.perf_counter()
    nb_tentatives_ag = WMP.resolution_par_algo_genetique(maxsize, maxgen, verbose=True)
    temps_fin_ag = time.perf_counter()

    temps_total_ag = temps_fin_ag - temps_debut_ag

    print("\n----- FIN -----\n")

    print("CSP RAC:\t{:.5f} s pour\t{} tentatives".format(temps_total_rac, nb_tentatives_rac))
    print("CSP OPT:\t{:.5f} s pour\t{} tentatives".format(temps_total_csp_opt, nb_tentatives_csp_opt))
    print("AG:\t\t\t{:.5f} s pour\t{} tentatives".format(temps_total_ag, nb_tentatives_ag))



