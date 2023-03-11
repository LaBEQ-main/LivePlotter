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
    plotlist = []
    overlay_bool = False
    paused = False

    def convertfilepath(self, filepath):
        return filepath.replace('/',"\\")

    def start(self, file, vars):
        global xcol, ycol, f, fname
        xcol = vars[0]
        ycol = vars[1]
        f = file
        fname = (f.split("\\")[-1])

        print('plotting',xcol,',',ycol,'data from: ',file)
        fig = plt.figure()
        self.ani = FuncAnimation(fig, self.animate, interval=500)
        
        #allow plot to pause on click
        fig.canvas.mpl_connect('button_press_event', self.toggle_pause)

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
        plt.plot(x, y)
        plt.tight_layout()

    def start_overlay(self):
        global x, y, plist, namedict
        plist = self.plotlist
        namedict = {}
        x = {}
        y = {}
        
        
        print('Plotting overlay using: ')
        for filepair in plist:
            file = filepair[0]
            vars = filepair[1]
            print(vars,'data from: ',file)
            fname = file.split("\\")[-1]
            namedict[file] = fname
        
        fig = plt.figure()
        self.ani = FuncAnimation(fig, self.animate_overlay, interval=500)

        #allow plot to pause on click
        fig.canvas.mpl_connect('button_press_event', self.toggle_pause)

        plt.tight_layout()
        plt.show()

    def toggle_pause(self, *args, **kwargs):
        if self.paused:
            self.ani.resume()
        else:
            self.ani.pause()

        #toggle paused bool
        self.paused = not self.paused

    def animate_overlay(self, i):
        
        plt.cla()
        #get new data from each file and plot all on the same graph
        for filepair in plist:
            file = filepair[0]
            vars = filepair[1]
            data = pd.read_csv(file, sep = '\t')
            xcol = vars[0]
            ycol = vars[1]
            x = data[xcol]
            y = data[ycol]

            #plot overlay
            plt.tight_layout()
            plt.xlabel(str(xcol))
            plt.ylabel(str(ycol))
            plt.title(f"Live Overlay")
            plt.plot(x, y, label = ycol)
            plt.legend(loc='best')

    def start_plot(self):
        if self.overlay_bool == False:
            for filedatapair in self.plotlist:
                file = filedatapair[0]
                vars = filedatapair[1]
                Process(target=self.start, args=(file, vars)).start()
        else:
            #Need to put a comma after dict passed into process for some reason. Not sure why.
            Process(target=self.start_overlay, args=()).start()

def main():
    print('CPU core count: ', os.cpu_count())

    lplot = LivePlotter()
    lplot.overlay_bool = True
    lplot.plotlist = [['C:\\Users\\2administrator\\Documents\\Device Logs\\MercuryiPS Magnet Temp Over Time 6.9.2022\\Mag_PT1_PT2_Temps_06102022_17-40-00.txt',('time (s)', 'Mag temp (K)')],
                ['C:\\Users\\2administrator\\Documents\\Device Logs\\MercuryiPS Magnet Temp Over Time 6.9.2022\\Mag_PT1_PT2_Temps_06102022_17-40-00.txt',('time (s)', 'PT1 temp (K)')]]
    lplot.start_plot()

if __name__ == '__main__':
    main()

