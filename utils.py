import string
import collections
import random


alphabet = list(string.ascii_lowercase)

# Feedback : nombre de lettres correctes (bien placées),
#            nombre de lettre proches (mal placées)
Feedback = collections.namedtuple('Feedback', ['correct', 'proche'])


def generer_mot_secret(n, dictionnaire):
    """
    Fonction qui génère aléatoirement un mot de taille n du dictionnaire.

    :param n: nombre de lettres du mot secret
    :param dictionnaire: dictionnaire de mots

    :type n: int
    :type dictionnaire: dict[int, list[list[str]]]

    :return: un mot du dictionnaire
    :rtype: list[str]
    """
    return random.choice(dictionnaire[n])


def lire_dictionnaire(nom_fichier):
    """
    Fonction qui lit les mots d'un dictionnaire et les met dans un dictionnaire qui a pour clé la taille des mots,
    et pour valeur la liste des mots correspondants à la taille de la clé.

    :param nom_fichier: chemin du fichier
    :type nom_fichier: str

    :return: un dictionnaire de mots trié par taille
    :rtype: dict[int, list[list[str]]]
    """

    fichier = open(nom_fichier, "r")
    dictionnaire = dict()

    for mot in fichier:
        mot = mot.strip('\n')

        m = []
        for lettre in mot:
            m.append(lettre)

        taille = len(mot)
        liste = dictionnaire.get(taille, [])
        liste.append(m)
        dictionnaire.update({taille: liste})

    fichier.close()
    return dictionnaire


def enlever_lettres_correctes(mot_actuel, proposition):
    """
    Fonction qui enlève les lettres correctes du mot actuel et du mot proposé.

    :param mot_actuel: mot actuel
    :param proposition: mot proposé

    :type mot_actuel: list[str]
    :type proposition: list[str]

    :return: tuple de mots où les lettres correctes sont enlevés
    :rtype: (list[str], list[str])
    """
    actuel = [a for (a, b) in zip(mot_actuel, proposition) if a != b]
    guess = [b for (a, b) in zip(mot_actuel, proposition) if a != b]

    # transformer la liste de string en une chaine de caractère
    actuel = ''.join(map(str, actuel))
    guess = ''.join(map(str, guess))

    return actuel, guess


def recuperer_nb_lettres_proches(mot_actuel, proposition):
    """
    Fonction qui renvoie le nombre total des lettres proches (mal placées) du mot proposé par rapport au mot actuel.

    :param mot_actuel: mot actuel
    :param proposition: mot proposé

    :type mot_actuel: list[str]
    :type proposition: list[str]

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
        pos = mot_actuel.find(lettre)
        if pos >= 0:
            # enlever toutes les occurrences de la lettre du mot actuel pour éviter de la compter à nouveau
            mot_actuel = mot_actuel[:pos] + mot_actuel[pos + 1:]

            # incrémenter le nombre de lettres proches
            nb_lettres_proches += 1

    return nb_lettres_proches


def recuperer_nb_lettres_correctes(mot_actuel, proposition):
    """
    Fonction qui renvoie le nombre total des lettres correctes (bien placées) du mot proposé par rapport au mot actuel.

    :param mot_actuel: mot actuel
    :param proposition: mot proposé

    :type mot_actuel: list[str]
    :type proposition: list[str]

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

    :type mot_actuel: list[str]
    :type proposition: list[str]

    :return: feedback (nombre de lettres correctes et proches)
    :rtype: Feedback
    """
    fb = Feedback(recuperer_nb_lettres_correctes(mot_actuel, proposition),
                  recuperer_nb_lettres_proches(mot_actuel, proposition))
    return fb


def test_compatibilite(proposition, feedback, mot_possible):
    """
    Fonction qui retourne vrai si le mot est possible étant donné le feedback et le mot proposé, faux sinon.

    :param proposition: mot proposé
    :param feedback: feedback (nombres des lettres correctes et proches)
    :param mot_possible: mot possible

    :type proposition: list[str]
    :type feedback: Feedback
    :type mot_possible: list[str]

    :return: vrai ou faux
    :rtype: bool
    """
    # si le feedback du mot proposé et celui du mot possible est le même
    # c'est-à-dire si le nombre des lettres correctes et proches sont les mêmes pour les deux mots
    return feedback == recuperer_feedback(mot_possible, proposition)


def nb_incompatibilites(mot, tentatives_precedentes):
    cpt_incompatibilites = 0
    for ancien_mot, feedback in tentatives_precedentes:
        compatible = test_compatibilite(ancien_mot, feedback, mot)
        if not compatible:
            cpt_incompatibilites += 1

    return cpt_incompatibilites
