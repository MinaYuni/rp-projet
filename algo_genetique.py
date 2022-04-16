import copy
import random
import time
import numpy as np

import utils
import WordleMindProblem as WMP


def mutation_remplacement(probabilite, mot):
    """
    Fonction qui change aléatoirement une lettre du mot donné selon une probabilité donnée.
    Attention le changement se fait directement sur le mot passé en paramètre.

    :param probabilite: probabilité de mutation (entre 0 et 1)
    :param mot: mot à changer

    :type probabilite: float
    :type mot: list[str]

    :return: vrai si la mutation a eu lieu, faux sinon
    :rtype: bool
    """

    # si mutation possible
    if random.random() > probabilite:
        return False

    liste_indices = range(len(mot))  # liste des indices du mot

    # choix aléatoire de la position à muter
    pos = random.choice(liste_indices)
    # mutation de la lettre
    mot[pos] = random.choice(utils.alphabet)

    return True


def mutation_echange(probabilite, mot):
    """
    Fonction qui fait un échange aléatoire entre deux lettres du mot donné selon une probabilité donnée.
    Attention le changement se fait directement sur le mot passé en paramètre.

    :param probabilite: probabilité de mutation (entre 0 et 1)
    :param mot: mot à changer

    :type probabilite: float
    :type mot: list[str]

    :return: vrai si la mutation a eu lieu, faux sinon
    :rtype: bool
    """

    # si mutation possible
    if random.random() > probabilite:
        return False

    liste_indices = range(len(mot))  # liste des indices du mot

    # choix aléatoire de deux positions à échanger
    pos1 = random.choice(liste_indices)
    pos2 = random.choice(liste_indices)

    # échange des lettres
    tmp = copy.deepcopy(mot[pos1])
    mot[pos1] = mot[pos2]
    mot[pos2] = tmp

    return True


def mutation_renversement(probabilite, mot):
    """
    Fonction qui fait une inversion d'une sous-séquence de lettres du mot donné selon une probabilité donnée.
    Attention le changement se fait directement sur le mot passé en paramètre.

    :param probabilite: probabilité de mutation (entre 0 et 1)
    :param mot: mot à changer

    :type probabilite: float
    :type mot: list[str]

    :return: vrai si la mutation a eu lieu, faux sinon
    :rtype: bool
    """

    # si mutation possible
    if random.random() > probabilite:
        return False

    liste_indices = range(len(mot))  # liste des indices du mot

    # choix aléatoire de la sous-séquence à inverser
    pos1 = random.choice(liste_indices)
    pos2 = random.choice(liste_indices[pos1:]) + 1

    # inversion de la séquence
    substring = reversed(mot[pos1:pos2])
    mot[pos1:pos2] = substring

    return True


def croisement(probabilite, parents):
    """
    Fonction qui fait un croisement entre deux mots sélectionnés parmi les parents selon une probabilité donnée.

    :param probabilite: probabilité de croisement (entre 0 et 1)
    :param parents: liste des parents parmi lesquels on peut choisir pour faire le croisement

    :type probabilite: float
    :type parents: list[list[str]]

    :return: vrai si le croisement a eu lieu avec le mot généré, faux sinon avec une copie d'un parent aléatoire
    :rtype: bool, enfant
    """

    # si croisement possible
    if random.random() > probabilite:
        return False

    liste_indices = range(1, len(parent1))  # liste des indices du mot

    # choix aléatoire de la position à croiser
    pos = random.choice(liste_indices)
    # croisement
    tmp = copy.deepcopy(parent1)
    parent1 = parent1[:pos] + parent2[pos:]
    parent2 = parent2[:pos] + tmp[pos:]

    return True


def get_mot_proche(mot, dictionnaire):
    """
    Fonction qui retourne le mot le plus proche dans le dictionnaire au sens de la distance d'édition
    (le mot lui-même s'il existe déjà).

    :param mot: un mot
    :param dictionnaire: dictionnaire de mots

    :type mot: list[str]
    :type dictionnaire: dict[int, list[lits[str]]]

    :return: mot le plus proche
    :rtype: list[str]
    """

    # pour optimiser il faudrait une structure de données qui stocke
    # les mots du dictionnaire par ordre alphabétique (une structure par taille de mot)

    taille_mot = len(mot)  # taille du mot donné
    liste_mots = dictionnaire[taille_mot]  # liste de mots qui on la même taille que le mot donné
    diff_min = float('infinity')  # nombre de lettres différentes entre le mot donné et le mot courant
    meilleur_mot = mot  # le mot le plus proche du mot donné

    # pour chaque mot de la liste
    for m in liste_mots:
        # si le mot donné existe déjà, alors le renvoyé
        if m == mot:
            return mot
        else:  # sinon prendre le plus proche
            diff = 0
            # pour chaque position de lettre du mot donné
            for i in range(taille_mot):
                # si la lettre à cette position n'est pas la même que le mot courant
                if mot[i] != m[i]:
                    # incrémenter le nombre de différences
                    diff += 1
            # choisir le mot avec la plus petite différence
            if diff < diff_min:
                diff_min = diff
                meilleur_mot = m

    return meilleur_mot


