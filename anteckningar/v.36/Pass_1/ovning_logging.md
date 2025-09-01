# Övningar: Logging (grundnivå)

## Övning 1: Byt från print till logging
Du får denna kod med `print`. Gör om till `logging`.

```python
data = [1,2,3]

def fetch_data():
    print("Hämtar data...")
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
    if result is not None:
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

## Övning 3: Mer logging (endast om du inte har andra saker att göra)

Du får denna kod med `print`. Gör om till `logging`.

```python
import os
from statistics import mean

DATA = [1, 2, 3, 0, -5, 10, None, 4]


def fetch_data():
    print("Hämtar data...")
    if os.getenv("FAIL_FETCH") == "1":
        print("no data found (simulerad tom dataset)")
        return []
    if not DATA:
        print("no data found")
    return DATA


def clean_data(data):
    print("Rensar None-värden...")
    before = len(data)
    cleaned = [x for x in data if x is not None]
    removed = before - len(cleaned)
    if removed > 0:
        print(f"tog bort {removed} None-värden")
    else:
        print("inga None-värden hittade")
    return cleaned


def validate_data(data):
    print("Validerar data (positiva tal förväntas)...")
    negatives = [x for x in data if isinstance(x, (int, float)) and x < 0]
    zeros = [x for x in data if x == 0]
    non_numbers = [x for x in data if not isinstance(x, (int, float))]
    if negatives:
        print(f"varning: negativa värden hittade: {negatives}")
    if zeros:
        print(f"varning: nollor hittade: {zeros}")
    if non_numbers:
        print(f"varning: icke-numeriska värden hittade: {non_numbers}")
    print("Validering klar.")


def filter_positive_numbers(data):
    print("Filtrerar till positiva tal...")
    filtered = [x for x in data if isinstance(x, (int, float)) and x > 0]
    if not filtered:
        print("inga positiva tal kvar efter filtrering")
    else:
        print(f"{len(filtered)} positiva tal kvar")
    return filtered


def compute_average(data):
    print("Beräknar medelvärde...")
    try:
        if not data:
            print("kan inte beräkna medelvärde på tom lista")
            return None
        result = mean(data)
        print("medelvärde beräknat")
        return result
    except Exception as e:
        print(f"fel vid beräkning av medelvärde: {e}")
        return None


def save_result(value, path="result.txt"):
    print(f"Sparar resultat till {path}...")
    try:
        with open(path, "w", encoding="utf-8") as f:
            f.write(f"Resultat: {value}\n")
        print("Resultat sparat.")
    except Exception as e:
        print(f"fel vid skrivning till fil: {e}")


def process_data(data):
    if not data:
        print("no data")
        return None
    print("Bearbetar data:", data)

    cleaned = clean_data(data)
    validate_data(cleaned)
    positive = filter_positive_numbers(cleaned)
    avg = compute_average(positive)

    return avg


def main():
    print("Program startar...")
    data = fetch_data()
    result = process_data(data)
    if result is not None:
        print("Resultat:", result)
        save_result(result)
    print("Program klart.")


if __name__ == "__main__":
    main()
```