# Bash Grundkurs: Kommandoraden för Data Engineers

## Varför Bash?

Bash (Bourne Again SHell) är ett **kommandorads-interface** (CLI) för att interagera med ett operativsystem. Inom data och cloud engineering är det oumbärligt.

- **Automation:** Skripta repetitiva uppgifter
- **Cloud Management:** Alla cloud CLIs (gcloud, aws, az) körs i en shell
- **Server Management:** Interagera med virtuella maskiner och servrar
- **Data Processing:** Manipulera filer, köra data-pipelines
- **Docker & Git:** Centrala verktyg som styrs från kommandoraden

> **Princip:** Om du kan göra det med klick i ett gränssnitt, kan du göra det snabbare och mer reproducerbart med ett skript i Bash.

---

## 1. Grundläggande koncept

### Terminalen och prompten
När du startar WSL ser du en prompt, t.ex:
```bash
anvandare@datornamn:~$
```
- **anvandare:** Ditt användarnamn
- **datornamn:** Namnet på din maskin
- **`:`:** Avskiljare
- **`~`:** Din nuvarande katalog (tilda `~` är en genväg till din hemkatalog)
- **`$`:** Indikerar att du är en vanlig användare (en administratör/root har ofta `#`)

### Anatomi för ett kommando
De flesta kommandon följer samma struktur:
```bash
kommando -alternativ argument
```
- **kommando:** Programmet du vill köra (t.ex. `ls`)
- **alternativ (flagga):** Ändrar kommandots beteende (t.ex. `-l` för lång lista)
- **argument:** Vad kommandot ska agera på (t.ex. en fil eller katalog)

---

## 2. Viktiga kommandon: Anteckningar

### Navigation
| Kommando | Beskrivning | Exempel |
|---|---|---|
| `pwd` | **P**rint **W**orking **D**irectory (visa var du är) | `pwd` |
| `ls` | **L**i**s**t (lista filer/kataloger) | `ls`, `ls -la` |
| `cd` | **C**hange **D**irectory (byt katalog) | `cd /home/projekt` |
| `cd ~` | Gå till hemkatalogen | `cd ~` eller bara `cd` |
| `cd ..` | Gå upp en nivå | `cd ..` |

**Alternativ för `ls`:**
- `-l`: Långt format (rättigheter, ägare, storlek, datum)
- `-a`: Visa alla filer (inklusive dolda, de som börjar med `.`)
- `-h`: Human-readable (visa filstorlek i KB, MB, etc.)

### Fil- och kataloghantering
| Kommando | Beskrivning | Exempel |
|---|---|---|
| `mkdir` | **M**a**k**e **Dir**ectory (skapa katalog) | `mkdir mitt_projekt` |
| `touch` | Skapa en tom fil (eller uppdatera tidsstämpel) | `touch min_fil.txt` |
| `cp` | **C**o**p**y (kopiera fil/katalog) | `cp fil1.txt fil2.txt` |
| `mv` | **M**o**v**e (flytta eller byt namn på fil/katalog) | `mv gammalt_namn.txt nytt_namn.txt` |
| `rm` | **R**e**m**ove (ta bort fil) | `rm min_fil.txt` |
| `rmdir` | **R**emove **Dir**ectory (ta bort tom katalog) | `rmdir tom_katalog` |
| `rm -r` | Ta bort katalog och allt dess innehåll (Recursive) | `rm -r projekt_arkiv` |

> **VARNING:** `rm -rf /` är ett katastrofalt kommando. Använd `rm` med försiktighet! Det finns ingen papperskorg i Bash.

### Läsa filer
| Kommando | Beskrivning | Exempel |
|---|---|---|
| `cat` | Con**cat**enate (visa hela innehållet i en fil) | `cat fil.txt` |
| `less` | Visa innehållet sida för sida (mer modernt) | `less stor_loggfil.log` |
| `head` | Visa de första 10 raderna | `head fil.txt` |
| `tail` | Visa de sista 10 raderna | `tail -f fil.log` (`-f` följer filen live) |

### Pipes och Redirection (Superviktigt!)
- `|` (Pipe): Skicka output från ett kommando som input till ett annat.
- `>` (Redirect): Skriv över och spara output till en fil.
- `>>` (Append Redirect): Lägg till output i slutet av en fil.

**Exempel:**
```bash
# Lista alla filer, hitta de med "py" i namnet, och spara i en fil
ls -la | grep "py" > python_filer.txt

# Lägg till en ny rad i filen utan att radera det gamla
echo "Detta är en ny rad" >> python_filer.txt
```

### Sökning och filtrering
| Kommando | Beskrivning | Exempel |
|---|---|---|
| `grep` | **G**lobal **R**egular **E**xpression **P**rint (sök efter text i filer) | `grep "error" logg.txt` |
| `find` | Sök efter filer/kataloger baserat på namn, storlek etc. | `find . -name "*.py"` |

**Alternativ för `grep`:**
- `-i`: Ignorera skiftläge (case-insensitive)
- `-r`: Sök rekursivt i alla filer i en katalog
- `-v`: Invertera sökningen (visa rader som *inte* matchar)

---

## Nästa steg: Praktiska övningar

Nu när du har gått igenom grunderna är det dags att testa dina kunskaper.

➡️ **Fortsätt till [Bash Övningar](../../../exercises/bash-ovningar.md)** 