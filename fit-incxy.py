#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script derived from one created by Antoine Bérut (ILM)
http://ilm-perso.univ-lyon1.fr/~aberut/documents.html#python


Made by Martin Vérot, ENS de Lyon.


You need to change the definition of func and func prime and define properly x,y, and the corresponding uncertainties

"""

# Importation des librairies
import numpy as np
import scipy.optimize as spopt
import matplotlib.pyplot as plt
import numpy.random as random
import matplotlib.ticker as tick
#Definition des fonctions
def func(x,p):
    """
    x : values where the function is knwon 
    p : parameters to perform the fit 
    """
    a,b,c=p
    return a*np.exp(-c*x)+b

def funcprim(x,p):
    """
    Derivative og the function to fit 
    """
    a,b,c=p
    return -c*a*np.exp(-c*x) 

def residuals(p, y, x,x_inc,y_inc,func,funcprim):
    """
    Function to minimize
        p paramters
        x x values
        x_inc uncertainty on x
        y_inc uncertainty on y
        func function to fit
        funcprime derivative of the function
    """
    err = (y-func(x,p))/np.sqrt(y_inc**2 + (funcprim(x,p)*x_inc)**2)
    return err

 

# Programme principal
if __name__ == "__main__":

    #Things to change : a readable version of the function to fit
    funcTitle = r'$y=a\times \exp(-c\times x)+b$'
    #Intial estimate of the parameters
    par0 = [4,10,0.3]
    #Readable name of the parameters
    parnames = ['a','b','c']
    xName = 'x'
    yName = 'y'
    
    #Reading the first four values from  the csv file (you can change it with usecols), the delimiter or comment can be changed, you can also skip the first line with skip_header
    x,x_inc,y,y_inc = np.genfromtxt('data.csv', delimiter=',',usecols=(0,1,2,3),skip_header=0,comments='#',unpack=True)

    if len(par0)!=len(parnames):
        print('The number of parameters to optimize in not the same as the number of parameter names given')

    
    
    #Performing the fit 
    result=spopt.leastsq(residuals,par0,args=(y, x,x_inc,y_inc, func, funcprim),Dfun=None, full_output=1)
    popt = result[0]
    print('Optimal parameters')
    print(popt)
    try :
        print('Uncertainty on the parameters (given at 1 sigma)')
        #print(result)
        upopt = np.sqrt(np.abs( np.diagonal(result[1])))
        print(upopt)
    except: 
        print('Error during optimization')
        print(result)
    x_smooth = np.linspace(min(x),max(x),201)
    

    fig = plt.figure(figsize=(10,6))
    gs = fig.add_gridspec(2, 2,  width_ratios=(1, 1), height_ratios=(2, 1), left=0.08, right=0.95, bottom=0.05, top=0.95, wspace=0.18, hspace=0.3)

    #Plot of the points with the optimal fit
    ax1 = fig.add_subplot(gs[0,0])
    ax1.errorbar(x,y,xerr=x_inc,yerr=y_inc,fmt='b+',elinewidth = 0.7)
    ax1.plot(x_smooth,func(x_smooth,popt),'r')
    ax1.set_ylim(min(y-y_inc)*0.95,max(y+y_inc)*1.05)
    ax1.set_xlabel(xName)
    ax1.set_ylabel(yName)
    ax1.set_title('Best Fit')

    #Plotting residuals
    ax2 = fig.add_subplot(gs[1,0])
    ax2.axhline(0,color='#cccccc',zorder=-1)
    ax2.errorbar(x,y-func(x,popt),xerr=x_inc,yerr=y_inc,fmt='b+',lw=0,elinewidth = 0.7)
    ax2.set_title('Residuals')

    #Influence of the different parameters : the functions are plotted at 1 sigma for each parameter to see how they impact the fitted function 
    ax3 = fig.add_subplot(gs[0,1])
    ax3.errorbar(x,y,xerr=x_inc,yerr=y_inc,fmt='b+',lw=0,elinewidth = 0.7)
    ax3.set_xlabel(xName)
    ax3.set_ylabel(yName)
    ax3.set_title('Influence of the uncertainty of parameters')
    for i in range(len(popt)):
        uncer = np.zeros_like(popt)
        uncer[i]=upopt[i]
        #Plotting the fitted function at 1 sigma for each parameter
        ax3.plot(x_smooth,func(x_smooth,popt+uncer),color='C{}'.format(i),linewidth=1.0,label='{}'.format(parnames[i]))
        ax3.plot(x_smooth,func(x_smooth,popt-uncer),color='C{}'.format(i),linewidth=1.0)
        #Plotting the area between the extremum of the curves for each parameter
        ymin = np.minimum(func(x_smooth,popt+uncer),func(x_smooth,popt-uncer))
        ymax = np.maximum(func(x_smooth,popt+uncer),func(x_smooth,popt-uncer))
        ax3.fill_between(x_smooth, ymin, ymax, color='C{}'.format(i), alpha=0.1)
    ax3.legend(loc='upper right') 


    #Plotting the value of each parameter and their values at 1 sigma (lower right graph)
    ax4 = fig.add_subplot(gs[1,1])
    ax4.set_title(funcTitle)
    ax4.spines['top'].set_visible(False)
    ax4.spines['right'].set_visible(False)
    ax4.spines['bottom'].set_visible(False)
    ax4.spines['left'].set_visible(False)
    ax4.axes.get_xaxis().set_visible(False)
    ax4.axes.get_yaxis().set_visible(False)
    gspars = gs[1,1].subgridspec(len(popt)+1,3)
    axcomm = fig.add_subplot(gspars[0,:])
    axcomm.set_ylim(-len(popt)-0.5,0.5+len(popt)+1)
    axcomm.spines['top'].set_visible(False)
    axcomm.spines['right'].set_visible(False)
    axcomm.spines['bottom'].set_position('zero')
    axcomm.spines['left'].set_visible(False)
    axcomm.axes.get_yaxis().set_visible(False)
    for i in range(len(popt)):      
        #Displaying the common values
        axcomm.errorbar(popt[i],[len(upopt)-i+1],xerr=[upopt[i]],marker='',capsize = 3)
        #Displaying a subplot with the values given at 1 sigma for the paramaters
        ax = fig.add_subplot(gspars[i+1,0])
        ax.errorbar(popt[i],[0],xerr=[upopt[i]],marker='',capsize = 3,color='C{}'.format(i),zorder=5)
        ax.set_ylim(-0.5,0.5)
        ax.set_xlim(popt[i]-upopt[i],popt[i]+upopt[i])
        ax.set_xticks([popt[i]-upopt[i],popt[i],popt[i]+upopt[i]])
        ax.xaxis.set_major_formatter(tick.StrMethodFormatter('{x:.2f}'))
        ax.axes.get_yaxis().set_visible(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['bottom'].set_position('zero')
        ax.spines['left'].set_visible(False)
        #Adding the parameter names
        ax5 = fig.add_subplot(gspars[i+1,1:])
        ax5.text(0,0.4,'{}'.format(parnames[i]))
        ax5.spines['top'].set_visible(False)
        ax5.spines['right'].set_visible(False)
        ax5.spines['bottom'].set_visible(False)
        ax5.spines['left'].set_visible(False)
        ax5.axes.get_xaxis().set_visible(False)
        ax5.axes.get_yaxis().set_visible(False)

    plt.show()
