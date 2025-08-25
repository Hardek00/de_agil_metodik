# Övningar: Logging (grundnivå)

## Övning 1: Byt från print till logging
Du får denna kod med `print`. Gör om till `logging`.

```python
def fetch_data():
    print("Hämtar data...")
    data = []
    if not data:
        print("no data found")
    return data

def process_data(data):
    if not data:
        print("no data")
        return None
    print("Bearbetar data:", data)
    return sum(data) / len(data)

def main():
    print("Program startar...")
    data = fetch_data()
    result = process_data(data)
    print("Resultat:", result)
    print("Program klart.")

if __name__ == "__main__":
    main()
```

Gör så här:
1) `import logging`
2) Lägg till i början: `logging.basicConfig(level=logging.INFO)`
3) Ersätt `print`:
   - Normal flödesinfo → `logging.info("...")`
   - Avvikelse (t.ex. tom data) → `logging.warning("no data found")`
4) Extra: Wrappa `process_data` i `try/except` och logga fel med `logging.exception("Fel i process_data")` om något går fel.

Hints:
- `logging.info("Bearbetar data: %s", data)` (använd `%s` och parametrar istället för f‑strings i logg‑anrop)
- Låt meddelandena vara korta och tydliga.

---

## Övning 2: Förstå basicConfig (nivåer och format)
Utgå från den omskrivna koden från övning 1. Lägg till tydligare konfiguration och testa nivåfiltrering.

1) Sätt format och nivå:
```python
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
)
```
Förklaring av fälten:
- `%(asctime)s`: tidsstämpel
- `%(levelname)s`: nivå (INFO/WARNING/etc.)
- `%(name)s`: loggerns namn (modul)
- `%(message)s`: själva texten

2) Lägg (valfritt) till en modul‑specifik logger och använd den:
```python
logger = logging.getLogger(__name__)
logger.info("Program startar…")
```

3) Testa nivåer:
- Ändra `level=logging.DEBUG` och logga en rad med `logging.debug("detaljer…")`. Syns nu.
- Byt tillbaka till `INFO`. Samma `debug` ska inte synas.

4) Välj nivåer med mening i din kod:
- Start och resultat → `INFO`
- Tom data eller oväntat värde → `WARNING`
- Fångat undantag → `ERROR` eller `logging.exception(...)`

Bonus:
- Lägg till `%(lineno)d` i formatsträngen för att se radnummer.
- Prova att skicka in lite testdata (t.ex. `data = [1,2,3]`) och se hur loggen förändras.
