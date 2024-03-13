import serial
import time
from PinsToPath import *

DEG_TO_PULSE = 11.377777777778

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


def manual_calibration_dxl():
    arduino.write('{T0}'.encode())
    while True:
        if arduino.in_waiting > 0:
            reponse = arduino.readline().decode().strip()
            if reponse == '1':
                print("torque has been disabled, you are free to move the arms ")
                while True:
                    input("press enter to read current position : \n")
                    arduino.write('{T1}'.encode())
                    while True:
                        if arduino.in_waiting > 0:
                            response = arduino.readline().decode().strip()
                            print(f"position gauche : {response}")
                            response = arduino.readline().decode().strip()
                            print(f"position droite : {response}")
                            response = arduino.readline().decode().strip()
                            print(f"position table : {response}\n")
                            break


# # Sequence clou 30 à gauche
#     "{C3 71 178 0}",
#     "{C3 80 177 0}",
#     "{C3 82 179 0}",
#     "{C3 71 180 0}",
#
# # Sequence clou 20 à droite
#     "{C3 8 257 0}",
#     "{C3 8 261 0}",
#     "{C3 7 270 0}",
#     "{C3 4 265 0}",
#     "{C3 8 257 0}",
#
# Sequence clou 0

seq0 = [
    "{C1 2660 2769}",
    "{C1 2732 2855}",
    "{C1 2760 2816}",
    "{C1 2710 2759}",
    "{C1 2560 2560}",
]

path = Path("StringUS/[1] - ImageProcessing/outputs/ThreadedCSVFile.csv", 250)
commandes = []
for pin in path.pinsInPulse[0]:
    commandes.append("{C2 %d}" % pin)
    for s in seq0:
        commandes.append(s)

for cmd in commandes:
    envoie_commande(cmd)
    time.sleep(0.01)  # Pour laisser le temps au arduino de calculer

# arduino.close()  # Si toute les commandes sont complété

# manual_calibration_dxl()
