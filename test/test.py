'''
Created on 27 janv. 2013

@author: eric
'''


import Algorithm
import IO
import sys



for mod_name in Algorithm.__all__:
    mod = __import__('Algorithm.'+mod_name, fromlist=Algorithm.__all__)
    #print mod_name
    mod_instance = getattr(mod, mod_name)()
    try:
        print mod_instance.getName()
    except:
        pass