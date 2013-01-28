'''
Created on 27 janv. 2013

@author: eric
'''


import Algorithm
import IO
import sys



for mod_name in IO.__all__:
    mod = __import__('IO.'+mod_name, fromlist=IO.__all__)
    print mod_name
    mod_instance = getattr(mod, 'ConsoleOutput')()