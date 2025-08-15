# CI/CD-verktyg: Alternativ till GitHub Actions

I kursen fokuserar vi på GitHub Actions, men det är viktigt att förstå det bredare landskapet av CI/CD-verktyg som används i industrin.

## Populära CI/CD-verktyg

| Verktyg | Typ | Användning | Fördelar | Nackdelar |
|---------|-----|------------|----------|-----------|
| **GitHub Actions** | Cloud SaaS | Integrerat med GitHub | Enkel setup, gratis för öppen källkod | Låst till GitHub |
| **Jenkins** | Self-hosted | Stora företag, legacy systems | Mycket flexibel, plugins för allt | Krånglig setup, underhåll |
| **GitLab CI** | Cloud/Self-hosted | GitLab-baserade projekt | Inbyggt i GitLab, kraftfullt | Måste använda GitLab |
| **Azure DevOps** | Cloud SaaS | Microsoft-ekosystem | Bra Azure-integration | Microsoft-fokuserat |
| **CircleCI** | Cloud SaaS | Startup/mid-size företag | Snabb, bra performance | Kan bli dyrt |
| **TeamCity** | Self-hosted | JetBrains-ekosystem | Professionell, kraftfull | Komplicerad, kostnad |

---

## Cloud-specifika CI/CD-verktyg

Varje stor cloud-leverantör har sina egna verktyg:

### **AWS:**
- **CodePipeline** - Orchestrering av hela release-processen
- **CodeBuild** - Build service för kompilering och testning
- **CodeDeploy** - Automatisk deployment till EC2, Lambda, etc.
- **CodeCommit** - Git-baserad source control

### **Google Cloud:**
- **Cloud Build** - Build och test i Google Cloud
- **Cloud Deploy** - Release management och deployment
- **Cloud Source Repositories** - Git repositories

### **Azure:**
- **Azure Pipelines** - Komplett CI/CD-lösning
- **Azure Repos** - Git repositories
- **Azure Artifacts** - Package management

---

## Detaljerad jämförelse

### Jenkins
**Fördelar:**
- Extremt flexibel med tusentals plugins
- Kan köras on-premise med full kontroll
- Stor community och support
- Gratis och open source

**Nackdelar:**
- Komplicerad setup och underhåll
- Kräver dedikerade servrar
- Säkerhetsuppdateringar och backups är ditt ansvar
- Kan bli långsam med många builds

**Vanlig användning:** Stora företag med dedikerade DevOps-team och specifika säkerhetskrav.

### GitLab CI
**Fördelar:**
- Helt integrerat med GitLab (kod, issues, CI/CD i samma plattform)
- Kraftfull pipeline-syntax
- Bra för både cloud och self-hosted
- Inbyggda säkerhetsskanning och dependency management

**Nackdelar:**
- Måste använda GitLab som Git-provider
- Kan vara dyrt för stora team
- Lärningskurva för avancerade pipelines

**Vanlig användning:** Team som vill ha allt-i-ett-lösning från kod till deployment.

### CircleCI
**Fördelar:**
- Snabb execution och bra performance
- Docker-first approach
- Elegant UI och bra användarupplevelse
- Parallellisering av builds

**Nackdelar:**
- Kan bli dyrt för stora projekt
- Mindre flexibel än Jenkins
- Begränsade customization-möjligheter

**Vanlig användning:** Snabbt växande tech-företag som värdesätter hastighet och enkelhet.

---

## Faktorer att överväga vid val av CI/CD-verktyg

### 1. **Integration med befintliga verktyg**
- Vilken Git-provider använder ni? (GitHub, GitLab, Bitbucket)
- Vilken cloud-leverantör? (AWS, GCP, Azure)
- Befintliga monitoring och deployment-verktyg?

### 2. **Team-storlek och expertis**
- Små team: Managed services (GitHub Actions, CircleCI)
- Stora team med DevOps-expertis: Jenkins, självhostade lösningar
- Blandade färdigheter: Cloud-baserade lösningar med bra UI

### 3. **Säkerhets- och compliance-krav**
- Finansiella tjänster: Ofta kräver on-premise eller privata clouds
- Startups: Cloud-baserade lösningar räcker oftast
- Healthcare/Government: Specifika compliance-krav

### 4. **Budget och kostnad**
- **Gratis alternativ:** Jenkins (kräver egen infrastructure), GitHub Actions (för publika repos)
- **Betalt per användare:** GitLab, Azure DevOps
- **Betalt per build-minut:** CircleCI, GitHub Actions (privata repos)

### 5. **Skalbarhet**
- Hur många builds per dag?
- Behov av parallella builds?
- Internationell distribution?

---

## Bransch-trender

### **Små till medelstora företag (Startups → 100 anställda)**
- **Populärt:** GitHub Actions, CircleCI, GitLab CI
- **Varför:** Snabb setup, managed service, fokus på utveckling

### **Stora företag (500+ anställda)**
- **Populärt:** Jenkins, Azure DevOps, GitLab Enterprise
- **Varför:** Anpassningsbarhet, säkerhetskontroll, integration med legacy-system

### **Cloud-native företag**
- **AWS-fokus:** CodePipeline + CodeBuild
- **GCP-fokus:** Cloud Build
- **Azure-fokus:** Azure Pipelines
- **Multi-cloud:** GitHub Actions eller GitLab CI

---

## Varför GitHub Actions för denna kurs?

Vi fokuserar på GitHub Actions eftersom:

- ✅ **Enkel att komma igång** - Ingen extern setup krävs
- ✅ **Gratis för lärande** - Publika repos och student-konton
- ✅ **Modern syntax** - YAML-baserat, lättläst och versionshanterat
- ✅ **Stora community** - Tusentals färdiga actions att återanvända
- ✅ **Branschstandard** - Används av många moderna företag
- ✅ **Bra dokumentation** - Microsoft investerar tungt i utvecklarupplevelsen

## Det viktiga att komma ihåg

**Koncepten är överförbara!** Lär dig GitHub Actions ordentligt och du kommer lätt kunna:

- Migrera till Jenkins när du börjar på ett företag som använder det
- Förstå Azure Pipelines om ditt team kör på Microsoft-stack
- Anpassa dig till CircleCI eller GitLab CI vid behov

**Grundprinciperna** - triggers, jobs, steps, artifacts, environments - är **samma** oavsett verktyg. Det som skiljer är syntax och specifika funktioner.

Fokusera på att förstå CI/CD-koncepten djupt, så kommer verktygen att vara enkla att växla mellan! 
