# -*- coding: utf-8 -*-
"""
Created on Fri Oct 18 16:07:46 2019

@author: student
"""

with open('text.txt') as f:
    print(f.read(10))  # 'The o'
    f.read(3)  # 'nly'