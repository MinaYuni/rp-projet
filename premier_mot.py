import sys
import time

import utils
import CSP as csp


def liste_mot_en_str(mot_list):
    mot_str = ""
    for lettre in mot_list:
        mot_str += lettre
    return mot_str


if __name__ == "__main__":
    file_path = "./dico.txt"
    dictionnaire = utils.lire_dictionnaire(file_path)

    liste_tailles = list(dictionnaire.keys())
    liste_tailles.sort()

    # nb_mots_par_taille = dict()
    # for taille in liste_tailles:
    #     nb_mots_par_taille.update({taille: len(dictionnaire[taille])})

    taille_min = 5  # min(liste_tailles)
    taille_max = max(liste_tailles)

    nb_mots_restants_par_taille = dict()

    print("\n----- DEBUT -----\n")

    debut_tps_calcul = time.perf_counter()
    for taille in range(taille_min, taille_max + 1):
        out_file_path = "./out/out_" + str(taille) + ".csv"
        moy_min = float("infinity")
        mot_opt = ""
        liste_mots = dictionnaire[taille]
        nb_mot_taille = len(liste_mots)
        with open(out_file_path, "w") as out_file:
            # we write the list of words in the file
            out_file.write("mot_test|mot_secret,")
            for mot in liste_mots:
                mot = liste_mot_en_str(mot)
                out_file.write(mot + ",")
            out_file.write("\n")
            debut_tps_taille = time.perf_counter()
            for i, mot_test in enumerate(liste_mots):
                mot_test_str = liste_mot_en_str(mot_test)
                nb_mots_restants = 0
                out_file.write(mot_test_str + ",")
                # if i == 0:
                #     print("=")
                # elif i % 100 == 0:
                #     print("-")
                # elif i % 10 == 0:
                #     print("_")

                for j, mot_secret in enumerate(liste_mots):
                    # if j == 0:
                    #     print("*", end='')
                    # elif j % 1000 == 0:
                    #     print(",")
                    # elif j % 100 == 0:
                    #     print(".", end='')

                    feedback = utils.recuperer_feedback(mot_secret, mot_test)
                    mots_restants = csp.filtrer_propositions(liste_mots, mot_test, feedback)
                    out_file.write(str(len(mots_restants)) + ",")
                    nb_mots_restants += len(mots_restants)

                moy_mots_restants = nb_mots_restants / nb_mot_taille
                out_file.write(str(moy_mots_restants) + "\n")
                nb_mots_restants_par_taille.update({taille: {mot_test_str: moy_mots_restants}})

                if moy_mots_restants < moy_min:
                    moy_min = moy_mots_restants
                    mot_opt = mot_test_str
                # we clear the previous  console line and then print the current one/
                print(f"\r{i + 1}/{nb_mot_taille}")

        fin_tps_taille = time.perf_counter()
        tps_taille = fin_tps_taille - debut_tps_taille

        print(
            "taille {} ({:.5f} s):\t{}\t{:.2f}/{}".format(taille, tps_taille, mot_opt.upper(), moy_min, nb_mot_taille))

    fin_tps_calcul = time.perf_counter()
    tps_calcul = fin_tps_calcul - debut_tps_calcul

    print("\n----- FIN ----- {:.5f} s\n".format(tps_calcul))
