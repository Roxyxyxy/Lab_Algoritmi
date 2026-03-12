# main.py - Script principale per il confronto degli alberi
# Questo script mette a confronto le prestazioni di tre
# diversi tipi di alberi di ricerca:
#   - ABR: Albero Binario di Ricerca (non bilanciato)
#   - AVL: Albero AVL (bilanciato con le altezze)
#   - RBT: Albero Rosso-Nero (bilanciato con i colori)
#
# Per ogni albero misuriamo:
#   1. Il tempo di inserimento di N elementi
#   2. L'altezza finale dell'albero
#   3. Il tempo di ricerca di 100 elementi a caso
#
# Lo facciamo sia con dati CASUALI che con dati ORDINATI,
# per vedere come si comportano gli alberi nei casi diversi.

import time
import random
import sys
import math
import matplotlib

# Aumentiamo il limite di ricorsione di Python.
# Il valore di default è 1000, che è troppo basso per alberi profondi. 
# AVL e RBT su N=3000 hanno profondità ~14-20
sys.setrecursionlimit(10000)
# Usiamo il backend 'Agg' che serve per salvare grafici su file senza mostrarli a schermo
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from abr import ABR
from avl import AVL
from rbt import RossoNero


# Teniamo le dimensioni basse per evitare il RecursionError
# che l'ABR su dati ordinati provoca con liste molto lunghe
# (ogni nodo aggiunto su una lista ordinata aumenta la
# profondità della ricorsione di 1, fino al limite di Python)
DIMENSIONI = [500, 1000, 1500, 2000, 2500, 3000]

# Quanti elementi cercare per misurare il tempo di ricerca
QUANTE_RICERCHE = 100

def esegui_esperimenti(tipo_dati):

    print("\n" + "=" * 60)
    print("  INIZIO ESPERIMENTI CON DATI: " + tipo_dati.upper())
    print("=" * 60)

    # Dizionari per raccogliere i risultati
    # Ogni lista avrà un valore per ogni dimensione testata
    tempi_inserimento = {"ABR": [], "AVL": [], "RBT": []}
    altezze           = {"ABR": [], "AVL": [], "RBT": []}
    tempi_ricerca     = {"ABR": [], "AVL": [], "RBT": []}

    # Iteriamo su ogni dimensione da testare
    for n in DIMENSIONI:

        print("\n  [*] Dimensione N =", n, "- tipo:", tipo_dati)

        # Creiamo una lista di N numeri interi da 1 a N*10
        # (moltiplicare per 10 riduce le collisioni/duplicati)
        lista = list(range(1, n * 10 + 1))

        if tipo_dati == "casuali":
            # Mescoliamo la lista in modo casuale
            random.shuffle(lista)
            # Prendiamo solo i primi N elementi
            lista = lista[:n]
        else:
            # Per i dati ordinati usiamo i primi N numeri in ordine
            # QUESTO è il caso peggiore per l'ABR!
            lista = list(range(1, n + 1))

        # Selezioniamo 100 elementi casuali dalla lista
        # per fare le ricerche (questi sicuramente esistono)
        elementi_da_cercare = random.sample(lista, QUANTE_RICERCHE)

        # Esperimento con ABR 
        # end evita il newline, flush=True forza la stampa immediata 
        print("      - ABR: inserimento...", end=" ", flush=True)
        albero_abr = ABR()
        inizio = time.perf_counter()
        for numero in lista:
            albero_abr.inserisci(numero)
        fine = time.perf_counter()
        tempo_ins_abr = fine - inizio
        tempi_inserimento["ABR"].append(tempo_ins_abr)
        print("fatto in {:.4f}s".format(tempo_ins_abr)) # formatta il numero float con 4 cifre decimali

        altezza_abr = albero_abr.altezza()
        altezze["ABR"].append(altezza_abr)
        print("      - ABR: altezza =", altezza_abr)

        print("      - ABR: ricerca...", end=" ", flush=True)
        inizio = time.perf_counter()
        for valore in elementi_da_cercare:
            albero_abr.cerca(valore)
        fine = time.perf_counter()
        tempo_ric_abr = fine - inizio
        tempi_ricerca["ABR"].append(tempo_ric_abr)
        print("fatta in {:.6f}s".format(tempo_ric_abr))

        # Esperimento con AVL
        print("      - AVL: inserimento...", end=" ", flush=True)
        albero_avl = AVL()
        inizio = time.perf_counter()
        for numero in lista:
            albero_avl.inserisci(numero)
        fine = time.perf_counter()
        tempo_ins_avl = fine - inizio
        tempi_inserimento["AVL"].append(tempo_ins_avl)
        print("fatto in {:.4f}s".format(tempo_ins_avl))

        altezza_avl = albero_avl.altezza()
        altezze["AVL"].append(altezza_avl)
        print("      - AVL: altezza =", altezza_avl)

        print("      - AVL: ricerca...", end=" ", flush=True)
        inizio = time.perf_counter()
        for valore in elementi_da_cercare:
            albero_avl.cerca(valore)
        fine = time.perf_counter()
        tempo_ric_avl = fine - inizio
        tempi_ricerca["AVL"].append(tempo_ric_avl)
        print("fatta in {:.6f}s".format(tempo_ric_avl))

        # Esperimento con RBT (Rosso-Nero)
        print("      - RBT: inserimento...", end=" ", flush=True)
        albero_rbt = RossoNero()
        inizio = time.perf_counter()
        for numero in lista:
            albero_rbt.inserisci(numero)
        fine = time.perf_counter()
        tempo_ins_rbt = fine - inizio
        tempi_inserimento["RBT"].append(tempo_ins_rbt)
        print("fatto in {:.4f}s".format(tempo_ins_rbt))

        altezza_rbt = albero_rbt.altezza()
        altezze["RBT"].append(altezza_rbt)
        print("      - RBT: altezza =", altezza_rbt)

        print("      - RBT: ricerca...", end=" ", flush=True)
        inizio = time.perf_counter()
        for valore in elementi_da_cercare:
            albero_rbt.cerca(valore)
        fine = time.perf_counter()
        tempo_ric_rbt = fine - inizio
        tempi_ricerca["RBT"].append(tempo_ric_rbt)
        print("fatta in {:.6f}s".format(tempo_ric_rbt))

    print("\n  [OK] Esperimenti con dati", tipo_dati, "completati!")

    # Restituiamo tutti i risultati raccolti
    return tempi_inserimento, altezze, tempi_ricerca


