import copy
import datetime
import matplotlib.pyplot as plt
import os
import glob
from statistics import mean
import time

import utils
from WordleMindProblem import WordleMindProblem


def recuperer_donnees(path_file):
    moy_essais = []
    moy_tps = []

    for filename in glob.glob(os.path.join(path_file, '*.txt')):
        with open(os.path.join(os.getcwd(), filename), 'r') as fichier:
            donnees_essais = []
            donnees_tps = []
            flag = int
            data = ""
            cpt = 0

            for mot in fichier:
                mot = mot.strip('\n')
                if cpt == 0:
                    for i, lettre in enumerate(mot):
                        if lettre == "]":
                            flag = i
                cpt += 1

                data = mot[flag + 2:]
                essais = data[0]
                tps = data[3:]

                if essais == "-":
                    essais = -1

                donnees_essais.append(int(essais))
                donnees_tps.append(float(tps))

        moy_essais.append(mean(donnees_essais))
        moy_tps.append(mean(donnees_tps))

    return moy_essais, moy_tps


if __name__ == "__main__":
    print("===== START =====")

    file_path = "./dico.txt"
    dictionnaire = utils.lire_dictionnaire(file_path)  # lecture du dictionnaire
    trie = utils.lire_dictionnaire_trie(file_path)

    # nom de tous les algorithmes
    # liste_algo = ["csp_rac", "csp_fc", "csp_opt", "ag", "ag_opt"]

    affichage = True  # si on veut l'affichage des tentatives
    nb_tours = 20  # nombre de fois qu'on exécute les algorithmes
    maxsize = 5  # taille max de l'ensemble E
    maxgen = 20  # nombre max de générations

    taille_min = 4  # taille minimale du mot secret
    taille_max = 8  # taille maximale du mot secret
    # liste des tailles voulues pour le mot secret
    liste_tailles = [i for i in range(taille_min, taille_max + 1)]

    fig, axs = plt.subplots(1, 2, figsize=(18, 8))

    print("----- csp_fc -----")

    csp_fc_path = "data/csp_fc/"
    csp_fc_essais, csp_fc_tps = recuperer_donnees(csp_fc_path)

    axs[0].plot(liste_tailles, csp_fc_essais, label="csp_fc")
    axs[1].plot(liste_tailles, csp_fc_tps, label="csp_fc")

    print("----- csp_opt -----")

    csp_opt_path = "data/csp_opt/"
    csp_opt_essais, csp_opt_tps = recuperer_donnees(csp_opt_path)

    axs[0].plot(liste_tailles, csp_opt_essais, label="csp_opt")
    axs[1].plot(liste_tailles, csp_opt_tps, label="csp_opt")

    print("----- ag -----")

    cag_path = "data/ag/"
    ag_essais, ag_tps = recuperer_donnees(cag_path)

    axs[0].plot(liste_tailles, ag_essais, label="ag")
    axs[1].plot(liste_tailles, ag_tps, label="ag")

    print("----- csp_rac -----")

    taille_min_rac = 2  # taille minimale du mot secret
    taille_max_rac = 5  # taille maximale du mot secret
    # liste des tailles voulues pour le mot secret
    liste_tailles_rac = [i for i in range(taille_min_rac, taille_max_rac + 1)]

    csp_rac_path = "data/csp_rac/"
    csp_rac_essais, csp_rac_tps = recuperer_donnees(csp_rac_path)

    axs[0].plot(liste_tailles_rac, csp_rac_essais, label="csp_rac")
    axs[1].plot(liste_tailles_rac, csp_rac_tps, label="csp_rac")

    print("===== PLOT =====")

    axs[0].set_title("nombre d'essais moyen en fonction de la taille du mot secret")
    axs[0].set_xlabel("taille du mot secret")
    axs[0].set_ylabel("nombre d'essais moyen")

    axs[1].set_title("temps moyen d'exécution en fonction de la taille du mot secret")
    axs[1].set_xlabel("taille du mot secret")
    axs[1].set_ylabel("temps moyen")

    plt.legend()
    # plt.show()

    # path = "./data/n{}_min{}_max{}".format(nb_tours, liste_tailles[0], liste_tailles[-1])
    path = "./data/n{}-ag-csp_rac-fc-opt".format(nb_tours)
    plt.savefig(path)

    print("===== FIN =====")

