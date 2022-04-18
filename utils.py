import itertools
import string
import collections
import random


# liste des lettres de l'alphabet en lower case
alphabet = list(string.ascii_lowercase)

# Feedback : nombre de lettres correctes (bien placées),
#            nombre de lettre proches (mal placées)
Feedback = collections.namedtuple('Feedback', ['correctes', 'proches'])


def generer_mot_secret(dictionnaire, n=3):
    """
    Fonction qui génère aléatoirement un mot de taille n du dictionnaire.

    :param dictionnaire: dictionnaire de mots
    :param n: nombre de lettres du mot secret

    :type dictionnaire: dict[int, list[list[str]]]
    :type n: int

    :return: un mot du dictionnaire
    :rtype: list[str]
    """

    return random.choice(dictionnaire[n])


def lire_dictionnaire(nom_fichier):
    """
    Fonction qui lit les mots d'un dictionnaire et les met dans un dictionnaire qui a pour clé la taille des mots
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


def lire_dictionnaire_trie(nom_fichier):
    """
    Fonction qui crée un arbre Trie pour représenter le dictionnaire contenu dans le fichier passé en paramètre.

    :param nom_fichier: chemin du fichier
    :type nom_fichier: str

    :return:
    :rtype:
    """

    # La clés du dictionnaire à la racine représentent les tailles des mots.
    # Pour chaque taille de mot, on retrouve un Trie.

    fichier = open(nom_fichier, "r")
    racine_dico = dict()

    for mot in fichier:

        mot = mot.strip('\n')
        taille_mot = len(mot)

        dico_de_travail = racine_dico.setdefault(taille_mot, dict())

        for lettre in mot:
            dico_de_travail = dico_de_travail.setdefault(lettre, dict())

        dico_de_travail["fin"] = "fin"  # pour pouvoir tester l'existence d'un mot qui pourrait être préfixe d'un autre mot

    fichier.close()

    return racine_dico


def present_dans_trie(mot, trie):
    """
    Fonction qui teste la présence d'un mot dans un Trie.

    :return: booléen indiquant la présence ou non du mot
    :rtype: bool
    """

    dico_de_travail = trie[len(mot)]
    for lettre in mot:

        if lettre not in dico_de_travail:
            return False

        dico_de_travail = dico_de_travail[lettre]

    return "fin" in dico_de_travail


def enlever_lettres_correctes(mot_actuel, proposition):
    """
    Fonction qui enlève les lettres correctes du mot actuel et du mot proposé.

    :param mot_actuel: mot actuel
    :param proposition: mot proposé

    :type mot_actuel: list[str]
    :type proposition: list[str]

    :return: tuple de mots où les lettres correctes sont enlevés
    :rtype: (str, str)
    """

    actuel = [a for (a, b) in itertools.zip_longest(mot_actuel, proposition) if a != b or b == None]
    guess = [b for (a, b) in itertools.zip_longest(mot_actuel, proposition) if a != b]

    # transformer la liste de string en une chaine de caractère
    actuel = ''.join(map(str, actuel))
    guess = filter(None, guess) # retire des "None" éventuellement ajoutés lors du zip
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
    print("inside:", mot_actuel, proposition)
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

    :return: vrai si le mot est possible, faux sinon
    :rtype: bool
    """

    # si le feedback du mot proposé et celui du mot possible est le même
    # c'est-à-dire si le nombre des lettres correctes et proches sont les mêmes pour les deux mots
    return feedback == recuperer_feedback(mot_possible, proposition)


def get_nb_incompatibilites(mot, tentatives_precedentes):
    """
    Fonction qui renvoie le nombre d'incompatibilités du mot actuel par rapport aux tentatives précédentes.

    :param mot: mot actuel
    :param tentatives_precedentes: liste des tentatives précédentes

    :return: nombre d'incompatibilités
    """

    cpt_incompatibilites = 0
    for ancien_mot, feedback in tentatives_precedentes:
        compatible = test_compatibilite(ancien_mot, feedback, mot)
        if not compatible:
            cpt_incompatibilites += 1

    return cpt_incompatibilites


def reduire_domaines(mot, feedback, domaines):
    """
    :param mot: mot de la tentative précédente
    :param feedback: feedback de la tentative précédente
    :param domaines: dictionnaire qui contient une liste de lettres acceptables pour chaque variable

    :type mot: list[str]
    :type feedback: Feedback
    :type domaines: dict[int: list[str]]

    :return: none
    """

    if feedback.correctes == 0:
        # si aucune lettre n'est correcte ni proche
        if feedback.proches == 0:
            # on retire toutes les lettres du mot des domaines de toutes les variables
            for i in range(len(mot)):
                for lettre in mot:
                    if lettre in domaines[i]:
                        domaines[i].remove(lettre)

        # si aucune lettre n'est correcte mais certaines sont proches
        else:
            # on retire la lettre instancié pour chaque variable du domaine de cette variable
            # ex : on retire la première lettre du mot de la variable 0 car on sait qu'elle n'apparaitra jamais à cette position
            for i in range(len(mot)):
                if mot[i] in domaines[i]:
                    domaines[i].remove(mot[i])
