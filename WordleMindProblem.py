import copy
import random

import algo_genetique as ag
import CSP as csp
import utils


class WordleMindProblem:

    def __init__(self, mot_secret, dictionnaire, trie):
        self.mot_secret = mot_secret        # mot secret (list[str])
        self.taille_mot = len(mot_secret)   # taille du mot secret
        self.dictionnaire = dictionnaire    # dictionnaire de mots
        self.trie = trie                    # Trie du dictionnaire
        self.tentatives = []                # liste de tentatives (les mots qui ont été testés)
        self.nb_tentatives = 0              # nombre de tentatives faites

        # key: indice des variables du csp
        # value: domaine des variables (liste de lettres)
        self.domaines = dict()
        for i in range(self.taille_mot):
            self.domaines[i] = utils.alphabet.copy()

        self.contraintes = []  # liste des contraintes


    def resolution_par_CSP(self, type_dico="dict", version="A2", verbose=False):
        """
        Fonction qui fait la résolution de Wordle Mind sous forme de CSP, par Retour Arrière Chronologique (RAC). 
        La version A2 utilise le forward-checking (FC).
        Attention : A2 ne marche qu'avec un Trie.

        :param verbose: si on veut l'affichage des tentatives
        :param type_dico: type du dictionnaire ("dict" ou "trie")
        :param version: "A1" (version basique) ou "A2" (avec FC)

        :type type_dico: str
        :type version: str
        :type verbose: bool

        :return: nombre de tentatives faites
        :rtype: int
        """
        
        if type_dico == "dict":
            dictionnaire = self.dictionnaire
        elif type_dico == "trie":
            dictionnaire = self.trie

        fin = False  # flag pour savoir quand le jeu se termine
        indice_var = 0  # indice de la variable du csp (lettre du mot)
        instanciation_courante = []  # instanciation courante (list[str])
        all_lettres_restantes = copy.deepcopy(self.domaines)  # dictionnaire des lettres restantes pour chaque variable

        # tant qu'on a pas fini (trouvé le mot secret)
        while not fin:

            if indice_var < 0:
                print("Le mot secret n'existe pas dans le dictionnaire.")

            # réussite de l'instanciation, lettres restantes pour la variable courante, instanciation courante
            reussite, lettres_restantes, instanciation_courante \
                = csp.instancier_variable(all_lettres_restantes[indice_var], instanciation_courante)

            # si l'instanciation de la variable courante a réussi
            if reussite:
                all_lettres_restantes[indice_var] = lettres_restantes
                indice_var += 1  # variable suivante

                # si la taille du mot courant est celle du mot secret
                if indice_var == self.taille_mot:
                    # si le mot existe et s'il est compatible
                    if csp.verifie_consistance_globale(instanciation_courante, self.tentatives, dictionnaire, type_dico):

                        # fait une tentative avec l'instanciation courante
                        fin, feedback = self.test_tentative(instanciation_courante, verbose)

                        # si on a trouvé le mot secret, alors on s'arrête et on renvoie le nombre de tentatives faites
                        if fin:
                            return self.nb_tentatives
                        else:  # sinon on reste sur la même variable
                            # met à jour la liste des lettres restantes en fonction de la mise à jour des domaines
                            utils.reduire_domaines(instanciation_courante, feedback, all_lettres_restantes)
                            indice_var -= 1
                            instanciation_courante = instanciation_courante[:indice_var]
                    else:  # sinon on reste sur la même variable
                        indice_var -= 1
                        instanciation_courante = instanciation_courante[:indice_var]
                else:
                    if version == "A2":
                        csp.forward_checking(instanciation_courante, self.taille_mot, all_lettres_restantes, self.tentatives, dictionnaire)

            else:  # sinon backtracking
                if version == "A1":
                    all_lettres_restantes[indice_var] = copy.copy(self.domaines[indice_var])                    
                elif version == "A2":
                    for i in range(indice_var, self.taille_mot):
                        all_lettres_restantes[i] = copy.copy(self.domaines[i])
                indice_var -= 1
                instanciation_courante = instanciation_courante[:indice_var]

        return self.nb_tentatives

    def resolution_par_CSP_opt(self, premier_mot=None, verbose=False):
        """
        Fonction qui fait la résolution de Wordle Mind en CSP de manière optimisée.

        :param premier_mot: premier mot à tester
        :param verbose: si on veut l'affichage des tentatives

        :type premier_mot: list[str]
        :type verbose: bool

        :return: nombre de tentatives faites
        :rtype: int
        """

        fin = False  # flag pour savoir quand le jeu se termine
        liste_mots = self.dictionnaire[self.taille_mot]  # sélection des mots correspondant à la taille du mot secret

        # choix du premier (s'il n'y pas de premier mot donné)
        if premier_mot is None:
            # aléatoire
            proposition = random.choice(liste_mots)
        else:
            # celui donné en paramètre
            proposition = premier_mot

        # tant qu'on a pas fini (trouvé le mot secret)
        while not fin:
            fin, feedback = self.test_tentative(proposition, verbose)
            liste_mots = csp.filtrer_propositions(liste_mots, proposition, feedback)
            proposition = csp.donner_proposition(liste_mots, feedback)

        return self.nb_tentatives

    def resolution_par_algo_genetique(self, maxsize, maxgen, verbose=False):
        """
        Fonction qui fait la résolution de Wordle Mind avec un algorithme génétique.

        :param maxsize: taille max de l'ensemble E
        :param maxgen: nombre de génération
        :param verbose: si on veut l'affichage des tentatives

        :type maxsize: int
        :type maxgen: int
        :type verbose: bool

        :return: nombre de tentatives faites
        :rtype: int
        """

        # choix aléatoire d'un mot parmi ceux qui ont la même taille que le mot secret
        mot_choisi = random.choice(self.dictionnaire[self.taille_mot])
        # teste du mot choisi
        fin, feedback = self.test_tentative(mot_choisi, verbose)

        # tant qu'on a pas fini (trouvé le mot secret)
        while not fin:
            # génération de l'ensemble des mots compatibles avec les tentatives précédentes
            ens = ag.engendrer_ens(mot_choisi, self.dictionnaire, self.tentatives, maxsize, maxgen)

            if ens:
                # choix aléatoire du mot parmi cette ensemble
                mot_choisi = random.choice(ens)
                # teste du mot choisi
                fin, feedback = self.test_tentative(mot_choisi, verbose)
            else:
                fin = True
                self.nb_tentatives = -1

        return self.nb_tentatives

    def test_tentative(self, mot, verbose=False):
        """
        Fonction qui teste si le mot donné est le mot secret et renvoie son feedback.

        :param mot: mot courant
        :param verbose: si on veut l'affichage des tentatives

        :type mot: list[str]
        :type verbose: bool

        :return: True ou False, feedback
        :rtype: (bool, Feedback)
        """

        self.nb_tentatives += 1

        if verbose:
            print("Tentative {}:\t{}".format(self.nb_tentatives, mot))

        if mot == self.mot_secret:
            return True, utils.Feedback(len(mot), 0)

        feedback = utils.recuperer_feedback(self.mot_secret, mot)
        self.tentatives.append((mot, feedback))
        utils.reduire_domaines(mot, feedback, self.domaines)

        return False, feedback
