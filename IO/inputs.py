
from Utils import *

class Input:
    
    def __init__(self, inputtype, data):
        self.type = inputtype
        self.data = data
    
    def getType(self):
        return self.inputtype
    
    def getData(self):
        return self.data
    
class InputFile(Input):
    
    def __init__(self, filename):
        Input.__init__(self, "File", read_file(filename))
    