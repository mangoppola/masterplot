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
        if file.lower().endswith(".csv") or file.lower().endswith(".xlsx"):
            files.append(file)
            
    # se non ci sono files, termina il programma
    if files == []:
        raise ValueError("Non ci sono dati in questa cartella")
        
    #se il file è uno, assumo che sia quello giusto
    if len(files) == 1:
        nome = files[0]
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
        ## opening the xlsx file
        xlsx = openpyxl.load_workbook(nome)
        ## opening the active sheet
        sheet = xlsx.active
        ## getting the data from the sheet
        data = sheet.rows

        ## individuo il nome file
        #Tolgo l'estensione
        nome_file = str(nome)[:str(nome).rfind(".")]

        #controllo che non ci sia già un file csv con lo stesso nome, così non sovrascrivo niente
        i=0
        while os.path.exists(f"{nome_file}{i}.csv"):
            i += 1
        #Ho trovato il nuovo nome del file
        nome = f"{nome_file}{i}.csv"

        ## creating a csv file
        csv = open(nome, "w+")

        for row in data:
            l = list(row)
            for i in range(len(l)):
                if i == len(l) - 1:
                    csv.write(str(l[i].value))
                    csv.write('\n')
                else:
                    csv.write(str(l[i].value) + ';')

        ## close the csv file
        csv.close()
    return(nome)
        

#SALVATAGGIO AD ALTA RISOLUZIONE
def print_plot(filename, extension = "png"):
    #cerco il punto, poi cancello l'estensione
    filename = filename[:filename.rfind(".")]
    #questa parte serve ad evitare la sovrascrizione automatica
    dirlist = os.listdir("./")
    if (filename + "." + extension) in dirlist:
        choice = input("Il file esiste già. Vuoi sovrascriverlo? [y o invio per confermare]: ")
        if choice == "y" or choice == "":
            plt.savefig(filename + "." + extension, dpi=1600)
    else:
        plt.savefig(filename + "." + extension, dpi=1600)
        

            
#RESTITUISCE LA STRINGA CON TUTTI I PARAMETRI (eventualmente, la stampa a schermo)
# @names è una lista di nomi per le variabili che stai fittando. Normalmente, vengono dati come nomi i numeri interi
# @decimal_places è il numero di cifre decimali che desideri nel tuo output
# @math_mode serve a dare gli apici con garbo. Disabilitare se succedono cose strane
# @notab serve a sostituire la tabulazione con un dato numero di spazi. Impostalo a true se vuoi usarlo nel grafico perchè a matplotlib non piace il \t
# @print_text serve a stampare il testo in console
def parameters_text(param_values, param_errors, names = list(range(len(sys.argv[0]))), decimal_places = 3, math_mode = True, notab = False, print_text = True):
    # legible_text contiene i dati in forma di lista, ben formattati per essere stampati in console
    legible_text = ""
    # formatted_text contiene il testo formattato in LaTeX
    formatted_text = ""
    # formatted parameters contiene una lista dei parametri formattati in LaTeX
    formatted_parameters = []
    # legible_parameters contiene una lista di parametri in formato leggibile, da stampare in console
    legible_parameters = []
    for i in range(len(param_values)):
        #Questa variabile contiene i dati grezzi, espressi come dato e+exp1 ± errore e+exp2 (ovviamente senza spazi)
        raw_data = str("{:.2e}".format(param_values[i])) + "±" + str("{:.2e}".format(param_errors[i]))
        
        if math_mode:
            math_text = raw_data
            #individuo i due esponenti e li rimpiazzo con ^{exp}. Aggiungo i dollari per passare a math mode
            exp1 = math_text[math_text.find("e"):math_text.find("±")]
            exp2 = math_text[raw_data.rfind("e"):]
            math_text = math_text.replace (exp1, "\cdot 10^{" + exp1[1:] + "}")
            math_text = math_text.replace(exp2, "\cdot 10^{" + exp2[1:] + "}")
            math_text = "$" + math_text + "$"
            formatted_parameters.append(math_text)
              
        legible_parameters.append(raw_data)
        if notab:
            legible_text += (str(names[i]) + ": " + legible_parameters[i])
            if math_mode:
                formatted_text += (str(names[i]) + ": " + formatted_parameters[i])
        else:
            legible_text += (str(names[i]) + ": \t" + legible_parameters[i])
            if math_mode:
                formatted_text += (str(names[i]) + ": \t" + formatted_parameters[i])

        #se non sono arrivato all'ultimo elemento, passo alla prossima riga
        if i != (len(param_values) - 1):
            formatted_text += "\n"
            legible_text += "\n"

    if print_text:
        print("Parametri del fit:")
        print (legible_text)
    if math_mode:
        return (formatted_text)
    else:
        return(legible_text)

##FUNZIONE PER FITTING CURVA
#func è il tuo modello, initial_guess la lista con le predizioni sui parametri
def curve_fit(func,initial_guess,data, label = ""):
    #se non hai impostato un modello o non hai dato guess iniziali, chiudo il programma
    if func == "" or initial_guess == []: 
        raise ValueError("Devi inserire un modello. Controlla riga 14")
    else:
        model=scipy.odr.Model(func)
        
        ##CURVE FITTING
        #sto caricando x, y, xerr, yerr
        mydata= scipy.odr.RealData(data[0],data[1],data[2],data[3])
        fit = scipy.odr.ODR(mydata,model,initial_guess)
        #Fit = minimi quadrati
        scipy.odr.ODR.set_job(fit,fit_type=2)
        output=scipy.odr.ODR.run(fit)
        parameters_text(output.beta, output.sd_beta, print_text = True)
        
        
        ##PLOT CURVA DI FIT
        x = data[0]
        xFit=np.arange(min(x),max(x),(max(x)-min(x))/1000)
        yFit= func(output.beta, xFit)
        plt.plot(xFit,yFit, label = label)
    return(output.beta,output.sd_beta)
