# coar_ird_it_stats

Statistiche sui record COAR IRD Italiani, curati dalle università di Bologna e Padova.

## Descrizione dei file

I dataset `systems_curated.csv` e `systems_italy.csv` sono estrazioni da COAR IRD al 30 ottobre 2026.

Il file `iris_installazioni.csv` è stato generato a partire da [questa lista](https://wiki.u-gov.it/confluence/display/public/UGOVHELP/List+of+IRIS+Installations+-+Elenco+delle+installazioni+IRIS) (scaricata dal sito CINECA il 26 ottobre 2026).

Il file `systems_italy.csv` è stato arricchito con le coordinate geografiche attraverso richieste a ror.org tramite lo script `add_coordinates.py`.

In seguito, il dataset è stato ulteriormente arricchito aggiungendo il dato `is_iris` (bool) sulla base della lista fornita dal CINECA, utilizzando lo script `add_iris_tag.py`.

I grafici sono salvati nel file `report.html`, e generati attraverso lo script `write_slides.py`.

## Uso

Questo progetto utilizza `uv` per gestire le librerie.

1. Installa uv: `curl -LsSf https://astral.sh/uv/install.sh | sh`
2. Installa le dependencies: `uv sync`
3. Per eseguire gli script: `uv run my_script.py`


## Licenza

Gli script e le elaborazioni sono rilasciati con licenza [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/deed.en).

I dataset `systems_curated.csv` e `systems_italy.csv` sono di pubblico dominio [CC0](https://creativecommons.org/public-domain/#cc0)