# LAWIM — Politique de Rapport Détaillé Obligatoire

## Principe

Aucun rapport LAWIM ne peut se limiter à une synthèse.

Chaque rapport doit être accompagné de fichiers contenant l'intégralité des
données ayant servi à établir les conclusions.

Le rapport principal sert uniquement de **table des matières et synthèse**.

Toutes les preuves détaillées doivent être enregistrées dans des fichiers
distincts.

## Architecture officielle des rapports

```
docs/

reviews/

    REPORT_INDEX.md                          ← index global de tous les rapports

    <mission>/

        REPORT.md                            ← résumé exécutif uniquement
        TRACEABILITY.md                      ← matrice assertion → contrôle → fichier → SHA256

        details/
            git-details.md
            tests-details.md
            corpus-details.md
            runtime-details.md
            web-details.md
            telegram-details.md
            whatsapp-details.md
            sqlite-details.md
            postgresql-details.md
            ovh-details.md
            logs-details.md

        evidence/
            manifest.json                    ← catalogue des preuves
            SHA256SUMS                       ← sommes de contrôle

            raw/                             ← fichiers bruts (logs, XML, traces)
            normalized/                      ← données normalisées
```

## Identifiant unique des contrôles

Chaque contrôle reçoit un identifiant unique selon le format suivant :

```
GIT-0001
TEST-0001
TEST-0002
OVH-0001
WEB-0001
TG-0001
WA-0001
SQLITE-0001
PG-0001
CORPUS-0001
RUNTIME-0001
```

Le rapport principal ne doit pas écrire uniquement `Tests PASS` mais :

```text
Tests PASS

Preuves :

TEST-0001
TEST-0002
```

Chaque identifiant pointe vers le fichier de détail correspondant.

## Interdiction des preuves uniquement terminales

Les sorties terminales sont considérées comme éphémères.

Elles ne constituent jamais une preuve officielle.

Toute information utilisée pour justifier un verdict doit être persistée dans
un fichier versionné du dépôt.

Une information affichée uniquement dans le terminal est réputée non prouvée.

## Rapport = synthèse

Le rapport principal ne doit jamais dépasser quelques pages.

Il contient uniquement :

- résumé du périmètre
- verdicts par catégorie
- liens vers les fichiers de détail
- identifiants des contrôles

Toutes les sorties détaillées vont dans `details/` ou `evidence/`.

## Une affirmation = une preuve

Chaque phrase du rapport principal doit pouvoir être reliée à un fichier.

Exemple correct :

```text
OVH PASS

Voir :

details/ovh-details.md

Contrôles :

OVH-0001
OVH-0002
```

Interdiction d'écrire `OVH PASS` sans référence.

## Matrice de traçabilité

Chaque mission doit contenir un fichier `TRACEABILITY.md` dans le dossier de
mission.

Format :

```text
| Assertion | Contrôle | Fichier | SHA256 |
| --------- | -------- | ------- | ------ |
| OVH reachable | OVH-0001 | details/ovh-details.md | a1b2c3... |
| Tests PASS | TEST-0001 | details/tests-details.md | d4e5f6... |
```

Toute assertion du rapport principal doit avoir une ligne dans cette matrice.

## Manifeste des preuves

Le fichier `evidence/manifest.json` catalogue chaque preuve.

Format de chaque entrée :

```json
{
  "control_id": "TEST-0001",
  "category": "tests",
  "path": "details/tests-details.md",
  "size": 12345,
  "sha256": "a1b2c3d4e5f6...",
  "created_at": "2026-07-26T12:00:00Z",
  "generated_by": "opencode-agent"
}
```

## Index global des rapports

Le fichier `docs/reviews/REPORT_INDEX.md` est l'index officiel de tous les
rapports produits par LAWIM.

Chaque rapport doit obligatoirement y apparaître.

Format :

```text
| Date | Mission | Commit | Branche | Rapport | Détails | Evidence | Verdict |
| ---- | ------- | ------ | ------- | ------- | ------- | -------- | ------- |
```

L'index est mis à jour automatiquement après chaque nouvelle mission.

## Structure obligatoire (récapitulatif)

