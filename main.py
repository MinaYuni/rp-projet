import random
import string
import time
import collections


alphabet = list(string.ascii_lowercase)
Feedback = collections.namedtuple('Feedback', ['correct', 'proche'])


def lire_dictionnaire(nom_fichier):
    """
    Fonction qui lit les mots d'un dictionnaire et les met dans une liste.

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


def enlever_lettres_correctes(mot_actuel, proposition):
    """
    Fonction qui enlève les lettres correctes du mot actuel et du mot proposé.

    :param mot_actuel: mot actuel
    :param proposition: mot proposé

    :type mot_actuel: str
    :type proposition: str

    :return: tuple de mots où les lettres correctes sont enlevés
    :rtype: (str, str)
    """
    actuel = [a for (a, b) in zip(mot_actuel, proposition) if a != b]
    guess = [b for (a, b) in zip(mot_actuel, proposition) if a != b]

    actuel = ''.join(map(str, actuel))
    guess = ''.join(map(str, guess))

    return actuel, guess


def recuperer_nb_lettres_proches(mot_actuel, proposition):
    """
    Fonction qui renvoie le nombre total des lettres proches (mal placées) du mot proposé par rapport au mot actuel.

    :param mot_actuel: mot actuel
    :param proposition: mot proposé

    :type mot_actuel: str
    :type proposition: str

    :return: nombre total des lettres proches
    :rtype: int
    """
    # enlever les lettres correctes pour éviter de les compter deux fois
    mot_actuel, proposition = enlever_lettres_correctes(mot_actuel, proposition)
    # print(mot_actuel)

    # nombre de lettres proches (mal placées)
    nb_lettres_proches = 0

    # pour chaque lettre du mot proposé
    for lettre in proposition:
        # si la lettre est dans le mot actuel
        if lettre in mot_actuel:
            # enlever toutes les occurrences de la lettre du mot actuel pour éviter de la compter à nouveau
            mot_filtre = filter(lambda l: l != lettre, mot_actuel)
            mot_actuel = ''.join(mot_filtre)

            # incrémenter le nombre de lettres proches
            nb_lettres_proches += 1

    return nb_lettres_proches


def recuperer_nb_lettres_correctes(mot_actuel, proposition):
    """
    Fonction qui renvoie le nombre total des lettres correctes (bien placées) du mot proposé par rapport au mot actuel.

    :param mot_actuel: mot actuel
    :param proposition: mot proposé

    :type mot_actuel: str
    :type proposition: str

    :return: nombre total des lettres correctes
    :rtype: int
    """
    nb_lettres_correctes = sum([1 for (a, b) in zip(mot_actuel, proposition) if a == b])
    return nb_lettres_correctes


def recuperer_feedback(mot_actuel, proposition):
    """
    Fonction qui compare les deux mots l'un par rapport à l'autre et renvoie un feedback
    (c'est-à-dire le nombre de lettres correctes et proches).

    :param mot_actuel: mot actuel
    :param proposition: mot proposé

    :type mot_actuel: str
    :type proposition: str

    :return: feedback (nombre de lettres correctes et proches)
    :rtype: Feedback
    """
    fb = Feedback(recuperer_nb_lettres_correctes(mot_actuel, proposition),
                  recuperer_nb_lettres_proches(mot_actuel, proposition))
    return fb


def is_match(proposition, feedback, mot_possible):
    """
    Fonction qui retourne vrai si le mot est possible étant donné le feedback et le mot proposé, faux sinon.

    :param proposition: mot proposé
    :param feedback: feedback (nombres des lettres correctes et proches)
    :param mot_possible: mot possible

    :type proposition: str
    :type feedback: Feedback
    :type mot_possible: str

    :return: vrai ou faux
    :rtype: bool
    """
    # si le feedback du mot proposé et celui du mot possible est le même
    # c'est-à-dire si le nombre des lettres correctes et proches sont les mêmes pour les deux mots
    return feedback == recuperer_feedback(mot_possible, proposition)


def filtrer_propositions(pool, proposition, feedback):
    """
    Fonction qui filtre l'ensemble des possibilités et élimine celles qui ne peuvent pas être le mot secret.

    :param pool: liste des mots possibles
    :param proposition: mot proposé
    :param feedback: feedback (nombres des lettres correctes et proches)

    :type pool: list[str]
    :type proposition: str
    :type feedback: Feedback

    :return: liste de mots possibles filtrés
    :rtype: list[str]
    """
    # pour chaque mot possible (pour chaque mot du pool des possibilités)
    for mot_possible in pool:
        # si le mot est possible selon les feedbacks et si le mot n'est pas déjà le mot proposé
        if is_match(proposition, feedback, mot_possible) and (mot_possible != proposition):
            yield mot_possible


def donner_proposition(pool, feedback):
    """
    Fonction qui renvoie le meilleur choix de mot parmi les mots possibles et les lettres correctes et proches.

    :param pool: liste des mots possibles
    :param feedback: feedback (nombres des lettres correctes et proches)

    :type pool: list[str]
    :type feedback: Feedback

    :return: un mot
    :rtype: str
    """
    longueur_minimale = float('infinity')
    mot_choisi = None

    # pour chaque mot possible (pour chaque mot du pool des possibilités)
    for mot_possible in pool:
        # on filtre les possibilités
        mots_possibles = list(filtrer_propositions(pool, mot_possible, feedback))
        nb_mots_possibles = len(mots_possibles)

        if longueur_minimale > nb_mots_possibles:
            longueur_minimale = nb_mots_possibles
            mot_choisi = mot_possible

    return mot_choisi


def wordlemind_csp(dictionnaire):
    """
    Modélisation du Wordle Mind et résolution par CSP.

    :param dictionnaire: liste de mots du dictionnaire
    :type dictionnaire: list[str]

    :return: none
    """
    fin = False  # flag pour savoir quand le jeu se termine
    nb_tour = 0  # nombre de tours effectués

    # choix aléatoire du mot secret
    mot_secret = random.choice(dictionnaire)
    # secret_word = lettre_en_chiffre(mot_secret)  # transformation du mot secret en chiffres
    taille = len(mot_secret)  # taille du mot secret (c'est-à-dire celle du mot à deviner)

    # sélection des mots correspondant à la taille du mot secret
    liste_mots = list(filter(lambda mot: len(mot) == taille, dictionnaire))
    # pool = mot_en_chiffre(liste_mots)  # transformation des mots en chiffres
    nb_possibilites = len(liste_mots)  # nombre total des mots possibles

    # 1ere proposition de mot, choisi de manière aléatoire
    proposition = random.choice(liste_mots)

    while not fin:
        nb_tour += 1
        print("----- TOUR {} ----- {}".format(nb_tour, mot_secret))
        print("Proposition : {}".format(proposition))

        # nombres des lettres correctes (bien placées)
        correctes = recuperer_nb_lettres_correctes(proposition, mot_secret)
        # nombres des lettres proches (mal placées)
        proches = recuperer_nb_lettres_proches(proposition, mot_secret)

        print("\tLettres correctes : {}".format(correctes))
        print("\tLettres proches : {}".format(proches))

        # mise à jour du feedback
        feedback = Feedback(correctes, proches)

        if proposition == mot_secret:
            fin = True
            print("\nGAGNE ! Le mot était bien {}.".format(mot_secret.upper()))
        else:
            liste_mots = list(filtrer_propositions(liste_mots, proposition, feedback))
            print("Il reste {} possibilités.\n".format(len(liste_mots)))

            proposition = donner_proposition(liste_mots, feedback)

    print("Tours effectués : {}/{}".format(nb_tour, nb_possibilites))


if __name__ == "__main__":
    print("========== Bienvenue dans Wordle Mind ========== \n")

    file_path = "./dico.txt"
    dico = lire_dictionnaire(file_path)

    temps_debut = time.perf_counter()
    wordlemind_csp(dico)
    temps_fin = time.perf_counter()

    temps_total = temps_fin - temps_debut

    print("Temps : {} s".format(temps_total))
