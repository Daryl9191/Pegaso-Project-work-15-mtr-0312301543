from classi import CaratteristicheProdotto, ConfigurazioneImpianto
from console import genera_ordine_casuale, simula_produzione, stampa_riepilogo

if __name__ == "__main__":
    # Configurazione del catalogo prodotti (termini reali del settore)
    catalogo = [
        CaratteristicheProdotto(
            nome="Miscela Cereali Zootecnica",
            linea_produttiva="A",
            quantita_minima_kg=1500,
            quantita_massima_kg=6000,
            minuti_per_kg=0.18,
            capacita_giornaliera_kg=8000,
            tempo_preparazione_minuti=45
          ),
        CaratteristicheProdotto(
            nome="Mangime Sfarinato Premium",
            linea_produttiva="A",
            quantita_minima_kg=1200,
            quantita_massima_kg=5000,
            minuti_per_kg=0.22,
            capacita_giornaliera_kg=6500,
            tempo_preparazione_minuti=60
        ),
        CaratteristicheProdotto(
            nome="Mangime Pellettato Alta Resa",
            linea_produttiva="B",
            quantita_minima_kg=1000,
            quantita_massima_kg=4500,
            minuti_per_kg=0.35,
            capacita_giornaliera_kg=4200,
            tempo_preparazione_minuti=90
        ),
        CaratteristicheProdotto(
            nome="Concime Granulare Bio",
            linea_produttiva="B",
            quantita_minima_kg=800,
            quantita_massima_kg=3500,
            minuti_per_kg=0.30,
            capacita_giornaliera_kg=5000,
            tempo_preparazione_minuti=80
        ),
    ]

    # Settaggio parametri
    fabbrica = ConfigurazioneImpianto(
        ore_lavoro_al_giorno=8.0,
        capacita_totale_giornaliera_kg=12000
    )

    # Start della simulazione
    ordine_corrente = genera_ordine_casuale(catalogo)
    risultati_simulazione = simula_produzione(ordine_corrente, catalogo, fabbrica)
    stampa_riepilogo(risultati_simulazione)
    print("Simulazione completata.")