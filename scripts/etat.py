C1 = False  # vrai si C2 est false
C2 = False  # code carte RFID autorisé par l'avion
C3 = False  # touche # appuyée
C4 = False  # C3 et C5 sont false
C5 = False  # interrupteur PWR position "ON"
C6 = False  # C7 est false
C7 = False  # interrupteur PWR position "OFF"

# en attente
def E1():
    print("E1: En attente\n")
    # impossible de contrôler les moteurs (DC et servo)
    # clavier désactivé
    # interrupteur désactivé
    # LCD affiche "Scannez la carte"
    # attendre qu'une carte soit passée au lecteur RFID

# pré-vol
def E2():
    print("E2: Pré-vol\n")
    # entrer code de destination
    # LCD affiche que l'on peut démarrer
    # interrupteur activé

# prêt à voler
def E3():
    print("E3: Prêt à voler\n")
    # activer moteur dc et servo
    # LCD affiche à chaque 100ms: moteur (%), angle servo, destination

def loop():
  currentstate = "E1"
  while (True):

    if currentstate == "E1":
      E1()
      # Validation des conditions pour la mise à jour de l'état
      if C2 is True:
        currentstate = "E2"

    elif currentstate == "E2":
      E2()
      # Validation des conditions pour la mise à jour de l'état
      if C3 is True:
        currentstate = "E1"
      elif C4 is True:
        currentstate = "E3"

    elif currentstate == "E3":
      E3()
      # Validation des conditions pour la mise à jour de l'état
      if C7 is True:
        currentstate = "E1"