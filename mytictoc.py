# -*- coding: utf-8 -*-
"""
Created on Tue Jul 18 11:17:23 2017

@author: Administrator
"""

import time

def tic():
    globals()['tt'] = time.clock()

def toc():
    print ('\nElapsed time: %.8f seconds\n' % (time.clock()-globals()['tt']))
