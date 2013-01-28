from Utils import *


class IO:
    def __init__(self, ioname):
        self.ioname = ioname
        self.data = {}
    
    def getIOName(self):
        return self.ioname
    
    def getData(self):
        return self.data
    
    def add(self, name, value):
        if name in self.data:
            self.data[name] += value
        else:
            self.data[name] = value
        

    
class InputFile(IO):
    
    def __init__(self, filename):
        IO.__init__(self, "File")
        self.add("content file", read_file(filename))
        
class InputIPPacket(IO):
    
    def __init__(self, packet):
        IO.__init__(self, "IP Packet")
        for key in packet:
            self.add(key, packet[key])
        
class Output(IO):
    def __init__(self, outputtype, resultname):
        IO.__init__(self, outputtype)
        self.resultname = resultname
        
    def printOutput(self):
        raise NotImplementedError
        
class ConsoleOutput(Output):
    
    def __init__(self, resultname):
        Output.__init__(self, "Console Output", resultname)
        
    def printOutput(self):
        print self.resultname
        for key in self.data:
            print '    '+key+" = "+str(self.data[key])