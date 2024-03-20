import serial
import time
from PinsToPath import *
import matplotlib
import matplotlib.pyplot as plt


DEG_TO_PULSE = 11.377777777778

class Envoyer:

    def __init__(self):

        matplotlib.use("TkAgg")

        self.ActualPos = dict()
        self.ActualPos['left'] = []
        self.ActualPos['right'] = []
        self.ActualPos['table'] = []

        self.Pos = dict()
        self.Pos['left'] = []
        self.Pos['right'] = []
        self.Pos['table'] = []

        # TODO CHECK TON CRISSE DE PORT
        self.arduino = serial.Serial('COM4', 115200, timeout=1)
        time.sleep(2)  # Temps pour que la connection se fasse

    def envoie_commande(self,commande):
        print(f"Python: {commande}")
        self.arduino.write(commande.encode())
        while True:
            if self.arduino.in_waiting > 0:
                reponse = self.arduino.readline().decode().strip()
                print(f"Arduino : {reponse}")
                if reponse == '1':  # Attend le signal du arduino
                    break  # Sort de la loop pour envoyer une autre commande


    def readPos(self):
        self.arduino.write('{T1}'.encode())
        while True:
            if self.arduino.in_waiting > 0:
                response = self.arduino.readline().decode().strip()
                self.ActualPos['left'].append(int(response))
                print(f"position gauche : {response}")
                response = self.arduino.readline().decode().strip()
                self.ActualPos['right'].append(int(response))
                print(f"position droite : {response}")
                response = self.arduino.readline().decode().strip()
                self.ActualPos['table'].append(int(response))
                print(f"position table : {response}\n")
                break


    def manual_calibration_dxl(self):
        self.arduino.write('{T0}'.encode())
        while True:
            if self.arduino.in_waiting > 0:
                reponse = self.arduino.readline().decode().strip()
                if reponse == '1':
                    print("torque has been disabled, you are free to move the arms ")
                    while True:
                        input("press enter to read current position : \n")
                        self.readPos()

    def start_run(self,filepath,numPins):
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
            (2660, 2769),
            (2732, 2855),
            (2760, 2816),
            (2710, 2759),
            (2560, 2560),
        ]

        path = Path(csvfilepath=filepath, numPins=numPins)
        commandes = []

        for pin in path.pinsInPulse[0]:
            commandes.append("{C2 %d}" % pin)
            self.Pos["table"].append(pin)
            self.Pos["left"].append(seq0[4][0])
            self.Pos["right"].append(seq0[4][1])
            for s in seq0:
                commandes.append(f"{{C1 {s[0]} {s[1]}}}")
                self.Pos["left"].append(s[0])
                self.Pos["right"].append(s[1])
                self.Pos["table"].append(pin)

        x = np.arange(len(commandes))
        eg = np.zeros(len(commandes))
        ed = np.zeros(len(commandes))
        et = np.zeros(len(commandes))

        plt.ion()
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.set_ylim((0, 10))
        line1, = ax.plot(x, eg, 'b-')
        line2, = ax.plot(x, ed, 'r-')
        line3, = ax.plot(x, et, 'g-')

        for i, cmd in enumerate(commandes):

            self.envoie_commande(cmd)
            self.readPos()

            et[i] = (np.abs(self.Pos['table'][i] - self.ActualPos['table'][i]))
            line3.set_ydata(et)

            eg[i] = (np.abs(self.Pos['left'][i] - self.ActualPos['left'][i]))
            ed[i] = (np.abs(self.Pos['right'][i] - self.ActualPos['right'][i]))
            line1.set_ydata(eg)
            line2.set_ydata(ed)

            ax.set_xlim(0, i+1)
            fig.canvas.draw()
            plt.draw()
            fig.canvas.flush_events()

            # time.sleep(0.005)  # Pour laisser le temps au arduino de calculer

        # arduino.close()  # Si toute les commandes sont complété

        # manual_calibration_dxl()
