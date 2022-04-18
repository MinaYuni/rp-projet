import copy
import datetime
import matplotlib.pyplot as plt
import os
from statistics import mean
import time

import utils
from WordleMindProblem import WordleMindProblem


def liste_mot_en_str(mot_list):
    """
    Fonction qui change une liste de char en une chaine de caractères.
    :param mot_list: liste de char
    :type mot_list: list[str]
    :return: chaine de caractère
    :rtype: str
    """
    mot_str = ""
    for lettre in mot_list:
        mot_str += lettre
    return mot_str


def lancer_algo(mot_secret, dictionnaire, trie, nom_algo, maxsize=5, maxgen=20, affichage=False):
    """
    Fonction qui lance un algorithme donné en paramètre et renvoie le nombre de tentatives faites et le temps d'exécution.
    :param mot_secret: le mot secret
    :param dictionnaire: ditionnaire de mots
    :param nom_algo: nom de l'algorithme qu'on veut lancer
    :param maxsize: taille max de l'ensemble E pour l'algorithme génétique
    :param maxgen: nombre max de génération pour l'algorithme génétique
    :param affichage: si on veut l'affichage des tentatives
    :type mot_secret: list[str]
    :type dictionnaire: dict[int, list[list[str]]]
    :type nom_algo: str
    :type maxsize: int
    :type maxgen: int
    :type affichage: bool
    :return: nombre de tentatives faites, temps d'exécution
    :rtype: (int, float)
    """

    # initialisation du Wordle Mind
    WMP = WordleMindProblem(mot_secret, dictionnaire, trie)

    # choix de l'algorithme
    tps_debut = time.perf_counter()
    if nom_algo == "csp_rac":
        if affichage:
            print("----- CSP RAC -----")
        nb_essais = WMP.resolution_par_CSP(type_dico="dict", version="A1", verbose=affichage)
    elif nom_algo == "csp_rac_trie":
        nb_essais = WMP.resolution_par_CSP(type_dico="trie", version="A1", verbose=affichage)
    elif nom_algo == "csp_fc":
        if affichage:
            print("----- CSP FC -----")
        nb_essais = WMP.resolution_par_CSP(type_dico="trie", version="A2", verbose=affichage)
    elif nom_algo == "csp_opt":
        if affichage:
            print("----- CSP OPT -----")
        nb_essais = WMP.resolution_par_CSP_opt(verbose=affichage)
    elif nom_algo == "ag":
        if affichage:
            print("----- Algo Génétique -----")
        nb_essais = WMP.resolution_par_algo_genetique(maxsize, maxgen, verbose=affichage)
    else:
        nb_essais = -1
    tps_fin = time.perf_counter()

    # calcul du temps d'exécution
    tps_total = tps_fin - tps_debut

    return nb_essais, tps_total


def lancer_all_algo(liste_tailles, liste_algo, nb_tours, dictionnaire, trie, dossier, maxsize=5, maxgen=20, affichage=False):
    """
    Fonction qui lance tous les algorithmes de la liste et renvoie le nombre d'essais moyen par taille et par algorithme,
    ainsi que le temps moyen d'exécution.
    Les listes retournées sont de format : len(liste_tailles) x len(liste_algo)
    :param liste_tailles: liste des tailles du mot secret
    :param liste_algo: liste des noms des algorithmes
    :param nb_tours: nombre de fois qu'on lance les algorithmes
    :param maxsize: taille max de l'ensemble E pour l'algorithme génétique
    :param maxgen: nombre max de génération pour l'algorithme génétique
    :param affichage: si on veut l'affichage des tentatives
    :type liste_tailles: list[int]
    :type liste_algo: list[str]
    :type nb_tours: int
    :type maxsize: int
    :type maxgen: int
    :type affichage: bool
    :return: liste nombre d'essais moyen, liste temps moyen d'exécution
    :rtype: (list[list[int]], list[list[float]])
    """

    liste_all_essais = []   # liste de nombres d'essais moyen pour chaque taille et chaque algo
    liste_all_tps = []  # liste de temps moyen pour chaque taille et chaque algo

    # pour chaque taille du mot secret
    for taille in liste_tailles:

        liste_moy_essais = []
        liste_moy_tps = []

        # pour chaque algo
        for algo in liste_algo:
            liste_nb_essais = []
            liste_tps = []

            f = open(dossier+algo+"_"+str(taille)+".txt", "a")

            # nb_tours exécutions des algorithmes
            for i in range(nb_tours):

                # initialisation du mot secret
                mot_secret = utils.generer_mot_secret(dictionnaire, n=taille)

                if affichage:
                    print("\nmot secret:\t{}".format(liste_mot_en_str(mot_secret).upper()))

                nb_essais, tps_total = lancer_algo(mot_secret, dictionnaire, trie, algo, maxsize=maxsize, maxgen=maxgen,
                                                   affichage=affichage)
                liste_nb_essais.append(nb_essais)
                liste_tps.append(tps_total)
                f.write(mot_secret+","+str(nb_essais)+","+str(tps_total)+"\n")

            liste_moy_essais.append(mean(liste_nb_essais))
            liste_moy_tps.append(mean(liste_tps))

            f.close()

        liste_all_essais.append(liste_moy_essais)
        liste_all_tps.append(liste_moy_tps)

    return liste_all_essais, liste_all_tps


