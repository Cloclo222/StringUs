import serial
import time

arduino = serial.Serial('COM4', 115200, timeout=1)
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
    "{C1 56 236}",
    "{C1 11 225}",
    "{C1 62 203}",
    "{C1 68 206}",
    "{C1 30 210}",
]

for cmd in commandes:
    envoie_commande(cmd)
    time.sleep(0.01)  #Pour laisser le temps au arduino de calculer
    
#arduino.close()  # Si toute les commandes sont complété
