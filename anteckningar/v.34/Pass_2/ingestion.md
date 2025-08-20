# Data Ingestion i en Modern Data Stack

## 1. Vanliga Ingestion-lösningar
- **Batchbearbetning**: Data samlas in och bearbetas i stora klumpar vid schemalagda intervall. Detta är lämpligt för icke-tidskritisk data och kan vara mer resurseffektivt.
- **Streaming**: Data bearbetas i realtid när den anländer. Detta är idealiskt för tidskritiska applikationer som bedrägeridetektion eller live-analys.
- **API-baserad Ingestion**: Data tas in via API:er, vilket kan vara antingen engångsjobb eller alltid på-tjänster.

## 2. Infrastrukturöverväganden
- **Engångsjobb vs. Alltid-på API**:
  - **Engångsjobb**: Lämpligt för batchbearbetning där data tas in vid specifika intervall. Detta kan containeriseras och köras på plattformar som Cloud Run, vilket är kostnadseffektivt eftersom du bara betalar för den använda beräkningstiden.
  - **Alltid-på API**: Idealisk för realtidsdataingestion. Men i miljöer som Cloud Run är tjänsten inte riktigt "alltid-på" eftersom den skalas ner till noll när den inte används, vilket kan introducera kallstartsfördröjning.

## 3. Varför Spara Rådata?
- **Dataintegritet**: Rådata fungerar som källan till sanning, vilket gör att du kan ombearbeta eller transformera data vid behov utan att förlora ursprunglig information.
- **Flexibilitet**: Att ha rådata tillåter olika transformationer och analyser att utföras när affärsbehoven utvecklas.
- **Revisionsbarhet**: Rådata ger en komplett registrering av vad som togs in, vilket är viktigt för efterlevnad och revision.

## 4. Fetcher vs. Writer: Dela upp eller Kombinera?

### Fetcher
- **Definition**: En fetcher är en komponent i en dataingestion pipeline som ansvarar för att hämta eller extrahera data från en källa. Detta kan vara en API, en databas, en fil, eller någon annan datakälla.
- **Funktion**: Fetchern samlar in data och förbereder den för vidare bearbetning eller lagring. Den kan också utföra initiala transformationer eller filtreringar av data.
- **Exempel**: En fetcher kan vara ett skript som anropar en webbtjänst för att hämta väderdata varje timme.

### Writer
- **Definition**: En writer är en komponent som ansvarar för att skriva eller ladda data till en destination. Detta kan vara en databas, en datalake, en filsystem, eller en annan lagringslösning.
- **Funktion**: Writern tar den bearbetade eller råa data och lagrar den på ett sätt som är optimerat för framtida åtkomst och analys.
- **Exempel**: En writer kan vara ett skript som laddar data till en BigQuery-tabell efter att den har bearbetats.

### Kombination eller Separation
- **Kombinera**: I enklare pipelines kan fetcher och writer kombineras i en enda komponent, vilket kan förenkla arkitekturen och minska komplexiteten.
- **Separera**: I mer komplexa system kan det vara fördelaktigt att separera fetcher och writer för att möjliggöra mer modulär och skalbar design. Detta tillåter också att varje komponent kan optimeras och skalas oberoende.

