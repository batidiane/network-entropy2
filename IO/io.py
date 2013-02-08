from Utils import *
import IO
class Data:
    def __init__(self, printname):
        self.printer = load_printer(printname)
        self.data = {}
    
    
    def getData(self):
        return self.data
    
    def add(self, name, value):
        if name in self.data:
            self.data[name] += value
        else:
            self.data[name] = value
    def printData(self, keys):
        self.printer.printData(keys, self.data)

    def apply_function(self, keys, function):
        for key in keys:
            try:
                self.data[key+' entropy'] = function(self.data[key])
            except:
                pass



class IPPacket(Data):
    
    def __init__(self, pktinfos, payload, timestamp):
        Data.__init__(self, "IP Packet")
        self.add('timestamp', timestamp)
        for key in pktinfos:
            self.add(key, pktinfos[key])
        self.add('payload', payload)
 
        
    def printData(self, keys):
        self.printer.printData(keys, self.data)
        

        

        
def load_printer(printname):
    mod = __import__('IO.printers', fromlist=IO.__all__)
    for i in IO.printers.__dict__:
        try:
            mod_instance = getattr(mod, i)()
            if mod_instance.getName() == printname:
                return mod_instance
        except:
            pass
    return getattr(mod, IO.printers.default_printer_class)()




        
    