# Crea e salva 3 grafici .png: tempi di inserimento, altezze, tempi di ricerca.
def crea_grafici(tipo_dati, tempi_ins, altezze, tempi_ric):

    print("\n  [*] Creazione grafici per dati:", tipo_dati, "...")

    # Colori e stili per le tre linee del grafico
    colore_abr = "green"
    colore_avl = "blue"
    colore_rbt = "red"


    # GRAFICO 1: Tempo di Inserimento

    plt.figure(figsize=(10, 6))

    # Disegniamo una linea per ogni albero
    plt.plot(DIMENSIONI, tempi_ins["ABR"], color=colore_abr, label="ABR")
    plt.plot(DIMENSIONI, tempi_ins["AVL"], color=colore_avl, label="AVL")
    plt.plot(DIMENSIONI, tempi_ins["RBT"], color=colore_rbt, label="RBT")

    # Titolo e etichette degli assi
    plt.title("Tempo di Inserimento - Dati " + tipo_dati.capitalize())
    plt.xlabel("Numero di elementi (N)")
    plt.ylabel("Tempo (secondi)")

    # Mostriamo la legenda e la griglia per leggibilità
    plt.legend()
    plt.grid(True)

    # Salviamo il grafico come file .png
    nome_file_inserimento = "tempi_inserimento_" + tipo_dati + ".png"
    plt.savefig(nome_file_inserimento)
    # Chiudiamo la figura per liberare memoria
    plt.close()
    print("      Salvato:", nome_file_inserimento)


    # GRAFICO 2: Altezza degli Alberi

    plt.figure(figsize=(10, 6))

    plt.plot(DIMENSIONI, altezze["ABR"], color=colore_abr, label="ABR")
    plt.plot(DIMENSIONI, altezze["AVL"], color=colore_avl, label="AVL")
    plt.plot(DIMENSIONI, altezze["RBT"], color=colore_rbt, label="RBT")

    plt.title("Altezza degli Alberi - Dati " + tipo_dati.capitalize())
    plt.xlabel("Numero di elementi (N)")
    plt.ylabel("Altezza dell'albero")

    plt.legend()
    plt.grid(True)

    nome_file_altezze = "altezze_" + tipo_dati + ".png"
    plt.savefig(nome_file_altezze)
    plt.close()
    print("      Salvato:", nome_file_altezze)


    # GRAFICO 3: Tempo di Ricerca

    plt.figure(figsize=(10, 6))

    plt.plot(DIMENSIONI, tempi_ric["ABR"], color=colore_abr, label="ABR")
    plt.plot(DIMENSIONI, tempi_ric["AVL"], color=colore_avl, label="AVL")
    plt.plot(DIMENSIONI, tempi_ric["RBT"], color=colore_rbt, label="RBT")

    plt.title("Tempo di Ricerca (100 elementi) - Dati " + tipo_dati.capitalize())
    plt.xlabel("Numero di elementi (N)")
    plt.ylabel("Tempo (secondi)")

    plt.legend()
    plt.grid(True)

    nome_file_ricerca = "tempi_ricerca_" + tipo_dati + ".png"
    plt.savefig(nome_file_ricerca)
    plt.close()
    print("      Salvato:", nome_file_ricerca)

    print("  [OK] Grafici salvati!")


