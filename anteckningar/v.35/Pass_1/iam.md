# GCP IAM – Grundläggande anteckningar

## Vad är IAM?
Identity and Access Management (IAM) i Google Cloud Platform styr **vem** (identitet) som får göra **vad** (roll/behörighet) **på vilken resurs** (scope: org/mapper/projekt/resurs).

- Identitet (principal): användare, grupp, service account, extern identitet
- Roll: samling av behörigheter (permissions)
- Policy binding: kopplar identitet ↔ roll ↔ resurs
- Ärvs nedåt i resurs‑hierarkin: Organisation → Mapp → Projekt → Resurs

## Centrala begrepp
- Roller:
  - **Basic (primitives)**: Owner/Editor/Viewer (för breda – undvik i produktion)
  - **Predefined**: Googles färdiga, tjänstspecifika roller (rekommenderas)
  - **Custom**: egna roller (minsta möjliga permissions, underhåll krävs)
- Identiteter:
  - Människor: Google‑konton/Cloud Identity
  - Grupper: hantera tilldelning via grupp i stället för individer
  - Service accounts: identitet för jobb/appar

## Bästa praxis (Do)
- **Least privilege**: ge minsta möjliga roll för uppgiften
- **Använd grupper** för mänskliga användare (tilldela roller till gruppen)
- **Separera miljöer** (dev/test/prod) i olika projekt
- **Använd predefined roller** före custom/basic
- **Service accounts för arbetslaster**, inte personliga konton
- **Undvik långlivade nycklar**: använd Workload Identity Federation eller kortlivade token/ADC
- **Aktivera Cloud Audit Logs** (Admin, Data Access där relevant)
- **Regelbunden åtkomst‑review** (t.ex. kvartalsvis)
- **Dokumentera** varför en roll behövs och på vilken nivå
- **Villkor (IAM Conditions)** vid behov: tidsbegränsa, IP‑range, resurs‑taggar

## Vanliga misstag (Don’t)
- Tilldela **Owner/Editor/Viewer** slentrianmässigt
- Ge rättigheter på **för hög nivå** (org/mapp) i stället för projekt
- Dela **service‑account‑nycklar** eller checka in nycklar i repo
- Återanvända **samma SA** i alla miljöer
- Sakna **separation of duties** (t.ex. samma person deployar och godkänner)
- Låta **inaktiva konton** eller behörigheter ligga kvar

## Praktiska tips
- Skapa en **grupp per team** och mappa till roller per projekt
- En **service account per applikation/miljö**, med snäv rolldefinition
- Använd **Folder/Org Policy** för att förbjuda SA‑nycklar, begränsa regioner m.m.
- Tagga resurser och använd **IAM Conditions** på taggar för finmaskig åtkomst
- Rotera behörigheter: sätt **tidsbegränsade** tilldelningar där möjligt

## Små exempel
- Lista IAM‑policy för projekt:
  ```bash
  gcloud projects get-iam-policy <PROJECT_ID>
  ```
- Tilldela en predefined roll till en grupp på projekt:
  ```bash
  gcloud projects add-iam-policy-binding <PROJECT_ID> \
    --member="group:team-data@yourdomain.com" \
    --role="roles/bigquery.dataViewer"
  ```
- Skapa service account och ge snäv roll:
  ```bash
  gcloud iam service-accounts create sa-ingest --display-name "Ingestion SA"
  gcloud projects add-iam-policy-binding <PROJECT_ID> \
    --member="serviceAccount:sa-ingest@<PROJECT_ID>.iam.gserviceaccount.com" \
    --role="roles/storage.objectCreator"
  ```

## Snabb checklista
- [ ] Är rollen minsta möjliga?
- [ ] Är tilldelningen på lägsta rimliga nivå (projekt/resurs)?
- [ ] Är åtkomst given till **grupp** i stället för individer?
- [ ] Använder arbetslaster **service accounts** utan långlivade nycklar?
- [ ] Finns audit logs aktiverat och granskas regelbundet?
- [ ] Finns process för borttag av inaktiva konton/behörigheter?

## Gruppprojekt (enkelt men inte farligt)
- Om ni måste: utse 1–2 som har `Owner` för projektet; ge övriga `Editor` eller specifika predefined roller (t.ex. `roles/storage.admin`, `roles/bigquery.dataEditor`).
- Använd en Google‑grupp (t.ex. `team-<kurs>@…`) och tilldela roller till gruppen i stället för individer.
- Städa efter er: ta bort Owner/Editor när projektet är klart.

## Länkar (officiell dokumentation)
- Översikt IAM: [What is IAM?](https://cloud.google.com/iam/docs/overview)
- Roller: [Understanding roles](https://cloud.google.com/iam/docs/understanding-roles) · [Predefined roles](https://cloud.google.com/iam/docs/understanding-roles#predefined_roles) · [Custom roles](https://cloud.google.com/iam/docs/custom-roles)
- Bästa praxis: [Best practices for IAM](https://cloud.google.com/iam/docs/best-practices)
- Service accounts: [Overview](https://cloud.google.com/iam/docs/service-accounts) · [Best practices](https://cloud.google.com/iam/docs/best-practices-for-using-and-managing-service-accounts)
- Workload Identity Federation: [Overview](https://cloud.google.com/iam/docs/workload-identity-federation)
- IAM Conditions: [Overview](https://cloud.google.com/iam/docs/conditions-overview)
- Audit Logs: [Cloud Audit Logs](https://cloud.google.com/audit-logs/docs/overview)
- Policy Troubleshooter: [Troubleshoot access](https://cloud.google.com/policy-intelligence/docs/policy-troubleshooter)
- gcloud IAM kommandon: [Granting, changing, and revoking access](https://cloud.google.com/iam/docs/granting-changing-revoking-access)