def recuperer_donnees_pour_graphe(liste_tailles, liste_algo, liste_all_essais, liste_all_tps):
    """
    Fonction qui récupérer les données des algorithmes pour les mettre au bon format pour faire un graphe du nombre
    d'essais moyen et temps moyen d'exécution de chaque algorithme en fonction de la taille du mot secret.
    Les listes retournées sont de format : len(liste_algo) x len(liste_tailles)
    :param liste_tailles: liste des tailles du mot secret
    :param liste_algo: liste des noms des algorithmes
    :param liste_all_essais: liste nombre d'essais moyen
    :param liste_all_tps: liste temps moyen d'exécution
    :type liste_tailles: list[int]
    :type liste_algo: list[str]
    :type liste_all_essais: list[list[int]]
    :type liste_all_tps: list[list[float]]
    :return: liste nombre d'essais moyen, liste temps moyen d'exécution
    :rtype: (list[list[int]], list[list[float]])
    """

    liste_donnees_essais = []   # liste de nombres d'essais moyen pour chaque algo et chaque taille
    liste_donnees_tps = []  # liste de temps moyen pour chaque algo et chaque taille

    # initialiser les listes des données
    for i, algo in enumerate(liste_algo):
        liste_tmp = []
        for j, taille in enumerate(liste_tailles):
            liste_tmp.append(-1)
        liste_donnees_essais.append(copy.deepcopy(liste_tmp))
        liste_donnees_tps.append(copy.deepcopy(liste_tmp))

    # récupérer les données
    for i, taille in enumerate(liste_tailles):
        for j, algo in enumerate(liste_algo):
            liste_donnees_essais[j][i] = liste_all_essais[i][j]
            liste_donnees_tps[j][i] = liste_all_tps[i][j]

    return liste_donnees_essais, liste_donnees_tps


def afficher_graphe(liste_tailles, liste_algo, liste_donnees_essais, liste_donnees_tps, nb_tours, taille_min, taille_max, nom_dossier):
    """
    Fonction qui plot le nombre d'essais moyen et le temps moyen d'exécution de chaque algorithme en fonction de la taille du mot secret.
    :param liste_tailles: liste des tailles du mot secret
    :param liste_algo: liste des noms des algorithmes
    :param liste_donnees_essais: liste nombre d'essais moyen
    :param liste_donnees_tps: liste temps moyen d'exécution
    :type liste_tailles: list[int]
    :type liste_algo: list[str]
    :type liste_donnees_essais: list[list[int]]
    :type liste_donnees_tps: list[list[float]]
    :return: None
    """

    # récupérer le nom des algo
    noms_aglo = ""
    for algo in liste_algo:
        noms_aglo += algo+"_"

    fig, axs = plt.subplots(1, 2, figsize=(18, 8))

    for i, algo in enumerate(liste_algo):
        axs[0].plot(liste_tailles, liste_donnees_essais[i], label=algo)
        axs[1].plot(liste_tailles, liste_donnees_tps[i], label=algo)

    axs[0].set_title("nombre d'essais moyen de chaque algorithme en fonction de la taille du mot secret")
    axs[0].set_xlabel("taille du mot secret")
    axs[0].set_ylabel("nombre d'essais moyen")

    axs[1].set_title("temps moyen d'exécution de chaque algorithme en fonction de la taille du mot secret")
    axs[1].set_xlabel("taille du mot secret")
    axs[1].set_ylabel("temps moyen")

    plt.legend()
    # plt.show()
    path = "./{}/n{}_min{}_max{}_{}".format(nom_dossier, nb_tours, taille_min, taille_max, noms_aglo)
    plt.savefig(path)


if __name__ == "__main__":

    file_path = "./dico.txt"
    dictionnaire = utils.lire_dictionnaire(file_path)  # lecture du dictionnaire
    trie = utils.lire_dictionnaire_trie(file_path)

    d = datetime.datetime.today()
    nom_run = d.strftime("%Y_%m_%d-%H:%M:%S")
    dossier = "./test_data/"+nom_run+"/"
    
    try:
        os.makedirs(dossier)
    except OSError:
        pass

    print("Résultats dans : "+dossier)

    affichage = True   # si on veut l'affichage des tentatives
    
    nb_tours = 20        # nombre de fois qu'on exécute les algorithmes
    taille_min = 4      # taille minimale du mot secret
    taille_max = 8      # taille maximale du mot secret

    maxsize = 5         # taille max de l'ensemble E
    maxgen = 20         # nombre max de générations

    # liste des tailles voulues pour le mot secret
    liste_tailles = [i for i in range(taille_min, taille_max + 1)]
    # nom de tous les algorithmes
    # liste_algo = ["csp_rac", "csp_fc", "csp_opt", "ag", "ag_opt"]
    liste_algo = ["csp_rac"]

    if affichage:
        print("========== Bienvenue dans Wordle Mind ==========")

    # exécuter tous les algorithmes
    liste_all_essais, liste_all_tps = lancer_all_algo(liste_tailles, liste_algo, nb_tours, dictionnaire, trie, dossier, maxsize=maxsize, maxgen=maxgen, affichage=affichage)

    # récupérer les données pour plot
    liste_donnees_essais, liste_donnees_tps = recuperer_donnees_pour_graphe(liste_tailles, liste_algo, liste_all_essais, liste_all_tps)

    # plot
    afficher_graphe(liste_tailles, liste_algo, liste_donnees_essais, liste_donnees_tps, nb_tours, taille_min, taille_max, dossier)