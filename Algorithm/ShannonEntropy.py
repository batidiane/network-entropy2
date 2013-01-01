from Algorithm.AbstractEntropyAlgorithm import *
import math


class ShannonEntropy(AbstractEntropyAlgorithm):
    def __init__(self, data):
        AbstractEntropyAlgorithm.__init__(self, data)
        
    def execute(self):
        self.countCharacters()
        entropy = 0
        for occurence in self.characters.values():
            frequency = occurence / self.totalCharacters
            entropy += frequency * math.log2(frequency)
        return -entropy