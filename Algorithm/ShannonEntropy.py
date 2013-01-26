from Algorithm.AbstractEntropyAlgorithm import *
import math


class ShannonEntropy(AbstractEntropyAlgorithm):
    
        
    def calculate(self, inputdata):
        self.countCharacters(inputdata)
        entropy = 0
        for occurence in self.characters.values():
            frequency = occurence / self.totalCharacters
            entropy += frequency * math.log2(frequency)
        return -entropy
    
    def getName(self):
        "Shannon Entropy"