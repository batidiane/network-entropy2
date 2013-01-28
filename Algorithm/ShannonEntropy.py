from Algorithm.AbstractEntropyAlgorithm import *
import math


class ShannonEntropy(AbstractEntropyAlgorithm):
    
        
    def calculate(self, data):
        self.countCharacters(data)
        entropy = 0
        for occurence in self.characters.values():
            frequency = occurence / float(self.totalCharacters)
            entropy += frequency * math.log(frequency,2)
        return -entropy
    
    def getName(self):
        return "Shannon Entropy"