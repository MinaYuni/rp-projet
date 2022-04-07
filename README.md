# Projet RP

Sorbonne Université - M1 ANDROIDE <br/>
MU4IN201 - RP (Résolution de Problèmes) <br/>

## Satisfaction de contraintes pour le Wordle Mind

### Introduction et objectifs

L'objet de ce projet est de développer et tester des méthodes de satisfaction de contraintes et un algorithme génétique 
pour la résolution d'un problème de Wordle Mind. Nous considérons une version de ce jeu dans laquelle on doit découvrir 
un mot caché du dictionnaire ("appelé mot secret") qui se compose de n lettres. Le jeu consiste pour le joueur à deviner 
le mot. Pour obtenir de l'information le joueur peut proposer un mot du dictionnaire (voir fichier dico.txt) et 
le programme lui indique combien de caractères du mot proposé sont corrects et bien placés et d'autre part combien de 
caractères sont corrects, mais mal placés (par exemple si le décodeur propose le mot "tarte" alors que le mot secret 
est "dette" on aura 2 bien placés et 1 mal placé (attention, contrairement à la version originale de "Wordle" la réponse 
n'indique pas quelle lettre est bien placée et quelle lettre est mal placée). Le joueur peut alors tenter un nouvel 
essai et ainsi de suite jusqu'à ce qu'il tombe sur le mot secret qui engendrera n bien placés et la partie s'arrête. 
Le but est bien sûr de chercher à découvrir le mot secret en utilisant le moins d'essais possibles. Dans ce projet, 
on s'intéresse à réaliser un programme qui, à chaque étape du jeu, est capable de proposer un nouveau mot à essayer qui 
soit compatible avec toutes les informations accumulées lors des essais précédents (on s'interdit de tester des 
combinaisons incompatibles avec l'information disponible, même si elles sont informatives).

### Partie 1 : modélisation et résolution par CSP

Dans cette partie, on décide de modéliser le problème de la recherche d'un mot compatible
avec l'information disponible par un CSP a n variables X1, ..., Xn de domaine D = {a, ..., z}.
Pour engendrer un mot compatible avec l'information disponible à l'itération courante on envisage deux algorithmes :
- A1 : retour arrière chronologique
- A2 : retour arrière chronologique avec arc cohérence (forward checking ou plus si nécessaire).

### Partie 2 : modélisation et résolution par algorithme génétique

Dans cette partie, on décide d'aborder le problème de la recherche d'un mot compatible a
l'aide d'un algorithme génétique. Le but de cet algorithme serait, après chaque nouvel essai,
d'engendrer un ensemble E de mots compatibles avec l'ensemble des essais précédents. 
L'ensemble E de mots compatibles présentera une taille maximale maxsize et l'algorithme génétique s’arrêtera dès que 
la taille maximale est atteinte. Afin de limiter les temps de calcul, l'algorithme génétique pourra également s’arrêter 
après un nombre maximal de générations maxgen (l'algorithme génétique pourra donc s’arrêter même si la taille de E 
est inférieure à maxsize). Notez qu'il se peut que l'algorithme ne retourne aucun mot compatible après avoir atteint 
le nombre maximal de générations. Dans ce cas, vous pouvez continuer la recherche d'un mot compatible jusqu’à ce qu'un 
timeout soit atteint (de 5 minutes par exemple). Si a la n de ce timeout aucun mot compatible n'a été engendré, 
on peut considérer que la méthode a échoué. La population évolue grâce aux opérateurs de croisements et de mutations. 
Différents opérateurs de mutations sont possibles (changement aléatoire d'un caractère, échange entre deux caractères, 
inversion de la séquence de caractères entre deux positions aléatoires, ...) et chacun pourra être choisi avec 
une certaine probabilité. Notez que ces opérations peuvent engendrer des mots interdits, car ils ne figurent pas dans 
le dictionnaire ; dans ce cas on choisira le mot le plus proche dans le dictionnaire (au sens d'une distance de 
votre choix, par exemple ordre alphabétique ou distance d’édition). La probabilité d'un mot d’être sélectionné comme 
parent sera proportionnelle à sa valeur adaptative ("fitness"). La valeur adaptative d'un mot devra être liée 
aux nombres d’incompatibilités avec les essais précédents. Dès qu'un mot compatible est trouvé, 
il sera ajouté à l'ensemble E.

### Partie 3 : détermination de la meilleure tentative (question bonus, optionnelle)

Il peut être intéressant d'évaluer a priori la valeur informative d'une tentative (essai d'un mot) pour réduire 
efficacement l'espace des solutions admissibles. Proposer une ou plusieur méthodes pour évaluer a priori l'utilité 
d'une tentative donnée, à la suite de celles déjà effectuées. Une telle évaluation peut être utilisée pour choisir 
la meilleure tentative dans une population de solutions compatibles engendrée par l'algorithme génétique. 
On peut aussi modifier l'algorithme de la partie 1 pour engendrer plusieurs solutions compatibles avec l'information 
disponible et choisir parmi elles la meilleure. Dans les deux cas, on cherchera à évaluer à quel point la sélection 
de la meilleure tentative peut accélérer la résolution du problème.
