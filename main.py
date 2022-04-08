import numpy as np
import math
import random


def lire_dictionnaire(nom_fichier):
    """
    Fonction qui lit les mots d'un dictionnaire et les retourne dans une liste.

    :param nom_fichier: chemin du fichier
    :type nom_fichier: str

    :return: une liste contenant tous les mots du dictionnaire donnée en paramètre
    :rtype: list[str]
    """
    fichier = open(nom_fichier, "r")
    dictionnaire = []

    for mot in fichier:
        mot = mot.strip('\n')
        dictionnaire.append(mot)

    fichier.close()

    return dictionnaire


def taille_min_max_mot(dictionnaire):
    """
    Fonction qui renvoie la taille minimale et maximale des mots du dictionnaire.

    :param dictionnaire: liste des mots du dictionnaire
    :type dictionnaire: list[str]

    :return: taille minimale et maximale des mots du dictionnaire
    :rtype: (int, int)
    """
    taille_min = 100
    taille_max = 0

    for mot in dictionnaire:
        taille_mot = len(mot)
        if taille_mot > taille_max:
            taille_max = taille_mot
        if taille_mot < taille_min:
            taille_min = taille_mot

    return taille_min, taille_max


def mots_de_taille(dictionnaire, taille):
    """
    Fonction qui sélectionne les mots du dictionnaire qui correspondent à la taille donnée.

    :param dictionnaire: liste des mots du dictionnaire
    :type dictionnaire: list[str]

    :param taille: taille du mot
    :type taille: int

    :return: liste de mots de la taille donnée
    :rtype: list[str]
    """
    mots_correspondant = []
    for mot in dictionnaire:
        if len(mot) == taille:
            mots_correspondant.append(mot)
    return mots_correspondant


def wordlemind_csp(dictionnaire):
    """
    Modélisation du Wordle Mind et résolution par CSP.

    :param dictionnaire: liste des mots du dictionnaire
    :type dictionnaire: list[str]

    :return: none
    """
    fin = False  # flag pour savoir quand le jeu se termine
    nb_tour = 0  # nombre de tours effectués

    # choix aléatoire du mot secret
    mot_secret = random.choice(dictionnaire)
    taille_mot = len(mot_secret)

    # sélection des mots correspondant à la taille du mot secret
    liste_mots = mots_de_taille(dictionnaire, taille_mot)
    taille_liste_mots = len(liste_mots)

    while not fin:
        nb_tour += 1
        # print("----- TOUR {} -----".format(nb_tour))

        mot_choisi = random.choice(liste_mots)
        # print("Mot choisi : {}".format(mot_choisi))

        if mot_choisi == mot_secret:
            print("BRAVO! Le mot est bien {}\n".format(mot_secret.upper()))
            fin = True
        else:
            # print("PERDU!\n")
            liste_mots.remove(mot_choisi)

    print("Nombre de tours total : {}/{}".format(nb_tour, taille_liste_mots))


if __name__ == "__main__":
    print("========== Bienvenue dans Wordle Mind ========== \n")

    file_path = "./dico.txt"
    dico = lire_dictionnaire(file_path)

    wordlemind_csp(dico)
