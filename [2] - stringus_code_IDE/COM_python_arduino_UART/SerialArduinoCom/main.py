import serial
import time
from PinsToPath import *
import matplotlib
import matplotlib.pyplot as plt

matplotlib.use("TkAgg")

DEG_TO_PULSE = 11.377777777778

ActualPos = dict()
ActualPos['left'] = []
ActualPos['right'] = []
ActualPos['table'] = []

Pos = dict()
Pos['left'] = []
Pos['right'] = []
Pos['table'] = []

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


def readPos():
    arduino.write('{T1}'.encode())
    while True:
        if arduino.in_waiting > 0:
            response = arduino.readline().decode().strip()
            ActualPos['left'].append(int(response))
            print(f"position gauche : {response}")
            response = arduino.readline().decode().strip()
            ActualPos['right'].append(int(response))
            print(f"position droite : {response}")
            response = arduino.readline().decode().strip()
            ActualPos['table'].append(int(response))
            print(f"position table : {response}\n")
            break

def readSeq():
    arduino.write('{T2}'.encode())
    i = 0
    while True:
        if arduino.in_waiting > 0:
            response_gauche = arduino.readline().decode().strip()
            response_droite = arduino.readline().decode().strip()
            i += 1
            print(f"{{{response_gauche}, {response_droite}}},")
            if i == 100:
                break

def manual_measure_dxl():
    arduino.write('{T0}'.encode())
    while True:
        if arduino.in_waiting > 0:
            reponse = arduino.readline().decode().strip()
            if reponse == '1':
                print("torque has been disabled, you are free to move the arms ")
                while True:
                    input("press enter to read current position : \n")
                    readPos()

def calibrate_contour_seq():
    arduino.write('{T0}'.encode())
    while True:
        if arduino.in_waiting > 0:
            reponse = arduino.readline().decode().strip()
            if reponse == '1':
                print("torque has been disabled, you are free to move the arms ")
                readSeq()


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

# path = Path("StringUS/[1] - ImageProcessing/outputs/ThreadedCSVFile.csv", 125)
# commandes = ["{C2 0}",
#              "{C2 2048}",
#              "{C2 3072}",
#              "{C5 0}"]
#
# for pin in path.pinsInPulse[0]:
#     commandes.append("{C2 %d}" % pin)
#     Pos["table"].append(pin)
#     Pos["left"].append(seq0[4][0])
#     Pos["right"].append(seq0[4][1])
#     for s in seq0:
#         commandes.append(f"{{C1 {s[0]} {s[1]}}}")
#         Pos["left"].append(s[0])
#         Pos["right"].append(s[1])
#         Pos["table"].append(pin)
#
# x = np.arange(len(commandes))
# eg = np.zeros(len(commandes))
# ed = np.zeros(len(commandes))
# et = np.zeros(len(commandes))
#
# plt.ion()
# fig = plt.figure()
# ax = fig.add_subplot(111)
# ax.set_ylim((0, 10))
# line1, = ax.plot(x, eg, 'b-')
# line2, = ax.plot(x, ed, 'r-')
# line3, = ax.plot(x, et, 'g-')
#
#
# for i, cmd in enumerate(commandes):
#
#
     # envoie_commande(cmd)
#     readPos()
#
#     et[i] = (np.abs(Pos['table'][i] - ActualPos['table'][i]))
#     line3.set_ydata(et)
#
#     eg[i] = (np.abs(Pos['left'][i] - ActualPos['left'][i]))
#     ed[i] = (np.abs(Pos['right'][i] - ActualPos['right'][i]))
#     line1.set_ydata(eg)
#     line2.set_ydata(ed)
#
#     ax.set_xlim(0, i+1)
#     fig.canvas.draw()
#     plt.draw()
#     fig.canvas.flush_events()

    # time.sleep(0.005)  # Pour laisser le temps au arduino de calculer

# arduino.close()  # Si toute les commandes sont complété

# calibrate_contour_seq()
envoie_commande("{C4}")