# REMSENS
Intro
REMOTING SERVER - Remsens

Remoting Server è un sistema general purpose di gestione, controllo e visualizzazione dati di sensori
attraverso un protocollo di alto livello basato su AMON.
In particolare il server si occupa di ricevere i dati di più client, memorizzarli in un database, consentire il controllo e la loro visualizzazione, nonché la gestione delle varie configurazioni di campionamento e invio.
C'è inoltre la possibilità di disabilitare i sensori da remoto.

************ HOWTO veloce ************

pacchetti necessari:
apt-get install python-setuptools python-dev python-pip libxslt1-dev libzmq-dev sqlite3 libsqlite3-dev libxml2-dev build-essential

installiamo virtualenv:
pip install virtualenv

creiamo un virtual environment:
virtualenv ~/remsens/djanni

facciamo partire virtualenv:
source ~/remsens/djanni/bin/activate

installiamo django e i bindings zmq (dal virtualenv):
pip install django==1.8 pyzmq

ora si possono avviare le app, entrambe da virtualenv nelal directory remsens:
python manage.py runserver per il web server
python serv2/main_serv.py

se main_serv2.py non parte aggiorniamo il $PYTHONPATH:
export PYTHONPATH="$PYTHONPATH:$HOME/remsens"

*********** fine HOWTO veloce ************

Per poter usare il sistema è necessario, allo stato attuale, installare Python 2.7 (o 3.0) insieme al framework di sviluppo web Django, che altro non è che un set di librerie Python.

Dopo di ché bisogna assicurarsi che siano presenti tutte le librerie suddette nello stesso PATH di Python, per questo può essere di aiuto usare virtualenv o fare link simbolici alla directory. Prestare attenzione anche alla scelta del PATH in PyDev. Una volta installato Django, configurato il PATH in PyDev e importato il progetto in Eclipse sempre con PyDev, si visualizzano dentro la directory src altre directory con nomi del tipo alpha, serv2 e server.
Alpha è il nome del progetto generale, server è il nome (e la directory dei file) dell'applicazione interna di Django che è quella parte del server che costituisce la parte web del sistema.
Mentre serv2 è la directory del server ad-hoc per la comunicazione con i singoli meteringPoint (d'ora in poi Client).

Per far partire tutta la baracca bisogna avviare il server django come da documentazione (via terminale con "python manage.py runserver" oppure da pydev in eclipse) e parte il server web, a cui possiamo accedere in locale sulla porta 8080 (è tutto presente e configurabile come da documentazione).
Mentre per far partire il server responsabile della comunicazione vera e propria con i client e conseguentemente coi singoli device (sensori d'ora in poi), bisogna avviare lo script "main_serv.py".
Adesso ci troviamo con due terminali in cui uno visualizza le richieste su http e l'altro visualizza i dati di comunicazione che mano a mano processa e vari avvisi in caso di eccezioni.

Possiamo adesso accedere all'account amministratore admin:remsens via localhost:8080/admin e da lì controlliamo tutto il modello del database.

Da questa interfaccia accessibile solo all'admin, possiamo creare una nuova entita (d'ora in poi Organizzazione) che
rappresenta l'ente generale che accomuna gli utenti e i loro client/sensori.
Possiamo, dunque, generare nuovi utenti registrandoli attraverso l'interfaccia web (oppure tutto da admin) e assegnare la loro appartenenza ad una Organizzazione di quelle presenti.
Il nuovo utente non è, però, ancora attivo e va abilitato dall'interfaccia admin (si vuole esser certi che appartenga a quella Organizzazione :) ). Una volta abilitato, l'utente visualizza tutti i Client associati all'Organizzazione dalla home page e i rispettivi Sensori. Naturalmente al primo avvio non ce ne sono ancora, quindi procediamo a crearne uno.

Per associare un nuovo Client dobbiamo avere effettivamente un Client, o almeno il programma Client. Bisogna dunque avviare il Client che come primo avvio richiederà un'associazione da effettuare in locale sulla porta 80.
Bisogna indicare un nome abbastanza significativo, l'indirizzo IP del server e le tre porte, una di ricezione di misure, una per le configurazioni di Sensori e una per le nuove richieste.

Una volta mandata la richiesta, bisogna andare sull'interfaccia web del server (Django) e dall'account dell'utente creato cliccare su Add New Client, dove ci sarà un menù a scelta per le richieste pendenti (è utile in questo caso controllare il pin numerico visualizzato dopo l'associazione del Client per esserne sicuri).

Adesso abbiamo un Client fresco di UUID a cui però dobbiamo aggiungere dei Sensori che misurino qualcosa.
Nel frattempo il Client comincerà a inviare incessanti richieste di configurazione al server, il quale ne farà vedere la ricezione sul terminale.

Dobbiamo adesso creare dei Sensori per il nostro nuovo Client. Sulla raspberry bisognerebbe installare tutto il necessario affinché il programma Remoting client riconosca il sensore e gli associ un protocollo di comunicazione (modbus solitamente, ma nel nostro caso virtuale è predisposto il protocollo random che produce dei valori casuali per uno o più sensori virtuali).

Una volta che si ha installato il sensore possiamo definirne un corrispettivo virtuale cliccando dalla home sul nome del Client a cui vogliamo associarlo. Da lì clicchiamo Add New Sensor e possiamo immettere tutti i dati necessari (segnati con asterisco) per la corretta configurazione del Sensore. Per i dettagli specifici sui tipi di valori possibili consultare la "documentazione di protocollo" (protocol.txt in miceli). Le opzioni vincolanti comunque, sono nei menù a scelta oppure non viene consentito il salvataggio del nuovo Sensore se mancano campi obbligatori.

Prestare attenzione al campo "Protocol name" che definisce il protocollo per la misurazione sul Client (da qui "random", di cui prima).

Una volta salvata la configurazione è tutto pronto, e se non ci sono errori, il Remoticng client creaerà una nuova configurazione e comincerà ad inviare le misure (fittizie nel nostro caso).

Per visualizzare tali misure basta cliccare nella pagina sul nome del(i) Sensore(i) oppure sul nome del Client per visualizzare le ultime misure di ciascun Sensore in forma compatta.

Per visualizzare in forma grafica le misure basta andare sulla pagina del Client (dalla home ad esempio) e cliccare "Show graph". Si potranno ceccare i box nella nuova pagina per visualizzare i grafici dei singoli sensori.

È possibile cancellare alcune misure, basta andare nella pagine del Sensore (sempre con lo stesso percorso: Home -> Client -> Sensore) e selezionare quelle che si vogliono cancellare e confermare con Delete Measures.

È possibile riconfigurare in qualsiasi momento ogni sensore, basta andare alla pagina del Sensore, come prima.
Per cancellare il sensore dal proprio Client (e dal database) bisogna andare nella configurazione alla pagina del Sensore e nella parte relativa alla configurazione scegliere il Command "Delete", così l'applicazione locale Remoting client cancellerà tale sensore anche in locale.

È sempre possibile, modificare, cancellare e filtrare qualsiasi oggetto del database (misure, sensori, client, richieste e utenti) dal pannello di amministrazione.

Thanks to Python and Guido van Rossum Benevolent Dictator For Life

#####author#####

CC BY 3.0 IT
Pavlo Burda - www.koelio.net - 20/10/2015
