from Algorithm.ShannonEntropy import *
from IO.inputs import *



if __name__ == "__main__":
    text = InputFile("fichiertest.txt")
    variable = ShannonEntropy()
    entropy = variable.calculate(text)
    print(entropy)