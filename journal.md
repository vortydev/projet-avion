# Journal du projet avion - Étienne Ménard

Ceci est mon journal personnel pour le projet pratique du cours **Introduction à l'utilisation d'objets connectés** du programme de Techniques de l'informatique au Cégep de Sherbrooke.

&nbsp;

## Scripts

Les scripts du projet sont listés dessous.

### A

- [Adafruit_LCD1602.py](./scripts/Adafruit_LCD1602.py) : Classe de l'écran LCD.
- [avion.py](./scripts/avion.py) : Programme principal du projet.

### E
- [etat.py](./scripts/etat.py) : Squelette des états de l'avion.

### J
- [joystick.py](./scripts/joystick.py) : Script de test pour le joystick.

### K
- [Keypad.py](./scripts/Keypad.py) : Classe du keypad matrix.

## L
- [lcd.py](./scripts/lcd.py) : Script de test pour l'écran LCD.

### M
- [MFRC522.py](./scripts/MFRC522.py) : Classe interfaçant le module NFC MF522-AN du lecteur RFID.
- [moteur.py](./scripts/moteur.py) : Script de test pour le moteur DC.
- [moteurjoystick.py](./scripts/moteurjoystick.py) : Script de test pour le moteur DC et le joystick.

### P
- [PCF8574.py](./scripts/PCF8574.py) : Classe interfaçant le module PCF8574 de l'écran LCD.

### R
- [rfid.py](./scripts/rfid.py) : Script de test pour le lecteur RFID.

### S
- [servo.py](./scripts/servo.py) : Script de test pour le servomoteur.
- [servomoteurjoystick.py](./scripts/servomoteurjoystick.py) : Script de test pour le servomoteur, le moteur DC et le joystick.
- [switch.py](./scripts/switch.py) : Script de test pour l'interrupteur *slide switch*.

&nbsp;

## Spécifications électriques

### Tableau de connexions pour le *header* du *Raspberry Pi*
| # *pin* | Nom E/S | Connecté à |
|-|-|-|
| 2 | SDA 1 | ADC et LCD |
| 3 | SCL 1 | ADC et LCD |
| 4 | GPIO 4 | Keypad matrix |
| 5 | GPIO 5 | Bouton *joystick* (SW) |
| 6 | GPIO 6 | Interrupteur *slide switch* (SW) |
| 8 | CE0 | Keypad matrix |
| 9 | MISO | Keypad matrix |
| 10 | MOSI | Keypad matrix |
| 11 | SCLK | Keypad matrix |
| 12 | GPIO 12 | Servomoteur |
| 13 | GPIO 13 | Contrôle moteur (L293D) |
| 16 | GPIO 16 | DEL rouge |
| 17 | GPIO 17 | Keypad matrix |
| 18 | GPIO 18 | Keypad matrix |
| 19 | GPIO 19 | Contrôle moteur (L293D) |
| 20 | GPIO 20 | DEL jaune |
| 21 | GPIO 21 | DEL verte |
| 22 | GPIO 22 | Keypad matrix |
| 23 | GPIO 23 | Keypad matrix |
| 24 | GPIO 24 | Keypad matrix |
| 25 | GPIO 25 | Lecteur RFID |
| 26 | GPIO 26 | Contrôle moteur (L293D) |
| 27 | GPIO 27 | Keypad matrix |

&nbsp;

## Vendredi 25/02/2022

### Sessions SSH

Cette semaine j'ai seulement configuré mon Raspberry Pi afin d'ouvrir des sessions SSH à partir de mon ordinateur portable dans Visual Studio Code, en suivant les instructions jointes de la semaine 6.

Article suivi: [lien](https://anthonyfourie.com/2021/08/16/vs-code-setting-remote-development-on-raspberry-pi/)

&nbsp;

## Vendredi 11/03/2022

### Moteur DC

J'ai suivi le tutoriel Freenove au Chapitre 13 afin de créer un montage avec le moteur DC et un potentiomètre. Il est préférable d'utiliser l'alimentation offerte par le Power Breakout Board (la petite board noire dans laquelle on peut brancher une pile 9V comme source d'alimentation), plutôt que d'utiliser le GPIO Extension Board.

Le script [moteur.py](./scripts/moteur.py) permet au moteur de tourner en sens horaire et anti-horaire dépendamment de la position du potentiomètre.

> Il est pertinent de débrancher le moteur lorsqu'on le teste pas, car il tire beaucoup d'énergie de la pile et peut faire planter le programme.

### Joystick

 J'ai ensuite poursuivi en remplaçant le potentiomètre du montage précédent par le joystick, en me basant sur les diagrammes du tutoriel Freenove au Chapitre 12. Assez facile.

Le script [joystick.py](./scripts/joystick.py) affiche les valeurs des axes X (horizontal) et Y (vertical), et si le bouton (Z) a été cliqué.

> La position "neutre" du joystick n'est pas parfaitement centrée, ça sera peut-être à tweaker plus tard dans le projet.

### Moteur DC + Joystick

La suite logique était ensuite de remplacer le potentiomètre dans le script du moteur par le joystick. Simple et facile, les axes X et Z sont écoutés même si le moteur DC n'utilise que les valeurs de l'axe Y.

Le script [moteurjoystick.py](./scripts/moteurjoystick.py) permet de faire tourner le moteur en sens horaire et anti-horaire selon la position du joystick sur l'axe Y (vertical). Les axes X, Y et Z du joystick sont également affichés.

> Julien recommande d'aplatir les câbles du montage afin de limiter la quantité de bruit électrique produit par le circuit, qui cause de l'interférence.

