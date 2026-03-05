# =============================================================
# avl.py - Albero AVL (Adelson-Velsky e Landis)
# =============================================================
# L'albero AVL è un Albero Binario di Ricerca BILANCIATO.
# La differenza rispetto all'ABR normale è che l'AVL si
# "aggiusta" automaticamente dopo ogni inserimento per
# garantire che l'altezza resti sempre logaritmica.
#
# CONCETTO CHIAVE - Fattore di Bilanciamento:
#   fattore = altezza(sottoalbero_sinistro) - altezza(sottoalbero_destro)
#
#   Se il fattore è  0, +1 o -1 -> il nodo è BILANCIATO (ok)
#   Se il fattore è +2            -> troppo pesante a SINISTRA
#   Se il fattore è -2            -> troppo pesante a DESTRA
#
# Quando un nodo è sbilanciato, si eseguono le ROTAZIONI
# per riportare l'albero in equilibrio.
# =============================================================


# -------------------------------------------------------------
# CLASSE: NodoAVL
# -------------------------------------------------------------
# Come NodoABR, ma con un attributo in più: "altezza".
# L'altezza di un nodo è la distanza dal nodo alla foglia
# più lontana sotto di lui.
# Un nodo appena creato (senza figli) ha altezza 1.
# -------------------------------------------------------------
class NodoAVL:

    def __init__(self, valore):
        # Il valore memorizzato nel nodo
        self.valore = valore
        # Figlio sinistro: inizialmente vuoto
        self.sinistro = None
        # Figlio destro: inizialmente vuoto
        self.destro = None
        # Altezza del nodo: un nodo foglia parte da 1
        self.altezza = 1


