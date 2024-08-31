import pandas as pd
import serial
import numpy as np


class SCARA_COM:

    def __init__(self, COM):

        self.pinColours = None
        self.pinsInPulse = None
        self.angles = None
        self.csvfile = None
        self.numPins = None
        self.pins = None
        # matplotlib.use("TkAgg")

        self.ActualPos = []

        # TODO CHECK TON CRISSE DE PORT
        port = "COM%i" % COM
        self.arduino = serial.Serial(port, 115200, timeout=1, write_timeout=1)

        self.commandes = []

    def __del__(self):
        self.arduino.close()

    def envoie_commande(self, commande):
        print(f"Python: {commande}")
        self.arduino.write(commande.encode())
        while True:
            if self.arduino.in_waiting > 0:
                reponse = self.arduino.readline().decode().strip()
                print(f"Arduino : {reponse}")
                if reponse == '1':  # Attend le signal du arduino
                    break  # Sort de la loop pour envoyer une autre commande

    def check_torque(self):
        print("Python: {T4}")
        self.arduino.write("{T4}".encode())
        while True:
            if self.arduino.in_waiting > 0:
                response = self.arduino.readline().decode().strip()
                return int(response)

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

    def getNumLinesCSV(self):
        return len(self.csvfile.p1)

    def readPos(self):  #, index
        self.arduino.write('{T1}'.encode())
        while True:
            if self.arduino.in_waiting > 0:
                response = self.arduino.readline().decode().strip()
                print(f"position gauche : {response}")
                response = self.arduino.readline().decode().strip()
                print(f"position droite : {response}")
                response = self.arduino.readline().decode().strip()
                print(f"position table : {response}")
                response = int(response)
                pin = (response - np.floor(response / 4096) * 4096) * (125 / 4096)
                self.ActualPos.append(np.round(pin))
                #erreur = abs(self.ActualPos[index] - self.pins[0][index])
                #erreur_pulse = self.pinsInPulse[0][index] - response
                #print(f"erreur pulse : {erreur_pulse}")
                #print(f"erreur : {erreur}\n")
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

        self.envoie_commande(cmd)
        # self.readPos(index)

#
# if __name__ == "__main__":
#     scara_com = SCARA_COM(3)
#     scara_com.envoie_commande("{C1 2449 3125}")
#     #scara_com.envoie_commande("{C2}")
#     scara_com.calibrate_contour_seq()
#     #scara_com.manual_measure_dxl()
#     # scara_com.readThreadedCSV("GUI/Output/ThreadedCSVFile.csv", 150)
#     # for cmd in scara_com.commandes:
#     # scara_com.envoie_commande(cmd)
