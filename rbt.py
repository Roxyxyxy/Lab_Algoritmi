# rbt.py - Albero Rosso-Nero (Red-Black Tree)
# L'Albero Rosso-Nero è un altro tipo di Albero Binario di
# Ricerca BILANCIATO. Invece di usare le altezze come l'AVL,
# usa una colorazione dei nodi (ROSSO o NERO) per garantire
# che l'albero non diventi mai troppo sbilanciato.
#
# LE 4 REGOLE FONDAMENTALI dell'Albero Rosso-Nero:
#   1. Ogni nodo è ROSSO o NERO.
#   2. La RADICE è sempre NERA.
#   3. Un nodo ROSSO non può avere figli ROSSI
#      (non ci possono essere due rossi di fila).
#   4. Ogni percorso dalla radice a una foglia vuota (None)
#      deve attraversare lo STESSO numero di nodi NERI.
#      (questa si chiama "black-height" o altezza nera)
#
# Quando inseriamo un nodo, potremmo violare queste regole.
# Il metodo "_sistema_inserimento" le ripristina.

# Costanti per i colori (usiamo stringhe semplici)
ROSSO = "ROSSO"
NERO  = "NERO"


class NodoRBT:
# Ha l'attributo "colore" (ROSSO o NERO)
# Ha l'attributo "padre" per risalire l'albero (necessario durante il bilanciamento)

    def __init__(self, valore):
        # Il valore memorizzato nel nodo
        self.valore = valore
        self.sinistro = None
        self.destro = None
        # Puntatore al nodo padre (necessario per risalire)
        self.padre = None
        # Ogni nuovo nodo inizia ROSSO (è la regola standard)
        self.colore = ROSSO


