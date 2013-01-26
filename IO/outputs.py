from Utils import *

class Output:
    
    def __init__(self, outputname, result):
        self.outputname = outputname
        self.result = result
        
    def getOutputName(self):
        return self.outputname
    
    def getResult(self):
        return self.result