# Stampa un'analisi dei risultati: confronto di altezze, tempi e vantaggi/svantaggi.
def analizza_risultati(tipo_dati, tempi_ins, altezze, tempi_ric):

    print("\n" + "=" * 60)
    print("  ANALISI - Dati: " + tipo_dati.upper())
    print("=" * 60)

    # Usiamo i dati all'ultima dimensione (N massimo) per il confronto
    i_max     = len(DIMENSIONI) - 1
    n_max     = DIMENSIONI[i_max]

    h_abr     = altezze["ABR"][i_max]
    h_avl     = altezze["AVL"][i_max]
    h_rbt     = altezze["RBT"][i_max]

    t_ins_abr = tempi_ins["ABR"][i_max]
    t_ins_avl = tempi_ins["AVL"][i_max]
    t_ins_rbt = tempi_ins["RBT"][i_max]

    t_ric_abr = tempi_ric["ABR"][i_max]
    t_ric_avl = tempi_ric["AVL"][i_max]
    t_ric_rbt = tempi_ric["RBT"][i_max]

    # ANALISI ALTEZZA
    print("\n  ALTEZZA con N =", n_max)
    print("    ABR:", h_abr)
    print("    AVL:", h_avl)
    print("    RBT:", h_rbt)

    if tipo_dati == "ordinati":
        print("\n  OSSERVAZIONE:")
        print("    L'ABR ha altezza = N =", h_abr, "-> e' diventato una lista!")
        print("    Ogni elemento inserito e' maggiore del precedente, quindi")
        print("    va sempre a destra: si forma una catena lunga N nodi.")
        print("    Questo e' il CASO PEGGIORE dell'ABR: O(n) invece di O(log n).")
        print("    AVL mantiene altezza", h_avl, "(teorico:", int(math.log2(n_max)) + 1, ").")
        print("    RBT mantiene altezza", h_rbt, "(teorico al massimo:", int(2 * math.log2(n_max + 1)), ").")
        print("    VANTAGGIO di AVL e RBT: altezza SEMPRE logaritmica, anche")
        print("    nel caso peggiore (dati ordinati).")
    else:
        print("\n  OSSERVAZIONE:")
        print("    Con dati casuali l'ABR e' gia' parzialmente bilanciato")
        print("    (altezza ~", h_abr, "), ma AVL e RBT sono piu' bassi (", h_avl, "e", h_rbt, ").")
        print("    AVL e RBT garantiscono il bilanciamento in OGNI caso,")
        print("    mentre l'ABR dipende dall'ordine dei dati.")

    # ANALISI INSERIMENTO
    print("\n  TEMPO DI INSERIMENTO con N =", n_max)
    print("    ABR: {:.4f}s".format(t_ins_abr))
    print("    AVL: {:.4f}s".format(t_ins_avl))
    print("    RBT: {:.4f}s".format(t_ins_rbt))
    print("\n  OSSERVAZIONE:")

    if tipo_dati == "ordinati":
        print("    L'ABR e' molto piu' lento: scorre una catena di N nodi")
        print("    per ogni inserimento -> O(n) per inserimento -> O(n^2) totale.")
        print("    AVL e RBT inseriscono in O(log n): molto piu' efficienti.")
        print("    SVANTAGGIO di AVL: esegue piu' rotazioni di RBT (bilancia")
        print("    in modo piu' stretto), quindi l'inserimento e' leggermente")
        print("    piu' lento del RBT in certi scenari.")
    else:
        print("    Con dati casuali l'ABR e' spesso piu' veloce nell'inserimento")
        print("    perche' non esegue rotazioni ne' aggiornamenti di colore.")
        print("    VANTAGGIO di ABR su dati casuali: overhead minimo.")
        print("    SVANTAGGIO: questo vantaggio scompare con dati ordinati.")

    # ANALISI RICERCA
    print("\n  TEMPO DI RICERCA (" + str(QUANTE_RICERCHE) + " elementi) con N =", n_max)
    print("    ABR: {:.6f}s".format(t_ric_abr))
    print("    AVL: {:.6f}s".format(t_ric_avl))
    print("    RBT: {:.6f}s".format(t_ric_rbt))
    print("\n  OSSERVAZIONE:")

    if tipo_dati == "ordinati":
        # Calcoliamo quante volte l'ABR e' piu' lento di AVL
        if t_ric_avl > 0:
            rapporto = t_ric_abr / t_ric_avl
            print("    L'ABR e' circa {:.0f}x piu' lento di AVL.".format(rapporto))
        print("    Su un albero-lista, ogni ricerca percorre in media N/2 nodi.")
        print("    Su AVL e RBT ogni ricerca percorre al massimo log2(N) nodi.")
        print("    VANTAGGIO fondamentale di AVL e RBT: la ricerca e' sempre")
        print("    O(log n), indipendentemente dall'ordine di inserimento.")
    else:
        print("    Con dati casuali la ricerca e' simile per tutti e tre.")
        print("    L'altezza piu' bassa di AVL e RBT puo' dare un lieve vantaggio.")

    # CONCLUSIONE FINALE
    print("\n  RIEPILOGO VANTAGGI / SVANTAGGI")
    print("    ABR :")
    print("      + Semplice da implementare, overhead minimo")
    print("      + Veloce su dati casuali (niente rotazioni)")
    print("      - Degenera su dati ordinati: altezza O(n), ricerca O(n)")
    print("    AVL :")
    print("      + Bilanciamento ottimale: altezza minima garantita")
    print("      + Ricerca sempre O(log n)")
    print("      - Inserimento con overhead: aggiornamento altezze + rotazioni")
    print("    RBT :")
    print("      + Bilanciamento garantito O(log n) con meno rotazioni di AVL")
    print("      + Buon compromesso tra costo di inserimento e costo di ricerca")
    print("      - Implementazione piu' complessa (regole colori + padre)")
    print("=" * 60)


# Punto di partenza: viene eseguito solo quando si lancia main.py direttamente
if __name__ == "__main__":

    print("=" * 60)
    print("  CONFRONTO ALBERI: ABR vs AVL vs ROSSO-NERO")
    print("=" * 60)
    print("  Dimensioni testate:", DIMENSIONI)
    print("  Ricerche per test: ", QUANTE_RICERCHE)

    # Esperimento 1: dati casuali
    tempi_ins_c, altezze_c, tempi_ric_c = esegui_esperimenti("casuali")
    crea_grafici("casuali", tempi_ins_c, altezze_c, tempi_ric_c)
    analizza_risultati("casuali", tempi_ins_c, altezze_c, tempi_ric_c)

    # Esperimento 2: dati ordinati (caso peggiore per l'ABR)
    tempi_ins_o, altezze_o, tempi_ric_o = esegui_esperimenti("ordinati")
    crea_grafici("ordinati", tempi_ins_o, altezze_o, tempi_ric_o)
    analizza_risultati("ordinati", tempi_ins_o, altezze_o, tempi_ric_o)

    print("\n" + "=" * 60)
    print("  TUTTI GLI ESPERIMENTI COMPLETATI!")
    print("  File .png salvati nella cartella corrente.")
    print("=" * 60)
