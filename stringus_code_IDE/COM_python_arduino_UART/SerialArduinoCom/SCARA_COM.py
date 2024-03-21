import pandas as pd
import serial
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


class SCARA_COM:

    def __init__(self, COM):

        # TODO CHECK TON CRISSE DE PORT
        arduino = serial.Serial('COM%i'%COM, 115200, timeout=1)
        time.sleep(2)  # Temps pour que la connection se fasse
        matplotlib.use("TkAgg")

        self.ActualPos = dict()
        self.ActualPos['left'] = []
        self.ActualPos['right'] = []
        self.ActualPos['table'] = []

        self.Pos = dict()
        self.Pos['left'] = []
        self.Pos['right'] = []
        self.Pos['table'] = []
        self.seq0 = [0]

        # TODO CHECK TON CRISSE DE PORT
        self.arduino = serial.Serial('COM%i' % COM, 115200, timeout=1)
        time.sleep(2)  # Temps pour que la connection se fasse

    def envoie_commande(self, commande):
        print(f"Python: {commande}")
        self.arduino.write(commande.encode())
        while True:
            if self.arduino.in_waiting > 0:
                reponse = self.arduino.readline().decode().strip()
                print(f"Arduino : {reponse}")
                if reponse == '1':  # Attend le signal du arduino
                    break  # Sort de la loop pour envoyer une autre commande

    def readThreadedCSV(self, csvfilepath, numPins):
        self.csvfile = pd.read_csv(csvfilepath)
        self.numPins = numPins
        self.angles = np.linspace(0, 4096, numPins + 1, dtype=int)

        self.pins = np.array((self.csvfile.p1, self.csvfile.p2))
        self.pinsInPulse = np.zeros_like(self.pins).astype(np.float32)

        for i in range(np.shape(self.pins)[1]):
            self.pinsInPulse[0][i] = self.angles[self.pins[0][i]]
            self.pinsInPulse[1][i] = self.angles[self.pins[1][i]]

    def getNumLinesCSV(self):
        return len(self.csvfile)

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

    def readSeq(self):
        self.arduino.write('{T2}'.encode())
        i = 0
        while True:
            if self.arduino.in_waiting > 0:
                response_gauche = self.arduino.readline().decode().strip()
                response_droite = self.arduino.readline().decode().strip()
                i += 1
                print(f"{{{response_gauche}, {response_droite}}},")
                if i == 100:
                    break

    def manual_measure_dxl(self):
        self.arduino.write('{T0}'.encode())
        while True:
            if self.arduino.in_waiting > 0:
                reponse = self.arduino.readline().decode().strip()
                if reponse == '1':
                    print("torque has been disabled, you are free to move the arms ")
                    while True:
                        input("press enter to read current position : \n")
                        self.readPos()

    def calibrate_contour_seq(self):
        self.arduino.write('{T0}'.encode())
        while True:
            if self.arduino.in_waiting > 0:
                reponse = self.arduino.readline().decode().strip()
                if reponse == '1':
                    print("torque has been disabled, you are free to move the arms ")
                    self.readSeq()

    def start_run(self, filepath, numPins):

        self.readThreadedCSV(filepath, numPins)
        commandes = []

        for pin in self.pinsInPulse[0]:
            commandes.append("{C2 %d}" % pin)
            self.Pos["table"].append(pin)
            # self.Pos["left"].append(seq0[4][0])
            # self.Pos["right"].append(seq0[4][1])
            # for s in seq0:
            #     commandes.append(f"{{C1 {s[0]} {s[1]}}}")
            #     self.Pos["left"].append(s[0])
            #     self.Pos["right"].append(s[1])
            #     self.Pos["table"].append(pin)

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

            # eg[i] = (np.abs(self.Pos['left'][i] - self.ActualPos['left'][i]))
            # ed[i] = (np.abs(self.Pos['right'][i] - self.ActualPos['right'][i]))
            # line1.set_ydata(eg)
            # line2.set_ydata(ed)

            ax.set_xlim(0, i + 1)
            fig.canvas.draw()
            plt.draw()
            fig.canvas.flush_events()
