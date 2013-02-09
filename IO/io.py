from Utils import *
import IO
class Data:
    keys_calculated = []
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
        self.printer.printData(keys, Data.keys_calculated, self.data)

    def apply_function(self, keys, algorithm):
        for key in keys:
            try:
                new_key = key+'_'+algorithm.getName()+'_'+algorithm.getType()
                self.data[new_key] = algorithm.calculate(self.data[key])
                if new_key not in Data.keys_calculated:
                    Data.keys_calculated.append(new_key)
            except:
                pass



class IPPacket(Data):
    
    def __init__(self, pktinfos, payload, timestamp):
        Data.__init__(self, "IP Packet")
        self.add('timestamp', timestamp)
        for key in pktinfos:
            self.add(key, pktinfos[key])
        self.add('payload', payload)
 
        

        

        

        
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




        
    
