import pandas as pd
import serial
import time
import numpy as np
import matplotlib
import matplotlib.pyplot as plt


class SCARA_COM:

    def __init__(self, COM):

        # TODO CHECK TON CRISSE DE PORT
        self.pinColours = None
        self.pinsInPulse = None
        self.angles = None
        self.csvfile = None
        self.numPins = None
        self.pins = None
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
        port = "COM%i" % COM
        self.arduino = serial.Serial(port, 115200, timeout=1)

        self.seq0 = [
            (2660, 2769),
            (2732, 2855),
            (2760, 2816),
            (2710, 2759),
            (2560, 2560),
        ]
        self.commandes = []

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
        self.pinColours = list(zip(self.csvfile.R, self.csvfile.G, self.csvfile.B))

        for i in range(np.shape(self.pins)[1]):
            self.pinsInPulse[0][i] = self.angles[self.pins[0][i]]
            self.pinsInPulse[1][i] = self.angles[self.pins[1][i]]

        for pin in self.pinsInPulse[0]:
            self.commandes.append("{C5 %d}" % pin)
            self.Pos["table"].append(pin)

    def getNumLinesCSV(self):
        return len(self.csvfile.p1)

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

    def send_one_line(self, index, cmd):
        # for index, cmd in enumerate(commandes):

        self.envoie_commande(cmd)
        self.readPos()

        # self.et[index] = (np.abs(self.Pos['table'][index] - self.ActualPos['table'][index]))
        # self.line3.set_ydata(self.et)
        #
        # self.eg[index] = (np.abs(self.Pos['left'][index] - self.ActualPos['left'][index]))
        # self.ed[index] = (np.abs(self.Pos['right'][index] - self.ActualPos['right'][index]))
        # self.line1.set_ydata(self.eg)
        # self.line2.set_ydata(self.ed)
        #
        # self.ax.set_xlim(0, index + 1)
        # self.fig.canvas.draw()
        # plt.draw()
        # self.fig.canvas.flush_events()

    # def start_run(self, filepath, numPins):
    #
    #     self.readThreadedCSV(filepath, numPins)
    #
    #     for pin in self.pinsInPulse[0]:
    #         commandes.append("{C2 %d}" % pin)
    #         self.Pos["table"].append(pin)
    #         # self.Pos["left"].append(seq0[4][0])
    #         # self.Pos["right"].append(seq0[4][1])
    #         # for s in seq0:
    #         #     commandes.append(f"{{C1 {s[0]} {s[1]}}}")
    #         #     self.Pos["left"].append(s[0])
    #         #     self.Pos["right"].append(s[1])
    #         #     self.Pos["table"].append(pin)
    #
    #     x = np.arange(len(commandes))
    #     eg = np.zeros(len(commandes))
    #     ed = np.zeros(len(commandes))
    #     et = np.zeros(len(commandes))
    #
    #     plt.ion()
    #     fig = plt.figure()
    #     ax = fig.add_subplot(111)
    #     ax.set_ylim((0, 10))
    #     line1, = ax.plot(x, eg, 'b-')
    #     line2, = ax.plot(x, ed, 'r-')
    #     line3, = ax.plot(x, et, 'g-')
    #
    #     for i, cmd in enumerate(commandes):
    #         self.envoie_commande(cmd)
    #         self.readPos()
    #
    #         et[i] = (np.abs(self.Pos['table'][i] - self.ActualPos['table'][i]))
    #         line3.set_ydata(et)
    #
    #         # eg[i] = (np.abs(self.Pos['left'][i] - self.ActualPos['left'][i]))
    #         # ed[i] = (np.abs(self.Pos['right'][i] - self.ActualPos['right'][i]))
    #         # line1.set_ydata(eg)
    #         # line2.set_ydata(ed)
    #
    #         ax.set_xlim(0, i + 1)
    #         fig.canvas.draw()
    #         plt.draw()
    #         fig.canvas.flush_events()


if __name__ == "__main__":
    scara_com = SCARA_COM(7)
    # scara_com.manual_measure_dxl()
    # scara_com.envoie_commande("{C1 1952 2800}")
    # scara_com.calibrate_contour_seq()
    scara_com.readThreadedCSV("GUI/Output/ThreadedCSVFile.csv", 125)