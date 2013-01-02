from Algorithm.AbstractAlgorithm import *

class AbstractEntropyAlgorithm(AbstractAlgorithm):
    
        
    def countCharacters(self, data):
        self.characters = {}
        self.totalCharacters = 0
        for i in data:
            self.totalCharacters += 1
            try:
                self.characters[i] = self.characters[i] + 1
            except:
                self.characters[i] = 1
    
        
    def getCharacters(self):
        return self.characters