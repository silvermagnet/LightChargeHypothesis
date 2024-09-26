# -*- coding: utf-8 -*-
'''
The MIT License (MIT)

Copyright (c) 2024 Julie Marty

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
'''

import json


import matplotlib.pyplot as plt

def plot_results(tdata, mappedPositions):

    
    
           
         
    
    udata0 = []
    xdata0 = []
    ydata0 = []
    zdata0 = []
    
    udata1 = []
    xdata1 = []
    ydata1 = []
    zdata1 = []
    
    udata2 = []
    xdata2 = []
    ydata2 = []
    zdata2 = []
    

    


    for i in range(0, len(mappedPositions[0])):
        
        
        position = mappedPositions[0][i]
        udata0.append(position[0])
        xdata0.append(position[1])  
        ydata0.append(position[2])
        zdata0.append(position[3])
        
        udata2.append(position[0])
        xdata2.append(position[1])  
        ydata2.append(position[2])
        zdata2.append(position[3])
        
        position = mappedPositions[1][i]
        udata1.append(position[0])
        xdata1.append(position[1])  
        ydata1.append(position[2])
        zdata1.append(position[3])
        
        udata2.append(position[0])
        xdata2.append(position[1])  
        ydata2.append(position[2])
        zdata2.append(position[3])
        
       


    tdata.pop(0)
    udata0.pop(0)
    udata1.pop(0)
    udata2.pop(0)
    xdata0.pop(0)
    xdata1.pop(0)
    xdata2.pop(0)
    ydata0.pop(0)
    ydata1.pop(0)
    ydata2.pop(0)
    zdata0.pop(0)
    zdata1.pop(0)
    zdata2.pop(0)
    
    
    ax = plt.axes(projection='3d')
    ax.scatter(ydata2, xdata2, udata2)
    ax.set_xlabel('y')
    ax.set_ylabel('x')
    ax.set_zlabel('u')
    ax.grid(True)
    
    
    plt.show()  
    
    
    ax = plt.axes(projection='3d')
    ax.scatter(xdata2, ydata2, zdata2)
    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')
    ax.grid(True)
    
    
    plt.show() 
    
    
       
    
    am0 = plt.axes()
    am0.scatter(xdata0, ydata0)
    am0.set_xlabel('x')
    am0.set_ylabel('y')
    am0.grid(True)
    
    plt.show()   
    
    
    am0 = plt.axes()
    am0.scatter(xdata0, udata0)
    am0.set_xlabel('x')
    am0.set_ylabel('u')
    am0.grid(True)
    
    plt.show() 
    
    
    am0 = plt.axes()
    am0.scatter(xdata0, udata0)
    am0.set_xlabel('x')
    am0.set_ylabel('u')
    am0.grid(True)
    
    plt.show() 
    
    
    am0 = plt.axes()
    am0.scatter(ydata0, udata0)
    am0.set_xlabel('y')
    am0.set_ylabel('u')
    am0.grid(True)
    
    plt.show() 
    
    
    am0 = plt.axes()
    am0.scatter(tdata, ydata0)
    am0.set_xlabel('t')
    am0.set_ylabel('y')
    am0.grid(True)
    
    plt.show() 
    
    
    am0 = plt.axes()
    am0.scatter(tdata, xdata0)
    am0.set_xlabel('t')
    am0.set_ylabel('x0')
    am0.grid(True)
    
    plt.show() 
    
    
    am0 = plt.axes()
    am0.scatter(tdata, udata0)
    am0.set_xlabel('t')
    am0.set_ylabel('u0')
    am0.grid(True)
    
    plt.show() 
    
    am1 = plt.axes()
    am1.scatter(tdata, xdata1)
    am1.set_xlabel('t')
    am1.set_ylabel('x1')
    am1.grid(True)
    
    plt.show() 
    
    
    am1 = plt.axes()
    am1.scatter(tdata, udata1)
    am1.set_xlabel('t')
    am1.set_ylabel('u1')
    am1.grid(True)
    
    plt.show()
    
    
    am1 = plt.axes()
    am1.scatter(tdata, ydata1)
    am1.set_xlabel('t')
    am1.set_ylabel('y')
    am1.grid(True)
    
    plt.show() 
    
    
    am1 = plt.axes()
    am1.scatter(xdata1, ydata1)
    am1.set_xlabel('x')
    am1.set_ylabel('y')
    am1.grid(True)
    
    plt.show()  
    
    
    am1 = plt.axes()
    am1.scatter(udata1, xdata1)
    am1.set_xlabel('u')
    am1.set_ylabel('x')
    am1.grid(True)
    
    plt.show()  
    
    
    ax = plt.axes(projection='3d')
    am0 = plt.axes()
    am0.scatter(xdata0, ydata0)
    am0.set_xlabel('x')
    am0.set_ylabel('y')
    am0.grid(True)
    
    plt.show() 
    
    

    
    
    ax = plt.axes(projection='3d')
    
    
    ax.scatter(ydata0, xdata0, udata0)
    ax.set_xlabel('y')
    ax.set_ylabel('x')
    ax.set_zlabel('u')
    ax.grid(True)
    
    plt.show()
    
    
    ax = plt.axes(projection='3d')
    ax.scatter(ydata1, xdata1, udata1)
    ax.set_xlabel('y')
    ax.set_ylabel('x')
    ax.set_zlabel('u')
    ax.grid(True)
    
    plt.show()
    
with open('tdataOutput.json', 'r') as openfile:
    tdata = json.load(openfile)
    
with open('positionsOutput.json', 'r') as openfile:
    mappedPositions = json.load(openfile)

print("mapped positions")
print(len(mappedPositions))
print(len(mappedPositions[0]))
print(len(mappedPositions[0][0]))
print(mappedPositions)


    
    




plot_results(tdata, mappedPositions) 
