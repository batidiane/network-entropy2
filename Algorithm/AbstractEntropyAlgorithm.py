from Algorithm.AbstractAlgorithm import *

class AbstractEntropyAlgorithm(AbstractAlgorithm):
    
        
    def countCharacters(self, data):
        self.characters = {}
        self.totalCharacters = 0
        try:
            data = str(data)
            for i in data:
                self.totalCharacters += 1
                if i in self.characters:
                    self.characters[i] = self.characters[i] + 1
                else:
                    self.characters[i] = 1
        except:
            self.characters[0] = 1
            self.totalCharacters = 1

        
    def getCharacters(self):
        return self.characters