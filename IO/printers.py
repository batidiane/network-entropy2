#!/usr/bin/env python
import sys
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
        
    def printData(self, keys, keys_calculated, data):
        res = ''
        for key in keys:
            try:
                res += key+':\033[32m'+str(data[key])+'\033[37m  |  '
            except:
                pass
        res += '\nResult : '
        for key in keys_calculated:
            try:
                res += key+':\033[31m'+str(data[key])+'\033[37m  |  '
            except:
                pass
        print res+'\n'
