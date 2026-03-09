# avl.py - Albero AVL 
# L'albero AVL è un Albero Binario di Ricerca bilanciato
# La differenza rispetto all'ABR normale è che l'AVL si
# "aggiusta" automaticamente dopo ogni inserimento per mantenersi bilanciato.
#
# Fattore di Bilanciamento:
#   fattore = altezza(sottoalbero_sinistro) - altezza(sottoalbero_destro)
#
#   Se il fattore è  0, +1 o -1 -> il nodo è bilanciato
#   Se il fattore è +2          -> troppo pesante a SINISTRA
#   Se il fattore è -2          -> troppo pesante a DESTRA
#
# Quando un nodo è sbilanciato, si eseguono le rotazioni
# per riportare l'albero in equilibrio



class NodoAVL:

    def __init__(self, valore):
        self.valore = valore
        self.sinistro = None
        self.destro = None
        # Un nodo appena creato (senza figli) ha altezza 1
        self.altezza = 1
# L'altezza di un nodo è la distanza dal nodo alla foglia
# più lontana sotto di lui.


class AVL:

    def __init__(self):
        # All'inizio l'albero è vuoto
        self.radice = None

    
    def _get_altezza(self, nodo):
        if nodo is None:
            return 0
        return nodo.altezza

    
    def _get_bilanciamento(self, nodo):
        if nodo is None:
            return 0
        altezza_sinistra = self._get_altezza(nodo.sinistro)
        altezza_destra = self._get_altezza(nodo.destro)
        return altezza_sinistra - altezza_destra

    

    def _aggiorna_altezza(self, nodo):
        altezza_sinistra = self._get_altezza(nodo.sinistro)
        altezza_destra = self._get_altezza(nodo.destro)
        if altezza_sinistra > altezza_destra:
            nodo.altezza = 1 + altezza_sinistra
        else:
            nodo.altezza = 1 + altezza_destra

    
    # Quando il sottoalbero sinistro è troppo pesante
    # si esegue una rotazione a destra attorno al nodo "y"

    # Prima della rotazione:       Dopo la rotazione:
    #       y                           x
    #      / \                         / \
    #     x   C          -->          A   y
    #    / \                             / \
    #   A   B                           B   C
    
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

        # Prima aggiorniamo y (ora è più in basso), poi x (ora è più in alto)
        self._aggiorna_altezza(y)
        self._aggiorna_altezza(x)

        return x

    
    # Quando il sottoalbero destro è troppo pesante
    # si esegue una rotazione a sinistra attorno al nodo "x"

    # Prima della rotazione:       Dopo la rotazione:
    #
    #     x                               y
    #    / \                             / \
    #   A   y              -->          x   C
    #      / \                         / \
    #     B   C                       A   B
    
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

        # Prima aggiorniamo x (ora è più in basso), poi y (ora è più in alto)
        self._aggiorna_altezza(x)
        self._aggiorna_altezza(y)

        return y


    def inserisci(self, valore):
        # Restituisce la nuova radice dell'albero dopo l'inserimento ricorsivo del valore
        self.radice = self._inserisci_ricorsivo(self.radice, valore)

    # Il metodo di inserimento ricorsivo fa 3 cose:
    #   1. Inserisce il nodo come in un ABR normale
    #   2. Aggiorna l'altezza del nodo corrente
    #   3. Controlla il bilanciamento e, se necessario, ruota
    #
    # I 4 CASI DI SBILANCIAMENTO:
    #   - Caso Sinistra-Sinistra (SS): ruotazione destra semplice
    #   - Caso Destra-Destra (DD):     rotazione sinistra semplice
    #   - Caso Sinistra-Destra (SD):   prima sinistra, poi destra
    #   - Caso Destra-Sinistra (DS):   prima destra, poi sinistra

    def _inserisci_ricorsivo(self, nodo, valore):

        # Se viene messo in un posto vuoto, creiamo il nodo e lo inseriamo lì
        if nodo is None:
            return NodoAVL(valore)

        # Il valore è minore: scendiamo a sinistra
        if valore < nodo.valore:
            nodo.sinistro = self._inserisci_ricorsivo(nodo.sinistro, valore)
        # Il valore è maggiore: scendiamo a destra
        elif valore > nodo.valore:
            nodo.destro = self._inserisci_ricorsivo(nodo.destro, valore)
        else:
            return nodo

        # Aggiorniamo l'altezza del nodo corrente dopo l'inserimento
        self._aggiorna_altezza(nodo)

        # Calcoliamo il fattore di bilanciamento del nodo corrente
        fattore = self._get_bilanciamento(nodo)


        # Controlliamo i 4 casi di sbilanciamento e applichiamo le rotazioni necessarie
        
        # CASO 1: Sinistra-Sinistra (fattore > 1 e valore inserito nel sottoalbero sinistro-sinistro)
        # dove basta una rotazione a destra per bilanciare
        if fattore > 1 and valore < nodo.sinistro.valore:
            return self._ruota_destra(nodo)

        # CASO 2: Destra-Destra (fattore < -1 e valore inserito nel sottoalbero destro-destro)
        # dove basta una rotazione a sinistra per bilanciare
        if fattore < -1 and valore > nodo.destro.valore:
            return self._ruota_sinistra(nodo)

        # CASO 3: Sinistra-Destra (fattore > 1 e valore inserito nel sottoalbero sinistro-destro)
        # Prima ruotiamo a SINISTRA il figlio sinistro, poi ruotiamo a DESTRA il nodo corrente
        if fattore > 1 and valore > nodo.sinistro.valore:
            nodo.sinistro = self._ruota_sinistra(nodo.sinistro)
            return self._ruota_destra(nodo)

        # CASO 4: Destra-Sinistra (fattore < -1 e valore inserito nel sottoalbero destro-sinistro)
        # Prima ruotiamo a DESTRA il figlio destro, poi ruotiamo a SINISTRA il nodo corrente
        if fattore < -1 and valore < nodo.destro.valore:
            nodo.destro = self._ruota_destra(nodo.destro)
            return self._ruota_sinistra(nodo)

        # Se non c'è bisogno di rotazioni, restituiamo il nodo invariato
        return nodo

 
    def cerca(self, valore):
        return self._cerca_ricorsivo(self.radice, valore)

    
    def _cerca_ricorsivo(self, nodo, valore):

        # Caso base: nodo vuoto -> valore non trovato
        if nodo is None:
            return False

        if valore == nodo.valore:
            return True

        # Il valore cercato è minore -> cerchiamo a sinistra
        if valore < nodo.valore:
            return self._cerca_ricorsivo(nodo.sinistro, valore)

        # Il valore cercato è maggiore -> cerchiamo a destra
        else:
            return self._cerca_ricorsivo(nodo.destro, valore)

   
    def altezza(self):
        return self._get_altezza(self.radice)
