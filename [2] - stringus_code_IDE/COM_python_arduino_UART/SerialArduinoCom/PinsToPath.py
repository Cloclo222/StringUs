import pandas as pd
import numpy as np

# TODO: Parse colours to know when to switch
class Path:

    def __init__(self, csvfilepath, numPins):
        self.csvfile = pd.read_csv(csvfilepath)
        self.numPins = numPins
        self.angles = np.linspace(0, 4096, numPins + 1, dtype=int)

        self.pins = np.array((self.csvfile.p1, self.csvfile.p2))
        self.pinsInPulse = np.zeros_like(self.pins).astype(np.float32)
        self.convertPinsToPulse()

    def convertPinsToPulse(self):
        for i in range(np.shape(self.pins)[1]):
            self.pinsInPulse[0][i] = self.angles[self.pins[0][i]]
            self.pinsInPulse[1][i] = self.angles[self.pins[1][i]]


if __name__ == "__main__":
    path = Path("the_rock.csv", 250)



    print(path.pins)
