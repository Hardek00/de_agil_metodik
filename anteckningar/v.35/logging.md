# Logging vs print i Python – när, hur och varför

## Varför logging istället för print?
- **Nivåer & filtrering**: Välj viktighet (DEBUG/INFO/WARNING/ERROR/CRITICAL) och filtrera per miljö.
- **Strukturer**: Tidsstämplar, modul/fil, tråd/process – automatiskt.
- **Handlers**: Skicka loggar till flera mål (konsol, fil, syslog, JSON, moln).
- **Konfiguration**: Centralt styrt (kod eller config), utan att ändra anropsställen.
- **Prestanda & säkerhet**: Slå av detaljnivå i prod, undvik att spamma; maska känslig data.

Print är ok för snabba experiment/notebooks – byt till logging i applikationer, bibliotek och produktion.

---

## Snabb jämförelse
- **print**: skriver alltid till stdout, ingen nivå, svår att stänga av/omdirigera centralt.
- **logging**: nivåer, formatters, handlers, hierarki (`logger` per modul), konfigurerbar globalt.

---

## Grundläggande användning
```python
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s [%(name)s] %(message)s",
)

logging.debug("detaljer för felsökning")
logging.info("normalt flöde")
logging.warning("något ser konstigt ut")
logging.error("fel uppstod")
logging.critical("kritiskt fel")
```

Tips: Använd modul‑specifik logger i filer:
```python
logger = logging.getLogger(__name__)
logger.info("Hej från %s", __name__)
```

---

## Nivåer (vanlig praxis)
- `DEBUG`: detaljer för utveckling/felsökning
- `INFO`: normal körning, viktiga steg
- `WARNING`: avvikelse men programmet fortsätter
- `ERROR`: fel som påverkar funktionalitet
- `CRITICAL`: allvarliga fel som kan kräva omedelbar åtgärd

I utveckling: `level=logging.DEBUG`. I produktion: minst `INFO` eller `WARNING`.

---

## Handlers & formatters (konsol + fil)
```python
import logging
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("app")
logger.setLevel(logging.INFO)

# Konsol
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
ch.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
logger.addHandler(ch)

# Fil med rotation
fh = RotatingFileHandler("app.log", maxBytes=5_000_000, backupCount=3)
fh.setLevel(logging.INFO)
fh.setFormatter(logging.Formatter(
    "%(asctime)s %(levelname)s [%(name)s:%(lineno)d] %(message)s"
))
logger.addHandler(fh)

logger.info("startar…")
```

---

## Strukturerad/JSON‑loggning (för moln/loggaggregatorer)
```python
# pip install python-json-logger
from pythonjsonlogger import jsonlogger
import logging, sys

logger = logging.getLogger("svc")
handler = logging.StreamHandler(sys.stdout)
fmt = jsonlogger.JsonFormatter("%(asctime)s %(levelname)s %(name)s %(message)s")
handler.setFormatter(fmt)
logger.addHandler(handler)
logger.setLevel(logging.INFO)

logger.info("order skapad", extra={"order_id": 123, "user_id": "u-9"})
```

I Docker/Cloud Run: logga till stdout/stderr; plattformen samlar upp.

---

## Bra praxis
- Använd `logger = logging.getLogger(__name__)` i varje modul.
- Parametriserade meddelanden: `logger.info("Kund %s skapad", customer_id)` (undvik f‑strings i loggsträngar för prestanda).
- Logga inte hemligheter/PII (maskera eller utelämna).
- En rad per händelse; undvik enorma objekt. Sammanfatta eller logga nyckelfält.
- Håll DEBUG‑loggar värdefulla; undvik brus.

---

## När är print acceptabelt?
- Snabbt experiment i REPL/notebook.
- Tillfällig debugging i skript som kastas bort.
- Aldrig i återanvändbara bibliotek eller produktionskod.

---

## Konfiguration via dictConfig (centralt)
```python
import logging, logging.config

LOGGING = {
  "version": 1,
  "disable_existing_loggers": False,
  "formatters": {
    "std": {"format": "%(asctime)s %(levelname)s [%(name)s] %(message)s"}
  },
  "handlers": {
    "console": {"class": "logging.StreamHandler", "formatter": "std", "level": "INFO"}
  },
  "root": {"handlers": ["console"], "level": "INFO"}
}

logging.config.dictConfig(LOGGING)
logging.getLogger(__name__).info("start")
```

---

## Integrationsexempel
- **FastAPI/Uvicorn**: `uvicorn` har egna loggers (`uvicorn`, `uvicorn.error`, `uvicorn.access`). Sätt miljövariabler/uvicorn‑flaggor eller konfigurera `logging.config` tidigt i appen.
- **Requests**: aktivera `logging.getLogger("requests").setLevel(logging.WARNING)` om du vill tysta/brusa upp HTTP‑loggar.
- **SQL‑drivrutiner**: många använder `logging`; höj nivån vid felsökning.

---

## Felsökningstips
- Ser du inga loggar? Kontrollera `level` på både logger och handler.
- Dubbla loggar? Undvik att lägga till handlers flera gånger; skydda med vakt eller initiera bara i main.
- Tidszoner: inkludera `%(asctime)s)` och hantera TZ centralt om du behöver UTC.

---

## Sammanfattning
- Använd `logging` för allt som inte är engångsskript.
- Välj rätt nivåer, standardisera format, och skicka till rätt mål.
- Print är för snabba experiment – logging är för system.
