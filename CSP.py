import random
import time
import utils


def filtrer_propositions(pool, proposition, feedback):
    """
    Fonction qui filtre l'ensemble des possibilités (pool) et élimine celles qui ne peuvent pas
    être le mot secret selon le feedback (nombres des lettres correctes et proches).

    :param pool: liste des mots possibles
    :param proposition: mot proposé
    :param feedback: feedback

    :type pool: list[list[str]]
    :type proposition: list[str]
    :type feedback: Feedback

    :return: liste de mots possibles filtrés
    :rtype: list[list[str]]
    """

    # pour chaque mot possible (pour chaque mot du pool des possibilités)
    # si le mot est possible selon le feedback et si le mot n'est pas déjà le mot proposé
    return [mot for mot in pool if utils.test_compatibilite(proposition, feedback, mot) and (mot != proposition)]


def donner_proposition(pool, feedback):
    """
    Fonction qui renvoie le meilleur choix de mot parmi les mots possibles (pool)
    selon le feedback (nombres des lettres correctes et proches).

    :param pool: liste des mots possibles
    :param feedback: feedback

    :type pool: list[list[str]]
    :type feedback: Feedback

    :return: un mot
    :rtype: str
    """

    longueur_minimale = float('infinity')
    mot_choisi = None
    # mp = []  # liste (mot actuel, nombre de mots du pool ayant le même feedback que le mot actuel)
    # mp_fb = []  # liste des mots du pool ayant le même feedback que le mot actuel

    # pour chaque mot possible (pour chaque mot du pool des possibilités)
    for mot_possible in pool:
        # on filtre les possibilités pour le mot_possible
        # c'est-à-dire qu'on récupère les mots du pool ayant le même feedback que le mot_possible
        liste_mots_possibles = filtrer_propositions(pool, mot_possible, feedback)
        # nombre de mots du pool ayant le même feedback que le mot_possible
        nb_mots_possibles = len(liste_mots_possibles)
        # mp.append((mot_possible, nb_mots_possibles))

        # le pire cas : quand le feedback reste le même au prochain tour
        # (quand on ne gagne aucune informations supplémentaires sur les lettres du mot secret)
        # on cherche à ce que dans le pire cas, l'espace de recherche soit le plus petit possible
        # (d'où l'intérêt de choisir la longueur minimale ici)
        # dans le cas où nb_mots_possibles = 0 (quand aucun mot du pool n'a le même feedback que le mot_possible)
        # ça veut dire que si le mot choisi n'est pas le bon, ça donnera forcément des informations en plus
        if longueur_minimale > nb_mots_possibles:
            longueur_minimale = nb_mots_possibles
            mot_choisi = mot_possible
            # mp_fb = liste_mots_possibles

    # mp.sort(key=lambda x: x[1])
    # print("mp : ", mp)
    # print("mp_fb : ", mp_fb)

    return mot_choisi


def verifie_consistance_locale(instanciation, contraintes):
    """
    Fonction qui vérifie la consistance locale de l'instanciation donnée avec les contraintes.

    :param instanciation: une instanciation
    :param contraintes: liste des contraintes

    :type instanciation: list[str]
    :type contraintes:

    :return: vrai si consistance locale, faux sinon
    :rtype: bool
    """

    # TODO
    return True


def verifie_consistance_globale(instanciation, tentatives, dictionnaire):
    """
    Fonction qui vérifie la consistance globale de l'instanciation donnée avec les contraintes et le dictionnaire.

    :param instanciation: une instanciation
    :param tentatives: liste des tentatives précédentes
    :param dictionnaire: dictionnaire de mots

    :type instanciation: list[str]
    :type tentatives: list[(list[str], Feedback)]
    :type dictionnaire: dict[int, list[lits[str]]]

    :return: vrai si consistance globale, faux sinon
    :rtype: bool
    """

    # teste la compatibilité du mot avec les tentatives précédentes
    if utils.get_nb_incompatibilites(instanciation, tentatives) != 0:
        return False

    # teste l'existence du mot dans le dictionnaire
    taille_mot = len(instanciation)
    liste_mots = dictionnaire[taille_mot]

    for m in liste_mots:
        if m == instanciation:
            return True

    # TODO other constraints
    return False


def instancier_variable(lettres_restantes, instanciation_partielle):
    """
    Fonction qui instancie la variable en vérifiant les contraintes locales.

    :param lettres_restantes: liste des lettres restantes possibles
    :param instanciation_partielle: une instanciation

    :type lettres_restantes: list[str]
    :type instanciation_partielle: list[str]

    :return: réussite de l'instanciation, liste des lettres restantes après instantiation, instanciation courante
    :rtype: (bool, list[str], list[str])
    """

    # tant qu'il reste des lettres
    while lettres_restantes:
        # prendre la premiere lettre de la liste
        lettre = lettres_restantes.pop(0)
        # faire uns instanciation avec cette lettre
        instanciation_courante = instanciation_partielle + [lettre]

        # si cette instanciation est possible,
        # alors on retourne vrai avec la liste des lettres restantes et l'instanciation courante
        if verifie_consistance_locale(instanciation_courante, []):  # TODO
            return True, lettres_restantes, instanciation_courante

    return False, [], instanciation_partielle


