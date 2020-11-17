#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Plot a function into a pdf file (vectorial form) from matplotlib

The most basic use is to change the function func and probably the boundaries of x 
"""

# Importation des librairies
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
#Changing the decimal separator to a comma
import locale
locale.setlocale(locale.LC_NUMERIC, "fr_FR.utf8")
mpl.rcParams['axes.formatter.use_locale'] = True

# Definition des fonctions
def func(x):
    return 4*(1/x**12 - 1/x**6)

# Programme principal
if __name__ == "__main__":
    #Name of the output file
    fileOutput = "Lennard-Jones.pdf"
    #Range of values where the data will be evaluated
    x =np.linspace(0,3,1000)

    #starting the figure
    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(1, 1)#,  width_ratios=(1, 1), height_ratios=(2, 1), left=0.08, right=0.95, bottom=0.05, top=0.95, wspace=0.18, hspace=0.3
    ax1 = fig.add_subplot(gs[0,0])
    #plot a vertical line at zero to give a hint on where it lies
    ax1.axhline(0,color='#cccccc')

    ax1.plot(x,func(x))



    #labels for the axis and title of the graph
    ax1.set_xlabel('$\dfrac{\sigma}{r}$')
    ax1.set_ylabel('$\dfrac{u(r)}{\epsilon}$')
    ax1.set_title('Potentiel de Lennard-Jones')
    #set limits to the plotted data (to crop for example)
    #ax1.set_ylim(-1.1,1.1)
    ax1.set_ylim(min(y),max(y))
    ax1.set_xlim(min(x),max(x))
    #show or hide the bounding axes
    ax1.spines['bottom'].set_visible(True)#.set_position('zero')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    ax1.spines['left'].set_visible(True)
    #change the position of the ticks
    #plt.setp(ax1.get_xticklabels(), position=(-1.,0.12))
    #plt.legend(loc='upper left')
    plt.savefig(fileOutput)
    plt.show()