&nbsp;

## Vendredi 18/03/2022

### Servomoteur

J'ai commencé le cours en suivant le tutoriel Freenove au chapitre 15 afin d'obtenir un montage et le script [servo.py](./scripts/servo.py) qui fait tourner mon servomoteur de 0 à 180 degrés allez-retour.

J'ai ensuite inséré les segments de codes du servomoteur dans le script [servomoteurjoystick.py](./scripts/servomoteurjoystick.py) et l'ai adapté pour contrôler le servomoteur et le moteur DC en même temps avec le joystick.

### Joystick

J'ai ensuite poursuivi en implémentant dans le script [servomoteurjoystick.py](./scripts/servomoteurjoystick.py) la fonctionnlité de vérouiller les contrôles du moteur DC et du servomoteur lorsque qu'on appuie sur le bouton (axe Z) du joystick. Rappuyer sur le bouton dévérouille les contrôles. Rinse, repeat.

### Codage

J'ai commencé à préparer pour la *"greater picture"* en créant les fichiers:
- [avion.py](./scripts/avion.py) : Contrôleur principal du programme de l'avion.
- [etat.py](./scripts/etat.py) : Script responsable de la gestion des états et des conditions.

> On peut accéder aux fonctions définies dans un script en l'important comme un module.
> ```python
> # importations
> import RPi.GPIO as GPIO
> from date import sleep
> import etat.py
> ```

&nbsp;

## Samedi 19/03/2022

### Joystick

J'ai *tweaké* les contrôles du joystick dans [servomoteurjoystick.py](./scripts/servomoteurjoystick.py) pour que les contrôles ne puissent être (dé)vérouillés qu'une fois par seconde, vu que le bouton du joystick est très sensible.

&nbsp;

## Dimanche 20/03/2022

### Écran LCD

J'ai ajouté à mon montage l'écran LCD. Le script [lcd.py](./scripts/lcd.py) affiche le temps et la température du CPU.

J'ai ensuite intégré l'écran LCD au montage déjà existant dans le script [avion.py](./scripts/avion.py), en y affichant les valeurs pour le moteur DC et le servomoteur, ainsi que le code de la destination qui sera implémenté plus tard.

&nbsp;

## Vendredi 25/03/2022

Aujourd'hui j'ai commencé en refaisant les connections électriques sur le breadboard, afin de limiter le bruit électrique et faciliter la manipulation du montage.

*J'ai mal aux doigts.*

J'ai également mis à jour les connections des pins dans [avion.py](./scripts/avion.py) et simplifié la fonction du servomoteur.

&nbsp;

## Vendredi 01/04/2022

J'ai débuté le cours en commençant un tableau des spécifications électriques et des connections des composants du projet.

J'ai ensuite débuté d'implémenter les états de [etat.py](./scripts/etat.py) dans le fichier [avion.py](./scripts/avion.py), et j'ai déplacé le code du contrôle du moteur DC et du servomoteur dans la fonction E3.

&nbsp;

## Samedi 02/04/2022

### Interrupteur

J'ai ajouté l'interrupteur au montage et codé la détection et le changement de la condition C5 dans le script [avion.py](./scripts/avion.py).

&nbsp;

## Dimanche 03/04/2022

### Interrupteur

L'interrupteur prenait initialement son alimentation de la même ligne que le contrôleur du moteur DC, ce qui empêchait le circuit de se fermer et de fonctionner correctement. 

J'ai donc créé un script séparé, [switch.py](./scripts/switch.py), afin de tenter de déboguer mon étrange problème, sans succès.

J'ai ensuite pensé que peut-être la pile 9V qui alimentait le montage était vide, vu que je l'avais laissée branchée au Power Breakout Board toute une nuit. Je suis donc allé acheter de nouvelles piles 9V (c'est de la grosse arnaque, une seule pile coûte 10$???), et comme remplacer la pile n'a rien changé à mon problème, j'ai repositionné l'interrupteur à une autre place sur le bread board et tout fonctionnait à nouveau!

&nbsp;

## Mardi 05/04/2022

### RFID

J'ai lu la théorie et la documentation de Freenove concernant le module de RFID.

> Le code python en exemple est malheureusement en Python 2, je devrai donc chercher et trouver le fichier Python 3 caché dans le répertoire des modules Freenove.

&nbsp;

## Mercredi 06/04/2022

### Documentation

J'ai mis à jour le tableau des connections électriques du Raspberry Pi et mon journal du projet avec l'avancement des derniers jours.

Mon répertoire local sur mon Raspberry Pi s'était corrompu, j'ai donc fait des gymanstique avec Git afin de mettre mon projet à jour sans trop de pépins.

J'ai ajouté de brèves descriptions aux [scripts](#scripts).

### RFID

J'ai importé les fichiers nécessaires au fonctionnement du lecteur RFID, que j'ai testé dans le script [rfid.py](./scripts/rfid.py).

Après de nombreuses heures de recherches, de taponnage et de frustration, j'ai finalement réussi à faire fonctionner le lecteur RFID au sein du script [avion.py](./scripts/avion.py). Il a fallu que je *rollback* la librairie SPI-Py à une version antécédante, merci à [derweili](https://stackoverflow.com/questions/54847012/raspberry-pi-3b-and-rfid-rc522-python-typeerror) d'avoir publié ta réponse!

J'ai poursuivi en ajoutant la matrice de boutons au montage et dans mon script.

&nbsp;

## Jeudi 07/04/2022

### Sprint final

Le montage est complété et le code à été écrit. Je pense que le projet est prêt pour la remise.
