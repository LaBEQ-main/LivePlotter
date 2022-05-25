# -*- coding: utf-8 -*-
# -----------------------------------------------------------------------------
# Authors - Frank Duffy, LaBEQ / Sardashti Research Group, Clemson University
#
# Based on tutorials about matplotlib animate by Corey Schafer and multiprocessing
# by Engineer Man
#
# Distributed under the terms of the BSD license.
#
# The full license is in the file LICENCE, distributed with this software.
# -----------------------------------------------------------------------------
# import random
from cProfile import label
from itertools import count
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import time

from csv import writer
from multiprocessing import Process
import os

from atom.api import Atom, Str

plt.style.use('fivethirtyeight')
x_vals = []
y_vals = []
index = count()

class LivePlotter():
    filedict ={}
    overlay_bool = False

    def start(self, file, vars):
        global xcol, ycol, f, fname
        xcol = vars[0]
        ycol = vars[1]
        f = file
        fname = (f.split("\\")[-1])

        print('plotting',xcol,',',ycol,'data from: ',file)
        fig = plt.figure()
        ani = FuncAnimation(fig, self.animate, interval=500)
        plt.tight_layout()
        plt.show()

    def animate(self, i):
        
        data = pd.read_csv(f, sep = '\t')
        x = data[xcol]
        y = data[ycol]

        plt.cla()
        plt.xlabel(str(xcol))
        plt.ylabel(str(ycol))
        plt.title(f"Live plot: {fname}")
        plt.plot(x, y, label=f'Channel {fname}')
        plt.legend(loc='upper right')
        plt.tight_layout()

    def start_overlay(self, filedict):
        global x, y, fdict, namedict
        fdict = filedict
        namedict = {}
        x = {}
        y = {}
        
        
        print('Plotting overlay using: ')
        for file in filedict:
            print(filedict[file],'data from: ',file)
            fname = file.split("\\")[-1]
            namedict[file] = fname
        
        fig = plt.figure()
        ani = FuncAnimation(fig, self.animate_overlay, interval=500)
        plt.tight_layout()
        plt.show()

    def animate_overlay(self, i):
        
        #get new data
        for file in fdict:
            data = pd.read_csv(file, sep = '\t')
            xcol = fdict[file][0]
            ycol = fdict[file][1]
            x[file] = data[xcol]
            y[file] = data[ycol]

        #plot overlay
        plt.cla()
        plt.xlabel(str(xcol))
        plt.ylabel(str(ycol))
        plt.title(f"Live Overlay")
        for file in fdict:
            plt.plot(x[file], y[file], label= namedict[file])
            plt.legend(loc='upper right')
            plt.tight_layout()


def main():
    print('CPU core count: ', os.cpu_count())

    lplot = LivePlotter()
    lplot.overlay_bool = True
    lplot.filedict = {'C:\\Users\\2administrator\\exopy\\tests\\LivePlottingTest\\ot1.csv': ('x', 'y'),
                'C:\\Users\\2administrator\\exopy\\tests\\LivePlottingTest\\ot2.csv': ('x', 'y')}


    if lplot.overlay_bool == False:
        for file in lplot.filedict:
            print(file)
            vars = lplot.filedict[file]
            Process(target=lplot.start, args=(file, vars)).start()
    else:
        #Need to put a comma after dict passed into process for some reason. Not sure why.
        Process(target=lplot.start_overlay, args=(lplot.filedict,)).start()

if __name__ == '__main__':
    main()

