# Agil Metodik – Kursmaterial

## Innehållsförteckning
1. [Vad är Agilt?](#vad-är-agilt)
2. [Det Agila Manifestet](#det-agila-manifestet)
3. [Scrum Framework](#scrum-framework)
4. [Roller](#roller)
5. [Artefakter](#artefakter)
6. [Ceremonier](#ceremonier)
7. [Andra Agila Metoder](#andra-agila-metoder)
8. [Vanliga Utmaningar](#vanliga-utmaningar)
9. [Verktyg](#verktyg)
10. [Mäta Framgång](#mäta-framgång)
11. [Nycklar till Framgång](#nycklar-till-framgång)
12. [Resurser och Länkar](#resurser-och-länkar)

---

## Vad är Agilt?
Agilt är ett arbetssätt för att utveckla mjukvara (och andra typer av projekt) som sätter **människan och värdeskapandet i centrum**.  

**Traditionella metoder (Waterfall):**
- Planering och krav samlas in i början.  
- Processen är linjär: Plan → Design → Utveckling → Test → Leverans.  
- Risk: kunden får se produkten först efter lång tid.  
- Förändringar är svåra och dyra att hantera.  

**Agila metoder:**
- Arbetet delas upp i korta iterationer (2–4 veckor).  
- Efter varje iteration finns en potentiellt levererbar produkt.  
- Kunden är delaktig under hela processen.  
- Förändringar ses som en möjlighet, inte som ett problem.  

**Exempel – skillnad i leverans:**

```
Traditionell utveckling:   [Plan] → [Design] → [Kod] → [Test] → [Leverans]
                           (6-12 månader)

Agil utveckling:           [Plan-Design-Kod-Test-Deploy] → [Plan-Design-Kod-Test-Deploy]
                           (2-4 veckor)                   (2-4 veckor)
```

---

## Det Agila Manifestet
Manifestet skrevs 2001 av 17 erfarna utvecklare. Det beskriver **4 värderingar** och **12 principer**.  

### Fyra värderingar
1. **Individer och interaktioner** framför processer och verktyg  
   → Samarbete och kommunikation är viktigare än formella processer.  

2. **Fungerande mjukvara** framför omfattande dokumentation  
   → Dokumentation är viktigt, men det centrala är att produkten fungerar.  

3. **Kundsamarbete** framför kontraktförhandling  
   → Dialog och samarbete är mer värdefullt än att strikt följa kontrakt.  

4. **Att reagera på förändring** framför att följa en plan  
   → En plan är bra, men anpassning är ännu viktigare.  

### Tolv principer (kortat urval)
- Leverera värdefull mjukvara tidigt och kontinuerligt.  
- Välkomna förändringar, även sent i projektet.  
- Leverera fungerande mjukvara ofta (veckor, inte månader).  
- Affärsfolk och utvecklare ska samarbeta dagligen.  
- Självorganiserande team ger bäst resultat.  
- Reflektera regelbundet och förbättra arbetssättet.  

**Att tänka på:** Manifestet är inte en metod, utan en filosofi. Scrum, Kanban m.fl. är ramverk som bygger på dessa principer.  

---

## Scrum Framework
Scrum är det vanligaste agila ramverket. Det är **enkelt att förstå men svårt att bemästra**.  

**Flöde:**
```
Product Backlog → Sprint Planning → Sprint (2-4 veckor) → Review → Retrospective
```

### Scrum-värderingar
- **Engagemang** – alla i teamet tar ansvar.  
- **Mod** – våga ta upp problem, testa nytt.  
- **Fokus** – leverera mot sprintmålet.  
- **Öppenhet** – transparens om arbete och hinder.  
- **Respekt** – för teamets olika roller och kompetenser.  

### Timeboxing
- **Sprint:** 2–4 veckor.  
- **Sprint Planning:** max 4h för en 2-veckors sprint.  
- **Daily Standup:** 15 minuter varje dag.  
- **Sprint Review:** 1–2h.  
- **Sprint Retrospective:** 1–1,5h.  

---

## Roller
Scrum definierar tre roller:  

### Product Owner (PO)
- Ansvarar för att maximera värdet av produkten.  
- Äger och prioriterar Product Backlog.  
- Är länken mellan teamet och kunden.  

### Scrum Master (SM)
- Ansvarar för att processen följs.  
- Tar bort hinder (impediments).  
- Coachar teamet och organisationen i agila arbetssätt.  

### Development Team
- Självorganiserande och tvärfunktionellt.  
- Består oftast av 3–9 personer.  
- Ansvarar kollektivt för att leverera produktinkrementet.  

**Rollernas relation:**
```
Product Owner (vision) ←→ Scrum Master (process) ←→ Development Team (utförande)
```

---

## Artefakter

### Product Backlog
- En prioriterad lista av funktionalitet som kan utvecklas.  
- Ägs av PO men hela teamet kan bidra.  
- Är levande – uppdateras kontinuerligt.  

**Exempel User Story:**  
> Som student vill jag logga in på plattformen för att komma åt kursmaterial.  

**Acceptanskriterier:**  
- Givet att jag har giltiga inloggningsuppgifter  
- När jag loggar in  
- Då ska jag se startsidan  

---

### Sprint Backlog
- Urval av stories från Product Backlog för sprinten.  
- Bryts ned i mindre uppgifter (tasks).  
- Teamets plan för sprinten.  

**Exempel:**  
- User Story: "Som användare vill jag kunna registrera konto"  
  - Skapa formulär (8h)  
  - Koppla till databas (6h)  
  - Skriv tester (4h)  

---

### Definition of Done (DoD)
- En gemensam överenskommelse om vad “klart” betyder.  
- Exempel: testat, kodgranskat, dokumenterat, godkänt av PO.  

---

```

**Att tänka på:**  
- Backloggen ska alltid spegla vad som ger mest affärsvärde.  
- DoD ska vara tydlig och gälla för hela teamet.  

---

## Ceremonier

### Sprint Planning
- Syfte: planera vad som ska levereras och hur.  
- Resultat: sprintmål och en sprint backlog.  

### Daily Standup
- Kort synkronisering (15 min).  
- Tre frågor: Vad gjorde jag igår? Vad gör jag idag? Finns det hinder?  

### Sprint Review
- Teamet visar vad som byggts.  
- Stakeholders ger feedback.  
- Backloggen uppdateras utifrån insikter.  

### Sprint Retrospective
- Teamet reflekterar över samarbetet och processen.  
- Identifierar förbättringar att testa i nästa sprint.  

---

## Andra Agila Metoder
- **Kanban:** Fokus på flöde, visualisering och WIP-limits.  
- **Extreme Programming (XP):** Praktiker som TDD, parprogrammering, refaktorering.  
- **Lean Software Development:** Inspirerad av lean manufacturing. Fokus på att eliminera slöseri.  

> **Snabb jämförelse Scrum vs Kanban**  
>
> | Aspekt | Scrum | Kanban |
> |---|---|---|
> | Tidsram | Sprintar (2–4 v) | Kontinuerligt flöde |
> | Planering | Sprint Planning | Löpande prioritering |
> | Roller | PO, SM, Team | Inga formella roller krävs |
> | WIP | Implicit via sprintmål | Explicit WIP-limit per kolumn |
> | Förändring under iteration | Ovanligt | Tillåtet när som helst |

---

## Vanliga Utmaningar
- **Motstånd mot förändring:** börja smått, visa värde, utbilda.  
- **Svag Product Owner:** viktigt med tid, mandat och kunskap.  
- **Stora user stories:** använd INVEST-kriterier för att dela upp.  
- **Estimationsproblem:** använd relativa mått (story points) och lär av velocity.  

---

## Verktyg
- **Projekthantering:** Jira, Trello, Azure DevOps, GitHub Projects.  
- **Kommunikation:** Slack, Microsoft Teams, Discord.  
- **Dokumentation:** Confluence, Notion, GitHub Wiki.  
- **Retrospectives:** Miro, FunRetro, Retrium.  

---

## Mäta Framgång
- **Kvantitativt:** Velocity, burndown charts, lead time.  
- **Kvalitativt:** Teamets trivsel, kundnöjdhet.  
- **Tekniskt:** Antal buggar, test coverage, leveransfrekvens.  

---

## Nycklar till Framgång
1. **Mindset först:** agilt är en filosofi, inte bara möten.  
2. **Investera i människor:** skapa psykologisk trygghet och utbilda.  
3. **Börja smått:** pilotprojekt innan större utrullning.  
4. **Mät & förbättra:** använd retrospectives och data.  

---

## Resurser och Länkar
- 📜 Det Agila Manifestet: <https://agilemanifesto.org/iso/sv/manifesto.html>  
- 🌀 Scrum Guide (officiell): <https://scrumguides.org>  
- 📚 Agile Alliance: <https://www.agilealliance.org>  
- 🔧 Scrum.org: <https://www.scrum.org>  
- 📘 Scaled Agile Framework (SAFe): <https://scaledagileframework.com>  
- 💬 Agila Sverige (community): <https://agilasverige.se>  