def forward_checking(instanciation_partielle, all_lettres_possibles, tentatives, dictionnaire):
    # TODO
    pass


##### OLD #####

# def RAC(var, n, instanciation_partielle, domaines, tentatives):
#     """
#     Instancie les variables restantes de manière récursive.
#
#     :param var: prochaine variable à instancier
#     :type var: int
#
#     :param n: longueur du mot complet
#     :type n: int
#
#     :param instanciation_partielle: instanciation du mot jusqu'à la variable var - 1
#     :type instanciation_partielle: list[str]
#
#     :param domaines: dictionnaire qui a pour clés les numéros de variables, et pour valeurs les domaines de chaque variable
#     :type domaines: dict(int: list[str])
#
#     :return: booléen représentant la réussite du reste de l'instanciation, instanciation complétée si réussite, liste vide sinon
#     :rtype: bool, list[str]
#     """
#
#     i = 0
#     while i < 26:
#         lettre = domaines[var][i]
#         instanciation_courante = instanciation_partielle+[lettre]
#         local_ok = consistance_locale(instanciation_courante, [])
#
#         if local_ok:
#             # si on vient d'instancier la dernière variable, on teste la consistence globale et la compatibilité
#             # si tout va bien, on fait une tentative
#             # sinon on continue la recherche d'une instanciation de la variable courante
#             if var == n:
#                 if consistance_globale(instanciation_courante, []):
#                     if utils.nb_incompatibilites(instanciation_courante, tentatives) == 0:
#                         fin, feedback = tentative(instanciation_courante)
#                     if fin:
#                         return True, instanciation_courante
#
#             # si on vient d'instancier une variable qui n'est pas la dernière, on procède à l'instanciation des variables suivantes
#             else:
#                 instanciation_reussie, instanciation_complete = RAC(i+1, n, instanciation_courante, domaines, tentatives)
#                 if instanciation_reussie:
#                     return instanciation_reussie, instanciation_complete
#
#         i += 1
#
#     return False, []
#
#
# def wordlemind_csp(dictionnaire, taille_mot):
#     """
#     Modélisation du Wordle Mind et résolution par CSP.
#
#     :param dictionnaire: dictionnaire de mots
#     :param taille_mot: taille du mot qu'on veut générer
#
#     :type dictionnaire: dict[int, list[list[str]]]
#     :type taille_mot: int
#
#     :return: none
#     """
#
#     fin = False  # flag pour savoir quand le jeu se termine
#     nb_tour = 0  # nombre de tours effectués
#
#     # choix aléatoire du mot secret
#     mot_secret = random.choice(dictionnaire[taille_mot])
#     # secret_word = lettre_en_chiffre(mot_secret)  # transformation du mot secret en chiffres
#
#     # sélection des mots correspondant à la taille du mot secret
#     liste_mots = dictionnaire[taille_mot]
#     # pool = mot_en_chiffre(liste_mots)  # transformation des mots en chiffres
#     nb_possibilites = len(liste_mots)  # nombre total des mots possibles
#
#     # 1ere proposition de mot, choisi de manière aléatoire
#     proposition = random.choice(liste_mots)
#
#     while not fin:
#         nb_tour += 1
#         print("----- TOUR {} ----- (mot secret: {})".format(nb_tour, mot_secret))
#         print("Proposition : {}".format(proposition))
#
#         # nombres des lettres correctes (bien placées)
#         correctes = utils.recuperer_nb_lettres_correctes(proposition, mot_secret)
#         # nombres des lettres proches (mal placées)
#         proches = utils.recuperer_nb_lettres_proches(proposition, mot_secret)
#
#         print("\tLettres correctes : {}".format(correctes))
#         print("\tLettres proches : {}".format(proches))
#
#         # mise à jour du feedback
#         feedback = utils.Feedback(correctes, proches)
#
#         if proposition == mot_secret:
#             fin = True
#             print("\nGAGNE ! Le mot était bien {}".format(mot_secret))
#         else:
#             liste_mots = filtrer_propositions(liste_mots, proposition, feedback)
#             print("Il reste {} possibilités.\n".format(len(liste_mots)))
#
#             # proposition = random.choice(liste_mots)
#             proposition = donner_proposition(liste_mots, feedback)
#
#     print("Tours effectués: {}/{}".format(nb_tour, nb_possibilites))
#
#
# if __name__ == "__main__":
#     print("========== Bienvenue dans Wordle Mind ========== \n")
#
#     file_path = "./dico.txt"
#     dico = utils.lire_dictionnaire(file_path)
#
#     n = 5
#
#     temps_debut = time.perf_counter()
#     wordlemind_csp(dico, n)
#     temps_fin = time.perf_counter()
#
#     temps_total = temps_fin - temps_debut
#
#     print("Temps: {} s".format(temps_total))
#
