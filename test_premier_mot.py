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

    liste_premier_mot = []

    fichier = open("./data/premier_mot.txt", "r")

    for ligne in fichier:
        mot = ligne.strip("\n")
        liste_premier_mot.append(mot.lower())

    for mot in liste_premier_mot:
        taille = len(mot)
        premier_mot = list(mot)
        mot_secret = utils.generer_mot_secret(dictionnaire, n=taille)
        print("taille {}: {}".format(taille, utils.liste_mot_en_str(mot_secret).upper()))

        WMP = WordleMindProblem(mot_secret, dictionnaire, trie)

        temps_debut_csp_opt = time.perf_counter()
        nb_tentatives_csp_opt = WMP.resolution_par_CSP_opt(premier_mot=premier_mot, verbose=False)
        temps_fin_csp_opt = time.perf_counter()

        temps_debut_csp_opt_random = time.perf_counter()
        nb_tentatives_csp_opt_random = WMP.resolution_par_CSP_opt(verbose=False)
        temps_fin_csp_opt_random = time.perf_counter()

        temps_total_csp_opt = temps_fin_csp_opt - temps_debut_csp_opt
        temps_total_csp_opt_random = temps_fin_csp_opt_random - temps_debut_csp_opt_random

        print("CSP OPT:\t{:.5f} s pour\t{} tentatives".format(temps_total_csp_opt, nb_tentatives_csp_opt))
        print("CSP OPT random:\t{:.5f} s pour\t{} tentatives".format(temps_total_csp_opt_random, nb_tentatives_csp_opt_random))
        print()

    fichier.close()



