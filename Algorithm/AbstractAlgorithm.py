

class AbstractAlgorithm:
    def __init__(self, data):
        self.data = data
        
    def execute(self):
        raise NotImplementedError
    
    