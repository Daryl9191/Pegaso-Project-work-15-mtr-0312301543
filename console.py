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
    
    mappa_prodotti = {p.nome: p for p in prodotti}
    risultati = {}

    for nome_prodotto, kg in ordine.items():
        p = mappa_prodotti[nome_prodotto]
        
        # 1. Limite basato sulla capacità fisica (quanti kg al giorno al massimo)
        giorni_per_capacita_specifica = kg / p.capacita_giornaliera_kg
        giorni_per_capacita_totale = kg / impianto.capacita_totale_giornaliera_kg
        giorni_limite_fisico = max(giorni_per_capacita_specifica, giorni_per_capacita_totale)

        # 2. Limite basato sul tempo (quante ore di lavoro servono)
        minuti_totali = _calcola_minuti_necessari(kg, p)
        ore_totali = minuti_totali / 60.0
        giorni_necessari_per_tempo = ore_totali / impianto.ore_lavoro_al_giorno
        
        # La produzione finisce quando entrambi i limiti sono soddisfatti
        giorni_stimati = max(giorni_limite_fisico, giorni_necessari_per_tempo)

        risultati[nome_prodotto] = {
            "kg_richiesti": kg,
            "linea": p.linea_produttiva,
            "ore_tecniche": round(ore_totali, 1),
            "giorni_stimati": round(giorni_stimati, 1)
        }

    return risultati
    
#Stampa i risultati della simulazione in modo chiaro e leggibile.
def stampa_riepilogo(risultati: Dict[str, Dict]) -> None:
    print("=== Piano di produzione simulato ===\n")
    for nome, dati in risultati.items():
        print(f"📦 Prodotto: {nome}")
        print(f"   Quantità: {dati['kg_richiesti']} kg")
        print(f"   Linea: {dati['linea']}")
        print(f"   Lavoro necessario: {dati['ore_tecniche']} ore")
        print(f"   Tempo di consegna: {dati['giorni_stimati']} giorni")
        print("-" * 35)
