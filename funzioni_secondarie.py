# -*- coding: utf-8 -*-
"""
Created on Sat Sep 25 21:40:01 2021

@author: mango
"""
import openpyxl
import scipy.odr
import numpy as np
import os, sys
from matplotlib import pyplot as plt

#SELEZIONE DATI
def fileselect():
    # metodo per selezionare il file più velocemente:
    files = []
    dirlist = os.listdir("./")
    for file in dirlist:
        if file.endswith(".csv") or file.endswith(".xlsx"):
            files.append(file)
            
    # se non ci sono files, termina il programma
    if files == []:
        raise ValueError("Non ci sono dati in questa cartella")
        
    #se il file è uno, assumo che sia quello giusto
    if len(files) == 1:
        return(files[0])
    else:
        #mostra la lista dei files trovati
        i = 1
        for file in files:
            print(str(i) + ". " + str(file))
            i += 1
        
        #richiedi selezione
        selection = int(input("Scegli il file da cui vuoi estrarre i dati: "))
        try:
            nome = files[selection - 1]
        except:
            print("hai scelto un file che non esiste, scemo")
            sys.exit()
            
        #converto il file se è excel
        if nome.endswith(".xlsx"):
            xlsx = openpyxl.load_workbook(nome)
            ## opening the xlsx file
            xlsx = openpyxl.load_workbook(nome)
            ## opening the active sheet
            sheet = xlsx.active
            ## getting the data from the sheet
            data = sheet.rows

            ## creating a csv file
            csv = open("data.csv", "w+")
            
            for row in data:
                l = list(row)
                for i in range(len(l)):
                    if i == len(l) - 1:
                        csv.write(str(l[i].value))
                    else:
                        csv.write(str(l[i].value) + ',')
                    csv.write('\n')
            
            ## close the csv file
            csv.close()
        return(nome)
        

#SALVATAGGIO AD ALTA RISOLUZIONE
def print_plot(filename):
    #cerco il punto, poi cancello l'estensione
    print(filename.rfind("."))
    filename = filename[:filename.rfind(".")]
    #questa parte serve ad evitare la sovrascrizione automatica
    dirlist = os.listdir("./")
    if filename in dirlist:
        input("Il file esiste già. Vuoi sovrascriverlo? [y o invio per confermare]: ")
        if input == "y" or input == "":
            plt.savefig(filename, dpi=1600)
    else:
        plt.savefig(filename, dpi=1600)
        

            
#STAMPA PARAMETRI DI FIT
#In questa funzione, ti aspetti che values ed errors siano LISTE di valori
def print_params(param_values, param_errors):
    print("Parametri del fit:")
    for i in range(len(param_values)):
        print(str(i) + ": \t" + str(param_values[i]) + "±" + str(param_errors[i]))

##FUNZIONE PER FITTING CURVA
#func è il tuo modello, initial_guess la lista con le predizioni sui parametri
def curve_fit(func,initial_guess,data):
    #se non hai impostato un modello o non hai dato guess iniziali, chiudo il programma
    if func == "" or initial_guess == []: 
        raise ValueError("Devi inserire un modello. Controlla riga 14")
    else:
        model=scipy.odr.Model(func)
        
        ##CURVE FITTING
        #sto caricando x, xerr, y, yerr
        mydata= scipy.odr.RealData(data[0],data[1],data[2],data[3])
        fit = scipy.odr.ODR(mydata,model,initial_guess)
        #Fit = minimi quadrati
        scipy.odr.ODR.set_job(fit,fit_type=2)
        output=scipy.odr.ODR.run(fit)
        print_params(output.beta, output.sd_beta)
        
        
        ##PLOT CURVA DI FIT
        x = data[0]
        xFit=np.arange(min(x),max(x),(max(x)-min(x))/1000)
        yFit= func(output.beta, xFit)
        plt.plot(xFit,yFit)