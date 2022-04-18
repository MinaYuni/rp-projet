import time

import utils
from WordleMindProblem import WordleMindProblem


if __name__ == "__main__":
    print("========== Bienvenue dans Wordle Mind ========== \n")

    file_path = "./dico.txt"
    dictionnaire = utils.lire_dictionnaire(file_path)
    trie = utils.lire_dictionnaire_trie(file_path)

    # toutes les tailles de mot possibles
    liste_tailles = list(dictionnaire.keys())
    liste_tailles.sort()

    taille = 4   # taille du mot secret
    # génération du mot secret selon la taille voulue
    mot_secret = utils.generer_mot_secret(dictionnaire, n=taille)
    print("mot secret: {}".format(mot_secret))

    print("\n----- RAC -----\n")
    # initialisation du Wordle Mind
    WMP = WordleMindProblem(mot_secret, dictionnaire, trie)

    temps_debut_rac = time.perf_counter()
    nb_tentatives_rac = WMP.resolution_par_CSP(type_dico="dict", version="A1", verbose=True)
    temps_fin_rac = time.perf_counter()

    temps_total_rac = temps_fin_rac - temps_debut_rac

    print("\n----- RAC avec Trie -----\n")
    # initialisation du Wordle Mind
    WMP = WordleMindProblem(mot_secret, dictionnaire, trie)

    temps_debut_rac_trie = time.perf_counter()
    nb_tentatives_rac_trie = WMP.resolution_par_CSP(type_dico="trie", version="A1", verbose=True)
    temps_fin_rac_trie = time.perf_counter()

    temps_total_rac_trie = temps_fin_rac_trie - temps_debut_rac_trie

    print("\n----- RAC avec forward-checking -----\n")
    # initialisation du Wordle Mind
    WMP = WordleMindProblem(mot_secret, dictionnaire, trie)

    temps_debut_fc = time.perf_counter()
    nb_tentatives_fc = WMP.resolution_par_CSP(type_dico="trie", version="A2", verbose=True)
    temps_fin_fc = time.perf_counter()

    temps_total_fc = temps_fin_fc - temps_debut_fc

    print("\n----- CSP optimisé -----\n")
    # initialisation du Wordle Mind
    WMP = WordleMindProblem(mot_secret, dictionnaire, trie)

    temps_debut_csp_opt = time.perf_counter()
    nb_tentatives_csp_opt = WMP.resolution_par_CSP_opt(verbose=True)
    temps_fin_csp_opt = time.perf_counter()

    temps_total_csp_opt = temps_fin_csp_opt - temps_debut_csp_opt

    print("\n----- Algo Génétique -----\n")
    # initialisation du Wordle Mind
    WMP = WordleMindProblem(mot_secret, dictionnaire, trie)

    # paramètres pour l'algo génétique
    maxsize = 5  # taille max de l'ensemble E
    maxgen = 20  # nombre de générations

    temps_debut_ag = time.perf_counter()
    nb_tentatives_ag = WMP.resolution_par_algo_genetique(maxsize, maxgen, verbose=True)
    temps_fin_ag = time.perf_counter()

    temps_total_ag = temps_fin_ag - temps_debut_ag

    print("\n----- FIN -----\n")

    print("CSP RAC:\t{:.5f} s pour\t{} tentatives".format(temps_total_rac, nb_tentatives_rac))
    print("CSP RAC avec Trie:\t{:.5f} s pour\t{} tentatives".format(temps_total_rac_trie, nb_tentatives_rac_trie))
    print("CSP FC:\t{:.5f} s pour\t{} tentatives".format(temps_total_fc, nb_tentatives_fc))
    print("CSP OPT:\t{:.5f} s pour\t{} tentatives".format(temps_total_csp_opt, nb_tentatives_csp_opt))
    print("AG:\t\t\t{:.5f} s pour\t{} tentatives".format(temps_total_ag, nb_tentatives_ag))



