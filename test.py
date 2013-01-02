from Algorithm.ShannonEntropy import *
import Utils

text = Utils.read_file("fichiertest.txt")
variable = ShannonEntropy()
entropy = variable.calculate(text);
print(entropy)