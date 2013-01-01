from Algorithm.ShannonEntropy import *
import Utils

text = Utils.read_file("fichiertest.txt")
variable = ShannonEntropy(text)
entropy = variable.execute();
print(entropy)