#!/usr/bin/env python
import sys
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import threading
default_printer_class = 'RFile'

class AbstractPrinter:
    def __init__(self, name):
        self.name = name
        
    def printData(self, keys, keys_calculated, data):
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

class RFile(AbstractPrinter):
    columns = None
    file = None
    def __init__(self):
        AbstractPrinter.__init__(self,"rfile")
        
    def printData(self, keys, keys_calculated, data):
        #Console.printData(self, keys, keys_calculated, data)
        
        if RFile.columns == None:
            RFile.columns = []
            RFile.file = open('data2.txt','a')
            res = ''
            for key in keys:
                if key not in RFile.columns:
                    RFile.columns.append(key)
                    res += key+'|'
            for key in keys_calculated:
                if key not in RFile.columns:
                    RFile.columns.append(key)
                    res += key+'|'
            res=res[:-1]
            RFile.file.write(res+'\n')
        res = ''
        for col in RFile.columns:
            try:
                res += str(data[col])+'|'
            except:
                res += '|'
        res=res[:-1]
        RFile.file.write(res+'\n')
        
class Graph(AbstractPrinter):
    fig =None
    ax = None
    x = None
    line = None
    y = None
    def __init__(self):
        AbstractPrinter.__init__(self, "graph")
        Graph.fig = plt.figure()
        Graph.ax = Graph.fig.add_subplot(111)
        Graph.x = np.arange(0, 2*np.pi, 0.01) 
        Graph.y = []
        Graph.line, = Graph.ax.plot(Graph.x, np.sin(Graph.x))
        #ani = animation.FuncAnimation(Graph.fig, self.animate, np.arange(1, 200), init_func=self.graphinit,interval=25, blit=True)
        thread= threading.Thread(None, self.funcAnimation, None)
        plt.show()
        thread.start()
        
    def animate(self, i):
        Graph.line.set_ydata(np.sin(Graph.x+i/10.0))  # update the data
        return Graph.line,
    
    def funcAnimation(self):
        animation.FuncAnimation(Graph.fig, self.animate, np.arange(1, 200), init_func=self.graphinit,interval=25, blit=True)
    
    #Init only required for blitting to give a clean slate.
    def graphinit(self):
        Graph.line.set_ydata(np.ma.array(Graph.x, mask=True))
        return Graph.line,
        
        
    def printData(self,keys, keys_calculated, data):
        for key in keys_calculated:
            try:
                Graph.x.append(data['timestamp'])
                Graph.y.append(data[key])
            except Exception as e:
                print e
        
        
        
        
        
        
        
        
        
        
        