class RossoNero:

    def __init__(self):
        self.radice = None

    # Rotazione a sinistra attorno al nodo x.
    # Rispetto all'AVL, qui dobbiamo anche aggiornare
    # i puntatori "padre" di tutti i nodi coinvolti.
    #
    # Prima:          Dopo:
    #     x               y
    #    / \             / \
    #   A   y    -->    x   C
    #      / \         / \
    #     B   C       A   B

    def _ruota_sinistra(self, x):
        # y è il figlio destro di x, salirà al posto di x
        y = x.destro
        # B è il figlio sinistro di y, cambierà posto
        B = y.sinistro

        # Aggiornamento dei collegamenti

        # y sale: prende il padre di x come suo padre
        y.padre = x.padre

        # Aggiorniamo il padre di x per puntare a y invece di x
        if x.padre is None:
            # x era la radice, ora y diventa la nuova radice
            self.radice = y
        elif x == x.padre.sinistro:
            # x era figlio sinistro del padre, ora ci va y
            x.padre.sinistro = y
        else:
            # x era figlio destro del padre, ora ci va y
            x.padre.destro = y

        # x scende a sinistra di y
        y.sinistro = x
        x.padre = y

        # B (il vecchio figlio sinistro di y) va a destra di x
        x.destro = B
        if B is not None:
            # B deve sapere che ora il suo padre è x
            B.padre = x

    # Rotazione a destra attorno al nodo y.
    # Simmetrica a _ruota_sinistra.
    #
    # Prima:          Dopo:
    #       y               x
    #      / \             / \
    #     x   C    -->    A   y
    #    / \                 / \
    #   A   B               B   C
    
    def _ruota_destra(self, y):
        # x è il figlio sinistro di y, salirà al posto di y
        x = y.sinistro
        # B è il figlio destro di x, cambierà posto
        B = x.destro

        # Aggiornamento dei collegamenti

        # x sale: prende il padre di y come suo padre
        x.padre = y.padre

        # Aggiorniamo il padre di y per puntare a x invece di y
        if y.padre is None:
            # y era la radice, ora x diventa la nuova radice
            self.radice = x
        elif y == y.padre.sinistro:
            # y era figlio sinistro del padre, ora ci va x
            y.padre.sinistro = x
        else:
            # y era figlio destro del padre, ora ci va x
            y.padre.destro = x

        # y scende a destra di x
        x.destro = y
        y.padre = x

        # B (il vecchio figlio destro di x) va a sinistra di y
        y.sinistro = B
        if B is not None:
            # B deve sapere che ora il suo padre è y
            B.padre = y


    # L'inserimento avviene in due fasi:
    #   FASE 1: Inserimento (come ABR), impostando correttamente i puntatori padre.
    #   FASE 2: Chiamata a _sistema_inserimento per ripristinare le regole Rosso-Nere.

    def inserisci(self, valore):

        # Creiamo il nuovo nodo (parte come ROSSO per default)
        nuovo = NodoRBT(valore)

        # Inserimento 

        # Se l'albero è vuoto, il nuovo nodo è la radice
        if self.radice is None:
            self.radice = nuovo
            # La radice deve essere NERA (Regola 2)
            self.radice.colore = NERO
            return

        # Troviamo la posizione giusta scorrendo l'albero
        nodo_corrente = self.radice
        nodo_padre    = None

        while nodo_corrente is not None:
            nodo_padre = nodo_corrente
            if nuovo.valore < nodo_corrente.valore:
                nodo_corrente = nodo_corrente.sinistro
            elif nuovo.valore > nodo_corrente.valore:
                nodo_corrente = nodo_corrente.destro
            else:
                # Valore duplicato: non inseriamo nulla
                return

        # Colleghiamo il nuovo nodo al padre trovato
        nuovo.padre = nodo_padre
        if nuovo.valore < nodo_padre.valore:
            nodo_padre.sinistro = nuovo
        else:
            nodo_padre.destro = nuovo

        # Ripristino delle regole Rosso-Nere
        self._sistema_inserimento(nuovo)


    # Questo metodo ripristina le regole dell'albero Rosso-Nero dopo un inserimento. 
    # Usa un ciclo while che sale verso la radice finché non trova e risolve le violazioni.
    # Violazione possibile: "doppio rosso" (un nodo rosso ha un padre rosso )
    # Esistono 3 casi principali:
    #   CASO 1: Lo ZIO del nodo è ROSSO 
    #       -Ricolorazione: padre e zio diventano NERI, nonno diventa ROSSO. Poi risaliamo.
    #   CASO 2: Lo ZIO è NERO e il nodo forma una "CURVA"
    #       -Rotazione per raddrizzare la curva, poi si ricade nel Caso 3.
    #   CASO 3: Lo ZIO è NERO e il nodo forma una "LINEA"
    #       -Rotazione sul nonno e scambio di colori.

    def _sistema_inserimento(self, nodo):

        # Continuiamo finché il padre del nodo è ROSSO
        # (cioè finché esiste una violazione "doppio rosso")
        while nodo.padre is not None and nodo.padre.colore == ROSSO:

            # Recuperiamo il padre e il nonno del nodo
            padre  = nodo.padre
            nonno  = padre.padre

            # Se non c'è nonno, non possiamo continuare 
            if nonno is None:
                break

            # Situazione in cui il padre è figlio sinistro del nonno
            if padre == nonno.sinistro:

                # Lo zio è il figlio destro del nonno
                zio = nonno.destro

                # Caso in cui lo zio è ROSSO
               
                if zio is not None and zio.colore == ROSSO:
                    padre.colore  = NERO
                    zio.colore    = NERO
                    nonno.colore  = ROSSO
                    # Risaliamo al nonno per verificare se ci sono altre violazioni
                    nodo = nonno

                else:
                    # Caso in cui lo zio è NERO, il nodo è figlio DESTRO (forma una "curva": sinistra poi destra)
                    if nodo == padre.destro:
                        # Dopo la rotazione, padre scende e nodo sale
                        nodo = padre
                        self._ruota_sinistra(nodo)
                        # Aggiorniamo padre dopo la rotazione
                        padre = nodo.padre

                    # CASO in cui lo zio è NERO, il nodo è figlio SINISTRO (forma una "linea" dritta: sinistra-sinistra)
                    # Soluzione: ricolorazione e rotazione destra sul nonno
                    padre.colore = NERO
                    nonno.colore = ROSSO
                    self._ruota_destra(nonno)

            # Situazione in cui il padre è figlio DESTRO del nonno
            else:

                # Lo zio è il figlio SINISTRO del nonno
                zio = nonno.sinistro

                # CASO in cui lo zio è ROSSO
                if zio is not None and zio.colore == ROSSO:
                    padre.colore  = NERO
                    zio.colore    = NERO
                    nonno.colore  = ROSSO
                    nodo = nonno

                else:
                    # CASO in cui lo zio è NERO, il nodo è figlio SINISTRO (forma una "curva": destra poi sinistra)
                    # Soluzione: ruotiamo a destra sul padre
                    if nodo == padre.sinistro:
                        nodo = padre
                        self._ruota_destra(nodo)
                        padre = nodo.padre

                    # CASO 3B: Lo zio è NERO, il nodo è figlio DESTRO (forma una "linea" dritta: destra-destra)
                    # Soluzione: ricolorazione e rotazione sinistra sul nonno
                    padre.colore = NERO
                    nonno.colore = ROSSO
                    self._ruota_sinistra(nonno)

        # Regola 2: la radice deve essere SEMPRE NERA. La forziamo nera alla fine di ogni sistemazione.
        self.radice.colore = NERO

  
    def cerca(self, valore):
        return self._cerca_ricorsivo(self.radice, valore)


    def _cerca_ricorsivo(self, nodo, valore):

        if nodo is None:
            return False

        if valore == nodo.valore:
            return True

        if valore < nodo.valore:
            return self._cerca_ricorsivo(nodo.sinistro, valore)

        else:
            return self._cerca_ricorsivo(nodo.destro, valore)


    def altezza(self):
        return self._altezza_ricorsiva(self.radice)

    
    def _altezza_ricorsiva(self, nodo):

        if nodo is None:
            return 0

        altezza_sinistra = self._altezza_ricorsiva(nodo.sinistro)
        altezza_destra   = self._altezza_ricorsiva(nodo.destro)

        # Altezza = 1 + il massimo tra le due
        if altezza_sinistra > altezza_destra:
            return 1 + altezza_sinistra
        else:
            return 1 + altezza_destra
