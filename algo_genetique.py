import random
import time
import numpy as np

import utils
import WordleMindProblem as WMP


def mutation_remplacement(probabilite, mot):
    """
    Changement aléatoire d'un caractère.
    Attention : changement fait directement sur le mot passé en paramètre.

    :param probabilite: probabilité de mutation (entre 0 et 1)
    :param mot: mot à changer

    :type probabilite: float
    :type mot: list[str]

    :return: vrai si mutation a eu lieu
    :rtype: bool
    """

    if random.random() > probabilite:
        return False

    pos = random.choice(range(len(mot)))
    mot[pos] = random.choice(utils.alphabet)

    return True


def mutation_echange(probabilite, mot):
    """
    Echange entre deux caractères.
    """

    if random.random() > probabilite:
        return False

    indices = range(len(mot))
    pos1 = random.choice(indices)
    pos2 = random.choice(indices)
    tmp = mot[pos1]
    mot[pos1] = mot[pos2]
    mot[pos2] = mot[pos1]

    return True


def mutation_renversement(probabilite, mot):
    """
    Renversement d'une sous-séquence de caractères du mot.
    """

    if random.random() > probabilite:
        return False

    indices = range(len(mot))
    pos1 = random.choice(indices)
    pos2 = random.choice(indices[pos1:]) + 1
    substring = reversed(mot[pos1:pos2])
    mot[pos1:pos2] = substring

    return True


def croisement(probabilite, mot1, mot2):
    if random.random() > probabilite:
        return False

    indices = range(1, len(mot1))
    pos = random.choice(indices)
    tmp = mot1.copy()
    mot1 = mot1[:pos] + mot2[pos:]
    mot2 = mot2[:pos] + tmp[pos:]

    return True


def mot_proche(mot, dictionnaire):
    """
    Retourne le mot le plus proche dans le dictionnaire au sens de la distance d'édition (le mot lui-même s'il existe).
    """

    # pour optimiser il faudrait une structure de données qui stocke
    # les mots du dictionnaire par ordre alphabétique (une structure par taille de mot)
    taille_mot = len(mot)
    liste_mots = dictionnaire[taille_mot]
    diff_min = float('inf')
    meilleur_mot = mot

    for m in liste_mots:
        if m == mot:
            return mot
        else:
            diff = 0
            for i in range(taille_mot):
                if mot[i] != m[i]:
                    diff += 1
            if diff < diff_min:
                diff_min = diff
                meilleur_mot = m

    return meilleur_mot


def engendrer_E(tentative_precendente, dictionnaire, tentatives, maxsize, maxgen):
    taille_pop = 5
    nb_parents = 2

    parents = [tentative_precendente] * nb_parents

    enfants = []
    nb_enfants = 0

    gen = 0
    total_time = 0

    while total_time < 300 and nb_enfants == 0:

        start = time.time()

        while nb_enfants < maxsize and gen < maxgen:

            population = []
            fitnesses = []
            for i in range(taille_pop):
                enfant = random.choice(parents).copy()
                mutation_remplacement(0.4, enfant)
                mutation_echange(0.4, enfant)
                mutation_renversement(0.4, enfant)
                enfant = mot_proche(enfant, dictionnaire)

                fitness = -utils.nb_incompatibilites(enfant, tentatives) - 1
                if fitness == -1:
                    enfants.append(enfant)
                    nb_enfants += 1

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
        if nb_enfants == 0:
            gen = 0

    if total_time >= 300 and nb_enfants == 0:
        print("La méthode a échouée (timeout).")
        raise TimeoutError()

    return enfants
