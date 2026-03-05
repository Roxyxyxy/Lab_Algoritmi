# abr.py - Albero Binario di Ricerca (ABR)
# Un Albero Binario di Ricerca è una struttura dati ad albero
# in cui ogni nodo rispetta questa regola:
#   - I valori nel sottoalbero SINISTRO sono MINORI del nodo
#   - I valori nel sottoalbero DESTRO sono MAGGIORI del nodo
# Classi NodoABR e ABR implementano questa struttura dati, 
# con metodi per inserire valori, cercare valori e calcolare l'altezza dell'albero.


class NodoABR:
# Rappresenta un singolo nodo dell'albero
# Ogni nodo contiene un valore e due "puntatori" ai figli
    def __init__(self, valore):
        self.valore = valore
        # Figlio sinistro: all'inizio è vuoto (None)
        self.sinistro = None
        # Figlio destro: all'inizio è vuoto (None)
        self.destro = None


class ABR:
# Rappresenta l'albero
    def __init__(self):
        # All'inizio l'albero è vuoto, quindi la radice è None
        self.radice = None

    
    def inserisci(self, valore):
        # Se l'albero è vuoto, il nuovo nodo diventa la radice
        if self.radice is None:
            self.radice = NodoABR(valore)
            return

        # Partiamo dalla radice e scendiamo finché troviamo un posto libero
        nodo_corrente = self.radice
        while True:
            # Il valore è MINORE: dobbiamo andare a sinistra
            if valore < nodo_corrente.valore:
                if nodo_corrente.sinistro is None:
                    # Se c'è un posto libero a sinistra lo inseriamo qui
                    nodo_corrente.sinistro = NodoABR(valore)
                    return
                else:
                    # Posto occupato: continuiamo a scendere
                    nodo_corrente = nodo_corrente.sinistro

            # Il valore è MAGGIORE: dobbiamo andare a destra
            elif valore > nodo_corrente.valore:
                if nodo_corrente.destro is None:
                    # Se c'è un posto libero a destra lo inseriamo qui
                    nodo_corrente.destro = NodoABR(valore)
                    return
                else:
                    # Posto occupato: continuiamo a scendere
                    nodo_corrente = nodo_corrente.destro

            # Il valore è uguale: duplicato, non inseriamo
            else:
                return

    
    def cerca(self, valore):
        # Partiamo dalla radice e scendiamo finché troviamo o finiamo
        nodo_corrente = self.radice

        while nodo_corrente is not None:
            if valore == nodo_corrente.valore:
                return True
            # Se il valore cercato è MINORE andiamo a sinistra
            elif valore < nodo_corrente.valore:
                nodo_corrente = nodo_corrente.sinistro
            # Se il valore cercato è MAGGIORE andiamo a destra
            else:
                nodo_corrente = nodo_corrente.destro

        return False


    
    def altezza(self): 
    # Calcola l'altezza dell'albero 
        # Albero vuoto: altezza 0
        if self.radice is None:
            return 0

        altezza_massima = 0

        # La pila contiene coppie: (nodo, profondità) che dobbiamo visitare
        pila = [(self.radice, 1)]
        # Usiamo una PILA (stack) per visitare l'albero 
        while len(pila) > 0:
            # Visitiamo finchè pila non è vuota
            nodo, profondita = pila.pop()

            # Aggiorniamo l'altezza massima trovata finora
            if profondita > altezza_massima:
                altezza_massima = profondita

            # Aggiungiamo i figli alla pila (se esistono)
            if nodo.sinistro is not None:
                pila.append((nodo.sinistro, profondita + 1))
            if nodo.destro is not None:
                pila.append((nodo.destro, profondita + 1))

        return altezza_massima
