from Algorithm.ShannonEntropy import *
import Utils


if __name__ == "__main__":
    text = Utils.read_file("fichiertest.txt")
    variable = ShannonEntropy()
    entropy = variable.calculate(text);
    print(entropy)