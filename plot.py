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
nome = fileselect()

# INIZIALIZZAZIONE GRAFICO
# @ecolor colore barre di errore, @fmt forma punti, @barsabove metti a True se non si vede l'errore @ms: dimensione punti sperimentali
x, xerror, y, yerror = np.loadtxt(nome, unpack=True, delimiter=";", skiprows=1)
plt.errorbar(x, y, xerr=xerror, yerr=yerror, fmt="o", ecolor="black",
             barsabove=False, ms=0.5, label="Dati Sperimentali")

##MODIFICARE SE VUOI UN FIT
#@label in curve_fit: aggiornare per inserire una etichetta al fit da mostrare in legenda.
#esempio di modello: beta[0]+beta[1]*np.cos(x**2)
def model(beta,x):
    return beta[0]*np.cos(beta[1]*x+beta[2])
#qui metti una lista con i parametri
initial_guess = [0,0,0]
selection = input("Hai bisogno di fare un fit? [y o invio per confermare]: ")
if selection == "y" or selection == "":
    data = [x,y,xerror,yerror]
    fit_parameters = curve_fit(model, initial_guess, data, label = "")
    
    # aggiungo i parametri del fit come testo
    # modificare names per mettere i giusti nomi dei parametri del fit
    # decimal places serve a dare il numero di cifre decimali
    text = parameters_text(fit_parameters[0], fit_parameters[1],
                           names=("beta0", "beta1", "beta2"), decimal_places = 3,
                           notab=True, print_text=False)
    
    #disegno il testo su schermo. @xy imposta l'angolo dove mettere il testo. 0 e 1 rappresentano gli estremi degli assi, con (0,0) in basso a sinistra e (1,1) in alto a destra
    #@xytext serve a spostare la casella di tot punti rispetto al punto selezionato. Regolare per spostare la casella attorno ad un angolo
    plt.gca().annotate(text, xy=(0,1), xytext=(15,-30), fontsize = 10,
                     xycoords='axes fraction', textcoords='offset points',
                     bbox=dict(facecolor='none', edgecolor = "black"),
                     horizontalalignment = "left", verticalalignment ="bottom")
    
##DEFINIZIONE ETICHETTE
plt.title("Grafico")
plt.xlabel("Asse x [udm]")
plt.ylabel("Asse y [udm]")


##PARAMETRI OPZIONALI: togli il commento a quelli che ti servono
#plt.grid(True)
#plt.xscale("Log")
##Questo serve per scegliere range e scansione degli assi
#plt.yticks(np.arange(ymin, ymax, larghezza_tacche))
##Togli il commento per aggiungere la legenda
#plt.legend()

##Stampa plot e mostralo in console
print_plot(nome, extension = "png")
plt.show()
