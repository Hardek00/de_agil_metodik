# Agil Metodik - Teori och Praktik

## Innehållsförteckning
1. [Vad är Agil Metodik?](#vad-är-agil-metodik)
2. [Det Agila Manifestet](#det-agila-manifestet)
3. [Scrum Framework](#scrum-framework)
4. [Roller i Agila Team](#roller-i-agila-team)
5. [Artefakter och Verktyg](#artefakter-och-verktyg)
6. [Agila Ceremonier](#agila-ceremonier)
7. [Andra Agila Metoder](#andra-agila-metoder)
8. [Praktiska Övningar](#praktiska-övningar)
9. [Vanliga Utmaningar](#vanliga-utmaningar)
10. [Verktyg för Agilt Arbete](#verktyg-för-agilt-arbete)

---

## Vad är Agil Metodik?

### Definition
Agil metodik är ett sätt att arbeta med mjukvaruutveckling och projektledning som betonar:
- **Flexibilitet** över stela processer
- **Samarbete** över kontraktförhandling
- **Fungerande produkter** över omfattande dokumentation
- **Anpassning till förändring** över att följa en plan

### Historisk Bakgrund
- **Traditionella metoder** (Waterfall): Linjära, sekventiella processer
- **Problem med traditionella metoder**: Långa utvecklingscykler, svårt att hantera förändringar
- **Agila metoder** (2001): Kortare cykler, snabb feedback, kontinuerlig förbättring

### Varför Agilt?
```
Traditionell utveckling:    [Plan] → [Design] → [Kod] → [Test] → [Deploy]
                           (6-12 månader)

Agil utveckling:           [Plan-Design-Kod-Test-Deploy] → [Plan-Design-Kod-Test-Deploy]
                           (2-4 veckor)      (2-4 veckor)
```

**Fördelar:**
- Snabbare leveranser
- Bättre kvalitet genom kontinuerlig testning
- Flexibilitet att anpassa sig till förändringar
- Högre kundnöjdhet genom regelbunden feedback

---

## Det Agila Manifestet

### De Fyra Grundvärdena

1. **Individer och interaktioner** framför processer och verktyg
   - Människor är viktigare än system
   - Kommunikation är nyckeln till framgång

2. **Fungerande mjukvara** framför omfattande dokumentation
   - Fokus på att leverera värde
   - Dokumentation ska vara nödvändig och användbar

3. **Kundsamarbete** framför kontraktförhandling
   - Kontinuerlig dialog med kunden
   - Gemensam förståelse för målen

4. **Att reagera på förändring** framför att följa en plan
   - Flexibilitet när nya krav uppstår
   - Planering är viktigt, men anpassning är viktigare

### De Tolv Principerna

1. **Tidig och kontinuerlig leverans** av värdefull mjukvara
2. **Välkomna förändrade krav**, även sent i utvecklingsprocessen
3. **Leverera fungerande mjukvara** ofta (veckor snarare än månader)
4. **Dagligt samarbete** mellan affärsmänniskor och utvecklare
5. **Motiverade individer** - ge dem stöd och förtroende
6. **Ansikte-mot-ansikte kommunikation** är mest effektiv
7. **Fungerande mjukvara** är det primära måttet på framsteg
8. **Hållbar utvecklingshastighet** - teamet ska kunna hålla takten
9. **Kontinuerlig uppmärksamhet** på teknisk excellens
10. **Enkelhet** - minimera onödigt arbete
11. **Självorganiserande team** producerar bästa resultat
12. **Regelbunden reflektion** och anpassning av arbetssätt

---

## Scrum Framework

### Översikt
Scrum är den mest populära agila metoden. Det är ett ramverk för att hantera komplexa produktutvecklingsprojekt.

```
Product Backlog → Sprint Planning → Sprint (2-4 veckor) → Sprint Review → Sprint Retrospective
      ↑                                      ↓
      └── Product Increment ←← Daily Standup ←┘
```

### Scrum Värderingar
- **Engagemang** (Commitment)
- **Mod** (Courage)
- **Fokus** (Focus)
- **Öppenhet** (Openness)
- **Respekt** (Respect)

### Timeboxing
Alla aktiviteter i Scrum har fasta tidsgränser:
- **Sprint**: 2-4 veckor
- **Sprint Planning**: 2-4 timmar
- **Daily Standup**: 15 minuter
- **Sprint Review**: 1-2 timmar
- **Sprint Retrospective**: 1-1.5 timmar

---

## Roller i Agila Team

### 1. Product Owner (Produktägare)
**Ansvar:**
- Definiera och prioritera Product Backlog
- Representera kundens röst
- Sätta acceptanskriterier
- Besluta om vad som ska byggas

**Egenskaper:**
- Stark affärsförståelse
- Beslutsfattare
- Tillgänglig för teamet
- Kan kommunicera vision tydligt

### 2. Scrum Master
**Ansvar:**
- Coacha teamet i Scrum-processen
- Ta bort hinder (impediments)
- Facilitera möten
- Skydda teamet från störningar

**Egenskaper:**
- Servant leadership
- Processexpert
- Konfliktlösare
- Kontinuerlig förbättrare

### 3. Development Team (Utvecklingsteam)
**Ansvar:**
- Bygga produkten
- Självstyra sitt arbete
- Uppskatta arbetsinsatser
- Säkerställa kvalitet

**Egenskaper:**
- Tvärfunktionellt (cross-functional)
- Självorganiserande
- 3-9 medlemmar
- Kollektivt ansvar

### Teamdynamik
```
Product Owner ←→ Scrum Master ←→ Development Team
      ↑              ↑                    ↑
   [Vision]      [Process]           [Execution]
```

---

## Artefakter och Verktyg

### 1. Product Backlog
**Vad det är:**
- Prioriterad lista av funktioner (features)
- Ägd av Product Owner
- Ständigt utvecklande dokument

**Struktur av en User Story:**
```
Som [roll/användare]
Vill jag [funktionalitet]
För att [nytta/värde]

Acceptanskriterier:
- Givet [kontext]
- När [händelse]
- Då [förväntat resultat]
```

**Exempel:**
```
Som student
Vill jag logga in på lärplattformen
För att komma åt kursmaterial

Acceptanskriterier:
- Givet att jag har giltiga inloggningsuppgifter
- När jag fyller i användarnamn och lösenord
- Då ska jag omdirigeras till startsidan
```

#### Epics
- Definition: Större, värdeorienterat arbete som spänner över flera stories och ofta flera sprintar. Samlar relaterade user stories som tillsammans levererar ett användarutfall.
- När: När en feature är för stor för en enskild sprint eller kräver flera steg/team.
- Hur bryta ner: Skiva vertikalt i värdesnitt (användarresa, arbetsflödessteg, datadelningsgränser). Undvik tekniska-lager‑skivor utan användarvärde.
- Acceptans på epik‑nivå: Formulera önskat utfall/mått (t.ex. “användare kan X end‑to‑end”). Epiken är klar när alla stories är Done och utfallet uppnås.
- Estimering & uppföljning: T‑shirt‑storlek (S/M/L) på epik; story points på stories. Följ procent klart via antal stories Done.
- Spårbarhet: Epic → stories → tasks. Länka i verktyget och i `docs/roadmap.md`.
- Verktyg: Jira har Epics. I GitHub kan man approximera med Milestones/Projects + label `epic:<namn>`.

Exempel på epik → stories:
- Epik: “Exportera rapporter till CSV”
  - Story A: Ladda ned en enkel dataset som CSV
  - Story B: Välj kolumner och filtrera innan export
  - Story C: Schema och filnamnsstandard i `docs/`

### 2. Sprint Backlog
**Vad det är:**
- Subset av Product Backlog för aktuell Sprint
- Teamets plan för Sprint
- Inkluderar uppgifter (tasks) för varje story

**Exempel Sprint Backlog:**
```
Sprint 1 (2 veckor):
1. User Story: Användaren kan registrera konto
   - Skapa registreringsformulär (8h)
   - Implementera validering (4h)
   - Koppla till databas (6h)
   - Skriva tester (4h)

2. User Story: Användaren kan logga in
   - Skapa inloggningsformulär (4h)
   - Implementera autentisering (8h)
   - Skapa session-hantering (6h)
```

### 3. Definition of Done (DoD)
**Exempel på DoD:**
- [ ] Kod är skriven och testad
- [ ] Unit tests passerar
- [ ] Kod är granskad (code review)
- [ ] Dokumentation är uppdaterad
- [ ] Funktionalitet är godkänd av Product Owner
- [ ] Kod är integrerad i main branch

### 4. Burndown Chart
```
Återstående arbete
        |
    100 |●
        | \
     75 |  ●
        |   \
     50 |    ●
        |     \
     25 |      ●
        |       \
      0 |________●
        1 2 3 4 5  Dagar i Sprint
```

### 5. Story Points
- Vad: Relativ uppskattning av arbetsinsats/komplexitet/osäkerhet – inte tid i timmar.
- Varför: Enklare att jämföra stories sinsemellan, robust mot individuella hastighetsskillnader.
- Skala: Ofta Fibonacci (1, 2, 3, 5, 8, 13 …). Välj en referens‑story (t.ex. “3p”) och jämför.
- Hur: Planning Poker – alla estimerar samtidigt, diskutera gap, aligna på ett värde.
- Do: Håll team‑specifikt, kalibrera regelbundet, använd för kapacitetsplanering (velocity).
- Don’t: Översätt direkt till timmar, jämför mellan team, använda för individmätning.

---

## Agila Ceremonier

### 1. Sprint Planning
**Syfte:** Planera vad som ska göras under Sprint
**Deltagare:** Hela Scrum-teamet
**Tidslängd:** 2-4 timmar (för 2-veckorssprint)

**Agenda:**
1. **Del 1:** Vad ska vi bygga?
   - Product Owner presenterar prioriterade stories
   - Teamet diskuterar och förstår kraven
   - Teamet commitar till Sprint-mål

2. **Del 2:** Hur ska vi bygga det?
   - Bryta ner stories i uppgifter
   - Uppskatta arbetsinsats
   - Skapa Sprint Backlog

### 2. Daily Standup
**Syfte:** Synkronisera teamet och identifiera hinder
**Deltagare:** Development Team (andra kan lyssna)
**Tidslängd:** 15 minuter
**Tid:** Samma tid varje dag

**Tre frågor:**
1. Vad gjorde jag igår?
2. Vad ska jag göra idag?
3. Finns det några hinder?

**Tips:**
- Stå upp (därav namnet)
- Fokus på arbetet, inte personen
- Håll det kort och koncist
- Ta djupare diskussioner efter mötet

### 3. Sprint Review
**Syfte:** Demonstrera vad som byggts och få feedback
**Deltagare:** Scrum-team + stakeholders
**Tidslängd:** 1-2 timmar

**Agenda:**
1. Demo av färdigställda features
2. Diskussion om vad som fungerade/inte fungerade
3. Feedback från stakeholders
4. Uppdatering av Product Backlog

### 4. Sprint Retrospective
**Syfte:** Förbättra teamets arbetssätt
**Deltagare:** Scrum-teamet
**Tidslängd:** 1-1.5 timmar

**Format - "Start, Stop, Continue":**
- **Start:** Vad ska vi börja göra?
- **Stop:** Vad ska vi sluta göra?
- **Continue:** Vad ska vi fortsätta göra?

**Andra format:**
- **Mad, Sad, Glad:** Känslomässig reflektion
- **5 Whys:** Djupare analys av problem
- **Timeline:** Kronologisk genomgång av Sprint

---

## Andra Agila Metoder

### 1. Kanban
**Principer:**
- Visualisera arbetsflödet
- Begränsa pågående arbete (WIP limits)
- Mät och förbättra flödet

**Kanban Board:**
```
| To Do | In Progress | Testing | Done |
|-------|-------------|---------|------|
| Task1 | Task3       | Task5   | Task7|
| Task2 | Task4       |         | Task8|
|       |             |         |      |
```

### 2. Extreme Programming (XP)
**Praktiker:**
- Parprogrammering
- Test-driven development (TDD)
- Kontinuerlig integration
- Refactoring
- Enkla designer

### 3. Lean Software Development
**Principer:**
- Eliminera slöseri
- Förstärk lärande
- Besluta så sent som möjligt
- Leverera så snabbt som möjligt
- Ge teamet makt
- Bygga in kvalitet
- Se helheten

---

## Praktiska Övningar

### Fulländat Exempel: "Adder" – En supersimpel app som adderar två tal

#### Produktvision (Why)
- Som studerande vill jag snabbt kunna addera två tal i en enkel app, så att jag slipper öppna kalkylatorn och kan fokusera på uppgiften.

#### Mål och Scope (What)
- Mål: En webbsida där användaren matar in två tal och ser summan direkt.
- Scope v1:
  - Inputfält A och B (endast heltal/decimaler)
  - Knapp "Beräkna" (eller auto‑beräkning)
  - Visning av resultat
  - Enkel felhantering för ogiltig input

#### Antaganden (Assumptions)
- Desktop först. Inga inloggningar/roller. Endast svenskt UI.

---

#### User Story (INVEST)
- Som användare vill jag kunna mata in två tal och se summan, så att jag snabbt kan beräkna enklare uttryck.

##### Acceptanskriterier (Gherkin‑stil)
- Givet att jag öppnar sidan, när jag skriver 2 i fält A och 3 i fält B och klickar på Beräkna, då ska resultat 5 visas.
- Givet att jag skriver 2.5 och 1.5, då ska resultat 4.0 visas.
- Givet att jag matar in ogiltig text i något fält, då ska jag få ett tydligt felmeddelande och inget resultat.
- Givet att fälten är tomma, då ska beräkning vara inaktiverad eller visa tomt resultat.

---

#### Product Backlog (prioriterad)
1. UI: Input A/B, knapp, resultatyta
2. Logik: Validering av numerisk input (int/float)
3. Felmeddelanden och disable‑state
4. Snabbtest (unit) för summalogik
5. Tillgänglighet: fokusordning och aria‑labels
6. Bonus: Auto‑beräkning on‑input
7. Bonus: Mörkt läge

##### Definition of Ready (DoR)
- Story har tydligt värde, tydliga AC, UI‑skiss (low‑fi), ingen blockerande beroende.

##### Definition of Done (DoD)
- Kod skriven och granskad
- Unit tests passerar lokalt/CI
- AC uppfyllda och demoade
- Tillgänglighetskontroll (grund)
- Dokumentation (README/notes) uppdaterad

---

#### Sprint Plan (Sprint 1 – 1 vecka)
- Sprintmål: Leverera enkel adderare med validering och felmeddelanden.
- Stories in:
  - #1 UI grund
  - #2 Validering
  - #3 Felmeddelanden
  - #4 Unit test för summalogik

##### Task Breakdown (exempel)
- Frontend UI (4h)
- Inputhantering/validering (3h)
- Felmeddelanden och disable‑state (2h)
- Summafunktion + unit test (2h)
- Manuell test/Demo‑script (1h)

---

#### Testfall (exempel)
- Positiva fall:
  - 2 + 3 = 5
  - 2.5 + 1.5 = 4.0
  - 0 + 0 = 0
- Negativa fall:
  - "abc" + 3 → visa fel, inget resultat
  - 2 + "" → visa fel, inget resultat
  - Mycket stora tal → visa resultat eller tydligt fel (över gräns)

---

#### Demo‑plan (Sprint Review)
1. Visa input A/B och knapp.
2. 2 + 3 → 5, 2.5 + 1.5 → 4.0.
3. Visa felmeddelande för "abc".
4. Gå igenom uppfyllda AC och DoD.

---

#### Retrospective (Start/Stop/Continue)
- Start: Skriv AC i Gherkin från början.
- Stop: Ta in stories utan UI‑skiss.
- Continue: Små stories, snabba code reviews.

---

#### Exempel på enkel pseudokod (summa‑logik)
```
function add(a, b):
  if not isNumber(a) or not isNumber(b):
    throw InvalidInput
  return toNumber(a) + toNumber(b)
```

#### Exempel på enkel test (pseudokod)
```
assert add(2, 3) == 5
assert add(2.5, 1.5) == 4.0
expect add("abc", 3) throws InvalidInput
```

---

#### Kanban/Scrum i praktiken (för denna miniprodukt)
- Board‑kolumner: To Do / In Progress / Review / Done
- WIP‑limit: max 2 i In Progress
- Daglig standup: 3 frågor (igår/idag/blockers)

---

> Poängen med exemplet är att visa hela kedjan: Vision → Story+AC → Backlog → DoR/DoD → Sprintplan → Tasking → Test → Demo → Retro. När detta fungerar för en enkel app, skala upp till riktiga funktioner.

#

## Vanliga Utmaningar

### 1. Motstånd mot Förändring
**Problem:** Team eller organisation vill inte ändra befintliga arbetssätt

**Lösningar:**
- Start small - pilotprojekt
- Utbilda och coacha
- Visa värdet av agila metoder
- Få ledningsstöd

### 2. Bristande Product Owner
**Problem:** Product Owner är inte tillgänglig eller saknar kunskap

**Lösningar:**
- Utbilda Product Owner i rollen
- Säkerställ tillgänglighet och mandat
- Proxy Product Owner för daglig kommunikation

### 3. För Stora User Stories
**Problem:** Stories tar flera Sprints att implementera

**Lösningar:**
- Bryt ner i mindre stories (story splitting)
- Använd INVEST-kriterierna
- Fokus på minimal viable functionality

### 4. Estimationsproblem
**Problem:** Team uppskattar konsekvent fel

**Lösningar:**
- Använd relativ uppskattning (story points)
- Spåra velocity över tid
- Förbättra genom retrospectives

### 5. Stakeholder Management
**Problem:** För många stakeholders med olika åsikter

**Lösningar:**
- Tydlig Product Owner-roll
- Regelbundna stakeholder-möten
- Transparent kommunikation om prioriteringar

---

## Verktyg för Agilt Arbete

### 1. Projekthantering
**Gratis verktyg:**
- **Trello:** Enkelt Kanban-board
- **GitHub Projects:** Integrerat med kod
- **Asana:** Omfattande projekthantering

**Betala verktyg:**
- **Jira:** Branschstandard för agila team
- **Azure DevOps:** Microsoft's lösning
- **Linear:** Modern, snabb issue tracking

### 2. Kommunikation
- **Slack:** Teamkommunikation
- **Microsoft Teams:** Video och chat
- **Discord:** Gaming-orienterad men populär bland studenter

### 3. Dokumentation
- **Confluence:** Kopplat till Jira
- **Notion:** All-in-one workspace
- **GitHub Wiki:** Enkelt och integrerat

### 4. Retrospectives
- **FunRetro:** Online retrospective boards
- **Miro/Mural:** Whiteboard-verktyg
- **Retrium:** Dedikerat retrospective-verktyg

---

## Mäta Framgång i Agila Team

### 1. Kvantitativa Mått
**Velocity:**
- Story points slutförda per Sprint
- Trender över tid
- Förutsägbarhet

**Burndown:**
- Framsteg inom Sprint
- Identifiera blockers tidigt
- Sprint-planering accuracy

**Lead Time:**
- Tid från idea till leverans
- Flödeseffektivitet
- Bottlenecks i processen

### 2. Kvalitativa Mått
**Team Happiness:**
- Regelbundna pulsmätningar
- Retrospective feedback
- Team-dynamik

**Kundnöjdhet:**
- Feedback från Sprint Reviews
- Användning av levererade features
- Ändringsfrekvens av krav

### 3. Tekniska Mått
**Code Quality:**
- Test coverage
- Bug rate
- Technical debt

**Deployment:**
- Deployment frequency
- Lead time for changes
- Mean time to recovery

---

## Sammanfattning

### Nycklar till Framgångsrik Agil Implementation

1. **Börja med Mindset**
   - Agilt är mer än process - det är ett sätt att tänka
   - Fokus på värde och kundnytta
   - Acceptera förändring som naturligt

2. **Investera i Människor**
   - Utbildning och coaching
   - Psykologisk säkerhet i teamet
   - Kontinuerlig förbättring

3. **Start Small, Scale Smart**
   - Pilot med ett team
   - Lär från misstag
   - Anpassa processen till din kontext

4. **Mät och Förbättra**
   - Använd data för beslut
   - Regelbundna retrospectives
   - Experimentera med förbättringar

### Fortsatt Lärande

**Böcker:**
- "Scrum: The Art of Doing Twice the Work in Half the Time" - Jeff Sutherland
- "User Story Mapping" - Jeff Patton
- "The Lean Startup" - Eric Ries

**Certifieringar:**
- Certified ScrumMaster (CSM)
- Professional Scrum Master (PSM)
- SAFe Agilist

**Konferenser och Communities:**
- Agile Sweden
- Local Scrum User Groups
- Agile Alliance

---

**Kom ihåg:** Agilt arbete handlar om att leverera värde snabbt och kontinuerligt förbättra både produkt och process. Det är en resa, inte ett mål!

---

### Vad är Gherkin?
Gherkin är ett enkelt, icke‑tekniskt språk för att beskriva testbara scenarion (BDD – Behavior‑Driven Development) så att både verksamhet och utveckling förstår samma sak.

- Syfte: skapa gemensam förståelse och kunna köra scenarion som automatiska tester
- Struktur (svenska termer):
  - Givet (Given): utgångsläge
  - När (When): handlingen
  - Då (Then): förväntat resultat
- Fördelar: tydliga krav, mindre missförstånd, lätt att automatisera

Mall:
```
Givet [utgångsläge]
När [handling]
Då [förväntat resultat]
```

Exempel (Adder‑appen):
```
Givet att jag öppnar sidan
När jag skriver 2 i fält A och 3 i fält B och klickar på Beräkna
Då ska resultat 5 visas
```
