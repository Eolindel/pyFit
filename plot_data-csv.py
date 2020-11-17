#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
plot data from a csv file the column used can be changed
"""

# Importation des librairies
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as tick
import locale
locale.setlocale(locale.LC_NUMERIC, "fr_FR.utf8")
mpl.rcParams['axes.formatter.use_locale'] = True


# Programme principal
if __name__ == "__main__":
    fileOutput = "plot_data.pdf"
    fileName = "data.csv"
    x =np.linspace(0,3,1000)
    fig = plt.figure(figsize=(8,6))
    data = np.genfromtxt(fileName,skip_header=0, delimiter=',', usecols=(0,2), names=['x','y'] )

    gs = fig.add_gridspec(1, 1)#,  width_ratios=(1, 1), height_ratios=(2, 1), left=0.08, right=0.95, bottom=0.05, top=0.95, wspace=0.18, hspace=0.3
    ax1 = fig.add_subplot(gs[0,0])
    #adding zero to see where it lies
    ax1.axhline(0,color='#cccccc')
    ax1.plot(data['x'],data['y'],marker='+',lw=0)



    #labels for the axes and the whole figure
    ax1.set_xlabel('$T~ (\mathrm{K})$')
    ax1.set_ylabel('$B_2~\left(\mathrm{cm^3\cdot mol^{-1}}\\right)$')
    #ax1.set_title('Potentiel de Lennard-Jones')
    
    #setting limits
    #ax1.set_ylim(-1.1,1.1)
    #ax1.set_ylim(min(y),max(y))
    #ax1.set_xlim(min(x),max(x))
    #ax1.spines['bottom'].set_position('zero')
    ax1.spines['top'].set_visible(False)
    ax1.spines['right'].set_visible(False)
    #ax1.spines['left'].set_visible(True)
    #plt.setp(ax1.get_xticklabels(), position=(-1.,0.12))
    #plt.legend(loc='upper left')
    plt.tight_layout()
    plt.savefig(fileOutput)
    plt.show()
    pass