```
docs/reviews/<mission>/

    REPORT.md                     ← résumé exécutif uniquement
    TRACEABILITY.md               ← matrice assertion → contrôle → fichier → SHA256

    details/
        git-details.md
        ovh-details.md
        tests-details.md
        web-details.md
        telegram-details.md
        whatsapp-details.md
        sqlite-details.md
        postgresql-details.md
        corpus-details.md
        runtime-details.md
        logs-details.md

    evidence/
        manifest.json
        SHA256SUMS

        raw/                       ← fichiers bruts (logs, XML, traces)
        normalized/                ← données normalisées
```

## Contenu du rapport principal

Le rapport principal est **court**. Exemple :

```text
Git ............... PASS
→ voir details/git-details.md

Tests ............. PASS
→ voir details/tests-details.md

Corpus ............ PARTIAL
→ voir details/corpus-details.md

OVH ............... PASS
→ voir details/ovh-details.md
```

Aucune longue sortie terminale ne doit être copiée dans `REPORT.md`. Chaque
affirmation doit pointer vers un fichier de détail.

## Contenu de chaque fichier de détail

### git-details.md

- commandes exécutées
- sorties complètes
- HEAD
- branches
- tags
- diff
- fichiers modifiés
- commit
- push
- hashes

### tests-details.md

Pour chaque suite :

- commande exacte
- nombre collecté
- nombre exécuté
- PASS
- FAIL
- SKIP
- durée
- stdout complet
- stderr complet
- junit

### corpus-details.md

Ne jamais écrire uniquement `100 certified / 100 repairable / 800 rejected`.

Contenu obligatoire :

- statistiques globales
- statistiques par bloc
- statistiques par langue
- statistiques par canal
- statistiques par catégorie
- liste complète des conversations certifiées
- liste complète des conversations réparables
- liste complète des conversations rejetées
- raison exacte de chaque rejet

### web-details.md

Pour chaque scénario :

- entrée utilisateur
- réponse
- état avant
- état après
- action métier
- object_id
- restart
- idempotence

### telegram-details.md

Même niveau de détail. Inclure :

- event_id
- update_id
- payload anonymisé
- réponse
- logs
- restart
- duplicate

### whatsapp-details.md

Même principe que telegram-details.md.

### sqlite-details.md

Inclure :

- schéma
- tables
- contenu utile
- conversations
- restauration après restart

### postgresql-details.md

Inclure :

- requêtes SQL
- résultats
- object_id
- conversation_id anonymisé
- preuve d'idempotence

### runtime-details.md

Décrire précisément :

- runtime actif
- moteur appelé
- services utilisés
- repositories utilisés
- chemins canoniques
- checksum runtime

### logs-details.md

Ne jamais tronquer les logs. Fournir :

- logs complets
- logs filtrés
- erreurs
- warnings
- stack traces éventuelles

## Règle d'affirmation

Chaque affirmation du rapport principal **doit** pointer vers un fichier de
détail.

```text
Tests : PASS

Voir :

details/tests-details.md
raw/tests/junit.xml
raw/tests/stdout.txt
```

## Interdictions

- Ne jamais répondre uniquement `PASS` sans fichier de preuve.
- Ne jamais répondre uniquement `Production validée` sans preuve détaillée.
- Ne jamais copier de longue sortie terminale dans `REPORT.md`.
- Ne jamais utiliser une sortie terminale comme preuve unique.
- Ne jamais émettre un verdict sans identifiant de contrôle.

## Vérification finale obligatoire

La sortie terminale doit afficher :

```text
REPORT :
DETAILS_DIRECTORY :

Git details :
Tests details :
Corpus details :
OVH details :
Web details :
Telegram details :
WhatsApp details :
SQLite details :
PostgreSQL details :
Runtime details :
Logs details :

Raw evidence :
Manifest :
SHA256SUMS :
```

Si un fichier de détail manque, le contrôle correspondant est déclaré :

```text
UNPROVEN
```

et non `PASS`.

## Sanction

Tout rapport produit sans respecter cette structure sera rejeté et devra être
reproduit intégralement avant toute prise de décision.