def engendrer_ens(tentative_precedente, dictionnaire, tentatives, maxsize, maxgen, taille_pop=5, nb_parents=2,
                  proba_mutation_remplacement=0.4, proba_mutation_echange=0.4, proba_mutation_renversement=0.4, 
                  proba_croisement=0.4, timeout=300):
    """
    Fonction qui génère l'ensemble E des mots compatibles avec les tentatives précédentes.

    :param tentative_precedente: dernier mot tenté
    :param dictionnaire: dictionnaire des mots
    :param tentatives: liste des tentatives précédentes
    :param maxsize: taille max de l'ensemble E
    :param maxgen: nombre de générations
    :param taille_pop: taille de la population
    :param nb_parents: nombre de parents à chaque génération
    :param proba_mutation_remplacement: probabilité de mutation par remplacement
    :param proba_mutation_echange: probabilité de mutation par échange
    :param proba_mutation_renversement: probabilité de mutation par renversement
    :param proba_croisement: probabilité de croisement
    :param timeout: temps max d'exécution

    :type tentative_precedente: list[str]
    :type dictionnaire: dict[int, list[list[str]]]
    :type tentatives: list[list[str]]
    :type maxsize: int
    :type maxgen: int
    :type taille_pop: int
    :type nb_parents: int
    :type proba_mutation_remplacement: float
    :type proba_mutation_echange: float
    :type proba_mutation_renversement: float
    :type proba_croisement: float
    :type timeout: int

    :return: l'ensemble E
    :rtype: list[list[str]]
    """

    parents = [tentative_precedente] * nb_parents  # liste des parents

    ens = []  # l'ensemble E
    taille_ens = 0  # taille de l'ensemble E

    gen = 0  # génération actuelle
    total_time = 0  # temps d'exécution de l'algorithme génétique

    # tant que le temps d'exécution est inférieure à 300 s
    # et que l'ensemble E est vide (tant qu'on n'a pas trouvé de mots compatibles)
    while total_time < timeout and taille_ens == 0:
        start = time.time()

        # tant que la taille de l'ensemble E n'a pas atteint sa taille max
        # et que la génération actuelle n'est pas la dernière
        while taille_ens < maxsize and gen < maxgen:
            population = []
            fitnesses = []

            # mutation et croisement de la population
            for i in range(taille_pop):
                # choisir un enfant à muter parmi les parents après croisement
                _, enfant = croisement(proba_croisement, parents)  # Choisir un enfant ou garder les deux ? TODO

                # mutation de l'enfant choisi
                mutation_remplacement(proba_mutation_remplacement, enfant)
                mutation_echange(proba_mutation_echange, enfant)
                mutation_renversement(proba_mutation_renversement, enfant)

                # choisir le mot existant le plus proche
                enfant = get_mot_proche(enfant, dictionnaire)

                # calcul de la fitness de l'enfant
                fitness = - utils.get_nb_incompatibilites(enfant, tentatives) - 1
                # si ce n'est pas incompatible, ajouter l'enfant à l'ensemble E
                if fitness == -1:
                    ens.append(enfant)
                    taille_ens += 1

                # print("pop:", population, "fitnesses:", fitnesses)
                population.append(enfant)
                fitnesses.append(fitness)

            somme = sum(fitnesses)
            distribution_proba = [fitness / somme for fitness in fitnesses]
            indices_parents = np.random.choice(range(5), 2, distribution_proba)
            parents = [population[i] for i in indices_parents]
            gen += 1

        stop = time.time()
        total_time += stop - start

        # si on n'a pas trouvé de mots compatibles, alors on recommence (on revient à la génération 0)
        if taille_ens == 0:
            gen = 0

    # si le temps d'exécution à dépasser 300 s et si on n'a pas trouvé de mots
    if total_time >= timeout and taille_ens == 0:
        print("La méthode a échouée (l'ensemble E est vide après {} s).".format(timeout))
        # raise TimeoutError()

    return ens
