import serial
import time
from PinsToPath import *
# TODO CHECK TON CRISSE DE PORT 
arduino = serial.Serial('COM7', 115200, timeout=1)
time.sleep(2)  # Temps pour que la connection se fasse


def envoie_commande(commande):
    print(f"Python: {commande}")
    arduino.write(commande.encode())
    while True:
        if arduino.in_waiting > 0:
            reponse = arduino.readline().decode().strip()
            print(f"Arduino : {reponse}")
            if reponse == '1':  # Attend le signal du arduino
                break  # Sort de la loop pour envoyer une autre commande


commandes = [
    "{C2 90}",
    "{C2 180}",
    "{C2 90}",
    "{C2 270}",
    "{C2 0}"
]

path = Path("StringUS/[1] - ImageProcessing/outputs/shronk.csv", 300)

# commandes = []
# for pin in path.pinsInDeg[1]:
#     commandes.append("C2 %f" % pin)

for cmd in commandes:
    envoie_commande(cmd)
    time.sleep(0.01)  # Pour laisser le temps au arduino de calculer

# arduino.close()  # Si toute les commandes sont complété
