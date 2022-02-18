# Journal du projet avion - Étienne Ménard

Ceci est mon journal personnel pour le projet pratique du cours **Introduction à l'utilisation d'objets connectés** du programme de Techniques de l'informatique au Cégep de Sherbrooke.

&nbsp;

# Vendredi 25/02/2022

## Sessions SSH

Cette semaine j'ai seulement configuré mon Raspberry Pi afin d'ouvrir des sessions SSH à partir de mon ordinateur portable dans Visual Studio Code, en suivant les instructions jointes de la semaine 6.

Article suivi: [lien](https://anthonyfourie.com/2021/08/16/vs-code-setting-remote-development-on-raspberry-pi/)

&nbsp;

# Vendredi 11/03/2022

## Moteur DC

J'ai suivi le tutoriel Freenove au Chapitre 13 afin de créer un montage avec le moteur DC et un potentiomètre. Il est préférable d'utiliser l'alimentation offerte par le Power Breakout Board (la petite board noire dans laquelle on peut brancher une pile 9V comme source d'alimentation), plutôt que d'utiliser le GPIO Extension Board.

Le script `moteur.py` permet au moteur de tourner en sens horaire et anti-horaire dépendamment de la position du potentiomètre.

> Il est pertinent de débrancher le moteur lorsqu'on le teste pas, car il tire beaucoup d'énergie de la pile et peut faire planter le programme.

## Joystick

 J'ai ensuite poursuivi en remplaçant le potentiomètre du montage précédent par le joystick, en me basant sur les diagrammes du tutoriel Freenove au Chapitre 12. Assez facile.

Le script `joystick.py` affiche les valeurs des axes X (horizontal) et Y (vertical), et si le bouton (Z) a été cliqué.

> La position "neutre" du joystick n'est pas parfaitement centrée, ça sera peut-être à tweaker plus tard dans le projet.

## Moteur DC + Joystick

La suite logique était ensuite de remplacer le potentiomètre dans le script du moteur par le joystick. Simple et facile, les axes X et Z sont écoutés même si le moteur DC n'utilise que les valeurs de l'axe Y.

Le script `moteurjoystick.py` permet de faire tourner le moteur en sens horaire et anti-horaire selon la position du joystick sur l'axe Y (vertical). Les axes X, Y et Z du joystick sont également affichés.

> Julien recommande d'aplatir les câbles du montage afin de limiter la quantité de bruit électrique produit par le circuit, qui cause de l'interférence.

&nbsp;

# Vendredi 18/03/2022

## Servomoteur

J'ai commencé le cours en suivant le tutoriel Freenove au chapitre 15 afin d'obtenir un montage et le script `servo.py` qui fait tourner mon servomoteur de 0 à 180 degrés allez-retour.

J'ai ensuite inséré les segments de codes du servomoteur dans le script `servomoteurjoystick.py` et l'ai adapté pour contrôler le servomoteur et le moteur DC en même temps avec le joystick.