# -*- coding: utf-8 -*-
"""
@author: mango
"""
#Libraries
import scipy.odr
import numpy as np
from matplotlib import pyplot as plt
from funzioni_secondarie import fileselect, print_plot, print_params, curve_fit

##SELEZIONE FILE
nome = fileselect()

##INIZIALIZZAZIONE GRAFICO
#ecolor: colore punti, fmt: forma punti, barsabove: metti a True se non si vede l'errore, ms: dimensione punti sperimentali
x, xerror, y, yerror= np.loadtxt(nome, unpack=True, delimiter = ";", skiprows=1)
plt.errorbar(x,y,xerr=xerror, yerr=yerror, fmt ="o", ecolor="black", barsabove=False, ms= 2)

##MODIFICARE SE VUOI UN FIT
#esempio di modello: beta[0]+beta[1]*np.cos(x**2)
def model(beta,x):
    return beta[0]*np.cos(beta[1]*x+beta[2])
#qui metti una lista con i parametri
initial_guess = [0,0,0]
selection = input("Hai bisogno di fare un fit? [y o invio per confermare]: ")
if selection == "y" or selection == "":
    data = [x,y,xerror,yerror]
    curve_fit(model,initial_guess,data)
    
##DEFINIZIONE ETICHETTE
plt.title("Grafico")
plt.xlabel("Asse x [udm]")
plt.ylabel("Asse y [udm]")


##PARAMETRI OPZIONALI: togli il commento a quelli che ti servono
#plt.grid(True)
#plt.xscale("Log")
##Questo serve per scegliere range e scansione degli assi
#plt.yticks(np.arange(ymin, ymax, larghezza_tacche))


##Stampa plot e mostralo in console
print_plot(nome)
plt.show()
