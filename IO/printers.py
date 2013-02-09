#!/usr/bin/env python

default_printer_class = 'Console'

class AbstractPrinter:
    def __init__(self, name):
        self.name = name
        
    def printData(self, keys, data):
        raise NotImplementedError
    
    def getName(self):
        return self.name
    
class Console(AbstractPrinter):
    def __init__(self):
        AbstractPrinter.__init__(self, "console")
        
    def printData(self, keys, data):
        res = ''
        for key in keys:
            try:
                res += key+':'+str(data[key])+'  |  '
            except:
                pass
        print res
