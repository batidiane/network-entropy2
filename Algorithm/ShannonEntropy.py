from Algorithm.AbstractEntropyAlgorithm import *
import math


class ShannonEntropy(AbstractEntropyAlgorithm):
    
        
    def calculate(self, data):
        self.countCharacters(data)
        entropy = 0
        for occurence in self.characters.values():
            frequency = occurence / self.totalCharacters
            entropy += frequency * math.log2(frequency)
        return -entropy