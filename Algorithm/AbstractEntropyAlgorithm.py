from Algorithm.AbstractAlgorithm import *

class AbstractEntropyAlgorithm(AbstractAlgorithm):
    def __init__(self, data):
        AbstractAlgorithm.__init__(self, data)
        
    def countCharacters(self):
        self.characters = {}
        self.totalCharacters = 0
        for i in self.data:
            self.totalCharacters += 1
            try:
                self.characters[i] = self.characters[i] + 1
            except:
                self.characters[i] = 1
        
    def getCharacters(self):
        return self.characters