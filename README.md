# masterplot
Easy scientific data plotting and fitting

I files
===========

Funzioni secondarie
--------
Questo file contiene tutte le funzioni che non dovrebbero essere modificate quando si vuole fare un plot. Di regola, queste funzioni vanno modificate *unicamente* nel caso in cui qualcosa non funzioni.
La ragione per cui queste funzioni non sono incluse nei files principali è per rendere più snello il corpo dei programmi principali e renderli più intuitivi e facili da leggere. In questo modo, in fase di plotting, sono subito visibili gli elementi importanti da modificare, quali, ad esempio, initial guess o eventuali opzioni per il grafico
Le funzioni incluse in questa libreria sono
* fileselect: serve ad individuare file excel o csv da cui caricare i dati. Mostra un semplice menu da cui scegliere il giusto file, a meno che non venga individuato un unico csv; in tal caso, il programma assume che quello sia quello corretto e procede al caricamento dei dati
* print_plot: stampa una versione ad alta risoluzione del grafico ottenuto. Di default, il programma sceglie di salvare il grafico come png, perché é piú facile da maneggiare; in alternativa, é possibile salvarlo come svg
* parameters_text: stampa i parametri del fit nella console di Python. É possibile dare come argomento i nomi dei parametri e il numero di cifre decimali desiderate
* curve_fit: esegue il fit con il metodo dei minimi quadrati. Nella pratica, questa funzione si occupa di calcolare i parametri del fit e di aggiungere il fit al grafico.

Plot
----
Questo file è quello che va utilizzato per creare e stampare un unico plot. Carica il file di dati e inizializza il grafico. Segue una sezione da utilizzare solo nel caso in cui serva fare un fit: *qui bisogna inserire la funzione da fittare e l'initial guess*. In questo file bisogna definire titolo del grafico e degli assi, nonchè eventuali parametri aggiuntivi (i.e. griglia, scala degli assi, range e scansione degli assi, etc.). Infine, il plot viene salvato e mostrato nella console
**Nota utile**: é possibile usare esponenti e pedici nelle etichette dei grafici. Ad esempio, per digitare correttamente x²³, serve scrivere $x^{23}$; se scrivere I con pedice DS, devi scrivere $I_{DS}$

Multiplot
----
Amplia quello che fa Plot ad un numero arbitrario di files (ovviamente, almeno per ora, non supporta il fitting). 

Utilizzo
=======
+ Apri spyder oppure apri una finestra di terminale (prompt dei comandi) e digita ``python``
+ Se vuoi generare un unico plot, utilizza ``plot.py``; se ne vuoi generare diversi su uno stessa immagine, usa ``multiplot.py``
+ Se hai bisogno di fare un fit, assicurati di modificare la sezione *Curve fitting*. Imposta la funzione che vuoi usare per il fit e di dare una initial guess
+ Controlla la sezione in fondo per eventuali opzioni aggiuntive che desideri
+ Avvia il programma e segui le istruzioni

