# -*- coding: utf-8 -*-
"""
@author: mango
"""
#Libraries
import scipy.odr
import numpy as np
from matplotlib import pyplot as plt
from funzioni_secondarie import fileselect, print_plot, curve_fit, parameters_text

##SELEZIONE FILE
n_graphs = int(input("Quanti grafici vuoi rappresentare? "))
datasets = []
labels = []
for i in range(n_graphs):
    print("Scegli il dataset" + str(i+1) + ": ")
    file = fileselect()
    datasets.append(file)
    label = input("Cosa rappresenta questo dataset? ")
    labels.append(label)

for i in range(len(datasets)):
    #estraggo i dati dal dataset
    data = np.loadtxt(datasets[i], unpack=True, delimiter = ";", skiprows=1)
    # IMPORTANTISSIMO: QUI SI ASSUME CHE TU STIA CARICANDO IN ORDINE X, ERRX, Y E ERRY
    plt.errorbar(data[0],data[2],xerr=data[1],yerr=data[3],fmt ="o", ecolor="black", barsabove=False, ms= 1, label = labels[i])

    
plt.legend()

##DEFINIZIONE ETICHETTE
plt.title("Grafico")
plt.xlabel("Asse x [udm]")
plt.ylabel("Asse y [udm]")


##PARAMETRI OPZIONALI: togli il commento a quelli che ti servono
#plt.grid(True)
#plt.xscale("Log")


##Stampa plot e mostralo in console
print_plot(datasets[0])
plt.show()
