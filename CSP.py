import copy
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

    # TODO ?
    return True


def verifie_consistance_globale(instanciation, tentatives, dictionnaire, type_dico="trie"):
    """
    Fonction qui vérifie la consistance globale de l'instanciation donnée avec les contraintes et le dictionnaire.

    :param instanciation: une instanciation
    :param tentatives: liste des tentatives précédentes
    :param dictionnaire: dictionnaire de mots
    :param type_dico: "dict" ou "trie"

    :type instanciation: list[str]
    :type tentatives: list[(list[str], Feedback)]
    :type dictionnaire: dict[int, list[lits[str]]]
    :type type_dico: str

    :return: vrai si consistance globale, faux sinon
    :rtype: bool
    """

    # teste la compatibilité du mot avec les tentatives précédentes
    if utils.get_nb_incompatibilites(instanciation, tentatives) != 0:
        return False

    # teste l'existence du mot dans le dictionnaire
    if type_dico == "dict":

        taille_mot = len(instanciation)
        liste_mots = dictionnaire[taille_mot]

        for m in liste_mots:
            if m == instanciation:
                return True

        return False

    elif type_dico == "trie":
        
        existe = utils.present_dans_trie(instanciation, dictionnaire)
        
        if not existe:
            return False

        return True

    print("Type du dictionnaire inconnu.")

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
        # faire une instanciation avec cette lettre
        instanciation_courante = instanciation_partielle + [lettre]

        # si cette instanciation est possible,
        # alors on retourne vrai avec la liste des lettres restantes et l'instanciation courante
        if verifie_consistance_locale(instanciation_courante, []):  # TODO
            return True, lettres_restantes, instanciation_courante

    return False, [], instanciation_partielle


def forward_checking(instanciation_partielle, taille_mot, all_lettres_restantes, tentatives, trie):
    """

    :param instanciation_partielle: mot partiellement instancié
    :param taille_mot: nombre de lettres du mot secret
    :param all_lettres_restantes: 
    :param tentatives: liste des tentatives précédentes avec leur feedback
    :param trie: dictionnaire sous forme de Trie

    :type instanciation_partielle: list[str]
    :type taille_mot: int
    :type all_lettres_restantes: dict[int, list[str]]
    :type tentatives: list[list[str], Feedback]
    :type trie: 
    """
    
    taille_instanciation = len(instanciation_partielle)

    dico_de_travail = trie[taille_mot]

    # On se positionne au bon niveau du Trie
    for lettre in instanciation_partielle:
        if lettre in dico_de_travail:
            dico_de_travail = dico_de_travail[lettre]

    # On met à jour le domaine de chaque variable qui n'est pas encore instanciée
    # (Toutes les variables sont liées entre elles par le dictionnaire et les infos obtenues lors des tentatives)

    lettres_possibles = dict()
    for i in range(taille_instanciation, taille_mot):
        lettres_possibles[i] = set()

    check_forward(taille_instanciation, taille_mot, all_lettres_restantes, dico_de_travail, lettres_possibles)
    
    lettres_restantes = copy.copy(all_lettres_restantes[taille_instanciation])

    for i in range(taille_instanciation, taille_mot):
        lettres_restantes = copy.copy(all_lettres_restantes[i])
        for lettre in lettres_restantes:
            if lettre not in lettres_possibles[i]:
                all_lettres_restantes[i].remove(lettre)
            

def check_forward(var, taille_mot, all_lettres_restantes, trie_partiel, lettres_possibles):

    if var == taille_mot:
        return

    for k in trie_partiel.keys():
        lettres_possibles[var].add(k)

    lettres_restantes = copy.copy(all_lettres_restantes[var])

    # pour chaque lettre possible pour la variable courante, on ajoute tous les successeurs
    for lettre in lettres_restantes:
        if lettre in trie_partiel:
            check_forward(var+1, taille_mot, all_lettres_restantes, trie_partiel[lettre], lettres_possibles)


def full_look_ahead():
    pass

    

#### OLD ####

# full lookahead ?
# def forward_checking(instanciation_partielle, taille_mot, all_lettres_restantes, tentatives, trie):
    
#     taille_instanciation = len(instanciation_partielle)

#     dico_de_travail = trie[taille_mot]

#     # On se positionne au bon niveau du Trie
#     for lettre in instanciation_partielle:
#         if lettre in dico_de_travail:
#             dico_de_travail = dico_de_travail[lettre]

#     # On met à jour le domaine de chaque variable qui n'est pas encore instanciée
#     # (Toutes les variables sont liées entre elles par le dictionnaire et les infos obtenues lors des tentatives)
#     for i in range(taille_instanciation, taille_instanciation+1):

#         lettres_restantes = copy.copy(all_lettres_restantes[i])

#         for lettre in lettres_restantes:
#             if lettre not in dico_de_travail and lettre in all_lettres_restantes[i]:
#                 all_lettres_restantes[i].remove(lettre)
#                 #print("i:", i, "lettre", lettre)
#             # else:#
#             #     forward_checking(instanciation_partielle+[lettre], taille_mot, all_lettres_restantes, tentatives, trie)