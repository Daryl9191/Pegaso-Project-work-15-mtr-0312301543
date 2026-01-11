from dataclasses import dataclass

@dataclass(frozen=True)
class CaratteristicheProdotto:
    # Creazione della classe che definiscono le caratteristiche base del prodotto quando viene richiamata da funzioni esterne
    nome: str
    linea_produttiva: str  
    quantita_minima_kg: int
    quantita_massima_kg: int
    minuti_per_kg: float 
    capacita_giornaliera_kg: int
    tempo_preparazione_minuti: int  

@dataclass(frozen=True)
class ConfigurazioneImpianto:
    # Questa classe definisce la base di ore lavoro e la capacità totale di produzione giornaliere
    ore_lavoro_al_giorno: float
    capacita_totale_giornaliera_kg: int