# -------------------------------------------------------------
# CLASSE: AVL
# -------------------------------------------------------------
# L'albero AVL vero e proprio.
# Contiene la radice e tutti i metodi per inserire,
# cercare e bilanciare l'albero.
# -------------------------------------------------------------
class AVL:

    def __init__(self):
        # All'inizio l'albero è vuoto
        self.radice = None

    # ---------------------------------------------------------
    # METODO PRIVATO: _get_altezza(nodo)
    # ---------------------------------------------------------
    # Restituisce l'altezza di un nodo.
    # Se il nodo è None (vuoto), l'altezza è 0.
    # Questo metodo ci evita di controllare "if nodo is None"
    # ogni volta che vogliamo l'altezza.
    # ---------------------------------------------------------
    def _get_altezza(self, nodo):
        if nodo is None:
            return 0
        return nodo.altezza

    # ---------------------------------------------------------
    # METODO PRIVATO: _get_bilanciamento(nodo)
    # ---------------------------------------------------------
    # Calcola il fattore di bilanciamento di un nodo.
    # Formula: altezza_sinistra - altezza_destra
    #
    # Risultato positivo -> il sottoalbero sinistro è più alto
    # Risultato negativo -> il sottoalbero destro è più alto
    # Risultato zero     -> perfettamente bilanciato
    # ---------------------------------------------------------
    def _get_bilanciamento(self, nodo):
        if nodo is None:
            return 0
        altezza_sinistra = self._get_altezza(nodo.sinistro)
        altezza_destra = self._get_altezza(nodo.destro)
        return altezza_sinistra - altezza_destra

    # ---------------------------------------------------------
    # METODO PRIVATO: _aggiorna_altezza(nodo)
    # ---------------------------------------------------------
    # Ricalcola e aggiorna l'altezza di un nodo.
    # L'altezza è 1 + il massimo tra le altezze dei due figli.
    # Questo va chiamato ogni volta che modifichiamo l'albero.
    # ---------------------------------------------------------
    def _aggiorna_altezza(self, nodo):
        altezza_sinistra = self._get_altezza(nodo.sinistro)
        altezza_destra = self._get_altezza(nodo.destro)
        if altezza_sinistra > altezza_destra:
            nodo.altezza = 1 + altezza_sinistra
        else:
            nodo.altezza = 1 + altezza_destra

    # ---------------------------------------------------------
    # METODO PRIVATO: _ruota_destra(y)
    # ---------------------------------------------------------
    # Esegue una ROTAZIONE A DESTRA attorno al nodo "y".
    # Si usa quando il sottoalbero SINISTRO è troppo pesante.
    #
    # Prima della rotazione:       Dopo la rotazione:
    #
    #       y                           x
    #      / \                         / \
    #     x   C          -->          A   y
    #    / \                             / \
    #   A   B                           B   C
    #
    # "x" sale al posto di "y", e "y" scende a destra di "x".
    # Il sottoalbero "B" (figlio destro di x) diventa
    # il figlio sinistro di y.
    #
    # Restituisce il nuovo nodo radice del sottoalbero (cioè x).
    # ---------------------------------------------------------
    def _ruota_destra(self, y):
        # x è il figlio sinistro di y, salirà al posto di y
        x = y.sinistro
        # B è il figlio destro di x, cambierà posto
        B = x.destro

        # Eseguiamo la rotazione:
        # x sale e prende y come figlio destro
        x.destro = y
        # y scende e prende B come figlio sinistro
        y.sinistro = B

        # IMPORTANTE: aggiorniamo le altezze
        # Prima aggiorniamo y (ora è più in basso), poi x (ora è più in alto)
        self._aggiorna_altezza(y)
        self._aggiorna_altezza(x)

        # x è il nuovo "capo" di questo sottoalbero
        return x

    # ---------------------------------------------------------
    # METODO PRIVATO: _ruota_sinistra(x)
    # ---------------------------------------------------------
    # Esegue una ROTAZIONE A SINISTRA attorno al nodo "x".
    # Si usa quando il sottoalbero DESTRO è troppo pesante.
    #
    # Prima della rotazione:       Dopo la rotazione:
    #
    #     x                               y
    #    / \                             / \
    #   A   y              -->          x   C
    #      / \                         / \
    #     B   C                       A   B
    #
    # "y" sale al posto di "x", e "x" scende a sinistra di "y".
    # Il sottoalbero "B" (figlio sinistro di y) diventa
    # il figlio destro di x.
    #
    # Restituisce il nuovo nodo radice del sottoalbero (cioè y).
    # ---------------------------------------------------------
    def _ruota_sinistra(self, x):
        # y è il figlio destro di x, salirà al posto di x
        y = x.destro
        # B è il figlio sinistro di y, cambierà posto
        B = y.sinistro

        # Eseguiamo la rotazione:
        # y sale e prende x come figlio sinistro
        y.sinistro = x
        # x scende e prende B come figlio destro
        x.destro = B

        # IMPORTANTE: aggiorniamo le altezze
        # Prima aggiorniamo x (ora è più in basso), poi y (ora è più in alto)
        self._aggiorna_altezza(x)
        self._aggiorna_altezza(y)

        # y è il nuovo "capo" di questo sottoalbero
        return y

    # ---------------------------------------------------------
    # METODO: inserisci(valore)
    # ---------------------------------------------------------
    # Aggiunge un valore nell'albero AVL.
    # Chiama il metodo ricorsivo e aggiorna la radice
    # (che potrebbe cambiare dopo una rotazione).
    # ---------------------------------------------------------
    def inserisci(self, valore):
        # Il metodo ricorsivo restituisce sempre la (nuova) radice
        # del sottoalbero su cui ha lavorato
        self.radice = self._inserisci_ricorsivo(self.radice, valore)

    # ---------------------------------------------------------
    # METODO PRIVATO: _inserisci_ricorsivo(nodo, valore)
    # ---------------------------------------------------------
    # Questo è il cuore dell'albero AVL.
    # Fa tre cose:
    #   1. Inserisce il nodo come in un ABR normale
    #   2. Aggiorna l'altezza del nodo corrente
    #   3. Controlla il bilanciamento e, se necessario, ruota
    #
    # I 4 CASI DI SBILANCIAMENTO:
    #   - Caso Sinistra-Sinistra (SS): ruotazione destra semplice
    #   - Caso Destra-Destra (DD):     rotazione sinistra semplice
    #   - Caso Sinistra-Destra (SD):   prima sinistra, poi destra
    #   - Caso Destra-Sinistra (DS):   prima destra, poi sinistra
    # ---------------------------------------------------------
    def _inserisci_ricorsivo(self, nodo, valore):

        # --- PASSO 1: INSERIMENTO NORMALE (come in ABR) ---

        # Caso base: siamo arrivati in un posto vuoto, creiamo il nodo
        if nodo is None:
            return NodoAVL(valore)

        # Il valore è minore: scendiamo a sinistra
        if valore < nodo.valore:
            nodo.sinistro = self._inserisci_ricorsivo(nodo.sinistro, valore)
        # Il valore è maggiore: scendiamo a destra
        elif valore > nodo.valore:
            nodo.destro = self._inserisci_ricorsivo(nodo.destro, valore)
        # Il valore è già presente: non inseriamo duplicati
        else:
            return nodo

        # --- PASSO 2: AGGIORNAMENTO DELL'ALTEZZA ---
        # Ora che abbiamo inserito il nodo figlio, l'altezza
        # del nodo corrente potrebbe essere cambiata
        self._aggiorna_altezza(nodo)

        # --- PASSO 3: CONTROLLO DEL BILANCIAMENTO ---
        # Calcoliamo il fattore di bilanciamento del nodo corrente
        fattore = self._get_bilanciamento(nodo)

        # ==================================================
        # CASO 1: Sinistra-Sinistra (fattore > 1 e valore
        # inserito nel sottoalbero sinistro-sinistro)
        # -> Basta una ROTAZIONE DESTRA
        # ==================================================
        if fattore > 1 and valore < nodo.sinistro.valore:
            return self._ruota_destra(nodo)

        # ==================================================
        # CASO 2: Destra-Destra (fattore < -1 e valore
        # inserito nel sottoalbero destro-destro)
        # -> Basta una ROTAZIONE SINISTRA
        # ==================================================
        if fattore < -1 and valore > nodo.destro.valore:
            return self._ruota_sinistra(nodo)

        # ==================================================
        # CASO 3: Sinistra-Destra (fattore > 1 e valore
        # inserito nel sottoalbero sinistro-destro)
        # -> Prima ruotiamo a SINISTRA il figlio sinistro,
        #    poi ruotiamo a DESTRA il nodo corrente
        # ==================================================
        if fattore > 1 and valore > nodo.sinistro.valore:
            nodo.sinistro = self._ruota_sinistra(nodo.sinistro)
            return self._ruota_destra(nodo)

        # ==================================================
        # CASO 4: Destra-Sinistra (fattore < -1 e valore
        # inserito nel sottoalbero destro-sinistro)
        # -> Prima ruotiamo a DESTRA il figlio destro,
        #    poi ruotiamo a SINISTRA il nodo corrente
        # ==================================================
        if fattore < -1 and valore < nodo.destro.valore:
            nodo.destro = self._ruota_destra(nodo.destro)
            return self._ruota_sinistra(nodo)

        # Se non c'è bisogno di rotazioni, restituiamo il nodo invariato
        return nodo

    # ---------------------------------------------------------
    # METODO: cerca(valore)
    # ---------------------------------------------------------
    # Cerca un valore nell'albero.
    # È identico al metodo cerca dell'ABR perché la struttura
    # di ricerca (sinistra=minore, destra=maggiore) è la stessa.
    # Restituisce True se trovato, False altrimenti.
    # ---------------------------------------------------------
    def cerca(self, valore):
        return self._cerca_ricorsivo(self.radice, valore)

    # ---------------------------------------------------------
    # METODO PRIVATO: _cerca_ricorsivo(nodo, valore)
    # ---------------------------------------------------------
    def _cerca_ricorsivo(self, nodo, valore):

        # Caso base: nodo vuoto -> valore non trovato
        if nodo is None:
            return False

        # Abbiamo trovato il valore!
        if valore == nodo.valore:
            return True

        # Il valore cercato è minore -> cerchiamo a sinistra
        if valore < nodo.valore:
            return self._cerca_ricorsivo(nodo.sinistro, valore)

        # Il valore cercato è maggiore -> cerchiamo a destra
        else:
            return self._cerca_ricorsivo(nodo.destro, valore)

    # ---------------------------------------------------------
    # METODO: altezza()
    # ---------------------------------------------------------
    # Restituisce l'altezza dell'intera albero.
    # Nell'AVL questa sarà sempre O(log n), mai O(n)!
    # ---------------------------------------------------------
    def altezza(self):
        return self._get_altezza(self.radice)
