'''
Created on 26 нояб. 2021 г.

@author: Arthur Stankevich
'''
from datetime import datetime

def quarterdate(offset):
    first = [1,2,3,-11,-10,-9]
    second = [4,5,6,-6,-7,-8]
    third = [7,8,9,-3,-4,-5]
    d = datetime.now().month-offset*3
    y = datetime.now().year
    if d<=0:
        y -= 1
    if d in first:
        return f'{y}-01-01'
    elif d in second:
        return f'{y}-04-01'
    elif d in third:
        return f'{y}-07-01'
    else:
        return f'{y}-10-01'
    
# print(quarterdate(3))