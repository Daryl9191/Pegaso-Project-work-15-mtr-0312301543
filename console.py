import random
import math
from typing import Dict, List
from classi import CaratteristicheProdotto, ConfigurazioneImpianto


# Questa funzione genera di un ordine casuale dei prodotti
def genera_ordine_casuale(prodotti: List[CaratteristicheProdotto], seed: int | None = None) -> Dict[str, int]:
    if seed is not None:
        random.seed(seed)

    ordine = {}
    for p in prodotti:
        ordine[p.nome] = random.randint(p.quantita_minima_kg, p.quantita_massima_kg)
    return ordine

#Funzione che calcola il tempo totale in minuti per preparazione prodotto e lavorazione
def _calcola_minuti_necessari(kg: int, prodotto: CaratteristicheProdotto) -> int:
    lavorazione = kg * prodotto.minuti_per_kg
    totale = prodotto.tempo_preparazione_minuti + lavorazione
    return int(math.ceil(totale))


#Analizza l'ordine e calcola i tempi di consegna stimatiConsidera sia la velocità dei macchinari che i limiti di carico giornalieri.

def simula_produzione(ordine: Dict[str, int], prodotti: List[CaratteristicheProdotto], impianto: ConfigurazioneImpianto) -> Dict[str, Dict]:
    """
    Simula la produzione con rotazione round-robin dei prodotti e calcolo saturazione impianto.
    """
    mappa_prodotti = {p.nome: p for p in prodotti}
    kg_rimanenti = {nome: kg for nome, kg in ordine.items()}
    risultati = {}
    
    giorno_corrente = 1
    prodotti_elenco = list(ordine.keys())
    
    kg_totali_lavorati = sum(ordine.values())
    kg_linea_a = sum(kg for nome, kg in ordine.items() if mappa_prodotti[nome].linea_produttiva == "A")
    kg_linea_b = sum(kg for nome, kg in ordine.items() if mappa_prodotti[nome].linea_produttiva == "B")

    ore_tecniche_totali = {}
    for nome, kg in ordine.items():
        p = mappa_prodotti[nome]
        minuti = _calcola_minuti_necessari(kg, p)
        ore_tecniche_totali[nome] = round(minuti / 60.0, 1)

    while any(kg > 0 for kg in kg_rimanenti.values()):
        capacita_disponibile_oggi = impianto.capacita_totale_giornaliera_kg
        
        # Rotazione round-robin: sposta il primo prodotto in fondo ogni giorno
        # per evitare che i primi prodotti abbiano sempre la precedenza
        shift = (giorno_corrente - 1) % len(prodotti_elenco)
        prodotti_oggi = prodotti_elenco[shift:] + prodotti_elenco[:shift]
        
        for nome in prodotti_oggi:
            if kg_rimanenti[nome] <= 0:
                continue
            
            p = mappa_prodotti[nome]
            kg_lavorabili_oggi = min(kg_rimanenti[nome], p.capacita_giornaliera_kg, capacita_disponibile_oggi)
            
            if kg_lavorabili_oggi > 0:
                kg_rimanenti[nome] -= kg_lavorabili_oggi
                capacita_disponibile_oggi -= kg_lavorabili_oggi
                
                if kg_rimanenti[nome] <= 0:
                    risultati[nome] = {
                        "kg_richiesti": ordine[nome],
                        "linea": p.linea_produttiva,
                        "ore_tecniche": ore_tecniche_totali[nome],
                        "giorno_completamento": giorno_corrente
                    }
            
            if capacita_disponibile_oggi <= 0:
                break
        
        if any(kg > 0 for kg in kg_rimanenti.values()):
            giorno_corrente += 1

    capacita_totale_teorica = giorno_corrente * impianto.capacita_totale_giornaliera_kg
    percentuale_utilizzo = round((kg_totali_lavorati / capacita_totale_teorica) * 100, 1)

    risultati["metriche_globali"] = {
        "giorni_totali_ordine": giorno_corrente,
        "kg_totali_lavorati": kg_totali_lavorati,
        "kg_linea_a": kg_linea_a,
        "kg_linea_b": kg_linea_b,
        "capacita_totale_teorica": capacita_totale_teorica,
        "percentuale_utilizzo_impianto": percentuale_utilizzo
    }
    return risultati

def stampa_riepilogo(risultati: Dict[str, Dict]) -> None:
    """Mostra i risultati della simulazione con statistiche di utilizzo impianto."""
    print("=== Piano di produzione simulato (Round-Robin & Saturazione) ===\n")
    
    metriche = risultati.pop("metriche_globali")
    
    for nome, dati in risultati.items():
        print(f"📦 Prodotto: {nome}")
        print(f"   Quantità: {dati['kg_richiesti']} kg")
        print(f"   Linea: {dati['linea']}")
        print(f"   Lavoro necessario: {dati['ore_tecniche']} ore")
        print(f"   Completato al giorno: {dati['giorno_completamento']}")
        print("-" * 35)
    
    print(f"\n📊 STATISTICHE ORDINE:")
    print(f"   KG Totali Linea A: {metriche['kg_linea_a']}")
    print(f"   KG Totali Linea B: {metriche['kg_linea_b']}")
    print(f"   KG Totali Lavorati: {metriche['kg_totali_lavorati']}")
    print(f"   Capacità Teorica Impianto: {metriche['capacita_totale_teorica']} kg")
    print(f"   Utilizzo Impianto: {metriche['percentuale_utilizzo_impianto']}%")
    print(f"\n✅ ORDINE COMPLETATO IN: {metriche['giorni_totali_ordine']} GIORNI")
