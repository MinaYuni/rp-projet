import copy
import random

import algo_genetique as ag
import CSP as csp
import utils


class WordleMindProblem:

    def __init__(self, mot_secret, dictionnaire):
        self.mot_secret = mot_secret
        self.dictionnaire = dictionnaire
        self.tentatives = []
        self.nb_tentatives = 0

        # key: taille des mots (int)
        # value: liste des lettres d'un mot de taille key (list[list[str]])
        self.domaines = dict()
        for i in range(len(self.mot_secret)):
            self.domaines[i] = utils.alphabet.copy()

        self.contraintes = []

    def resolution_par_CSP_A1(self):

        n = len(self.mot_secret)
        fin = False
        var = 0
        instanciation_courante = []
        all_lettres_restantes = copy.deepcopy(self.domaines)

        while not fin:
            reussite, lettres_restantes, instanciation_courante = csp.instancier_variable(all_lettres_restantes[var],
                                                                                          instanciation_courante)
            if reussite:
                all_lettres_restantes[var] = lettres_restantes
                var += 1

                if var == n:
                    if csp.consistance_globale(instanciation_courante, [],
                                               self.dictionnaire) and utils.nb_incompatibilites(instanciation_courante,
                                                                                                self.tentatives) == 0:
                        fin, feedback = self.tentative(instanciation_courante)
                        if fin:
                            return self.nb_tentatives
                        else:
                            var -= 1
                            instanciation_courante = instanciation_courante[:var]
                    else:
                        var -= 1
                        instanciation_courante = instanciation_courante[:var]

            else:
                all_lettres_restantes[var] = copy.copy(self.domaines[var])
                var -= 1
                instanciation_courante = instanciation_courante[:var]

        return self.nb_tentatives

    def resolution_par_CSP_A2(self):
        pass

    def resolution_par_CSP_opt(self):
        pass

    def resolution_par_algo_genetique(self, maxsize, maxgen):

        mot_choisi = random.choice(self.dictionnaire[len(self.mot_secret)])
        fin, feedback = self.tentative(mot_choisi)

        while not (fin):
            E = ag.engendrer_E(mot_choisi, self.dictionnaire, self.tentatives, maxsize, maxgen)
            mot_choisi = random.choice(E)
            fin, feedback = self.tentative(mot_choisi)

        return self.nb_tentatives

    def tentative(self, mot):
        # fonction à utiliser pour faire une tentative pour bien séparer le côté solveur et le côté du système du jeu
        # les fonctions statiques pouvant être appelées pour autre chose
        # et aussi pour stocker les tentatives qq part

        print("Tentative:", mot)
        self.nb_tentatives += 1
        if mot == self.mot_secret:
            return True, utils.Feedback(len(mot), 0)

        feedback = utils.recuperer_feedback(self.mot_secret, mot)
        self.tentatives.append((mot, feedback))
        return False, feedback
