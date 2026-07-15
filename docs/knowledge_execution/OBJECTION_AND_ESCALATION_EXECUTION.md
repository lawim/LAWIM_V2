# OBJECTION AND ESCALATION EXECUTION

**Statut :** Gold Standard
**Source :** `docs/lawim_heritage_gold/CONVERSATION_MODEL.md` (§16, §17, §20)
**Rôle :** Conversation Execution Architect — Définit la gestion des objections et l'escalade humaine.

---

## 1. Catalogue des objections

### 1.1 Peurs acheteurs (12)

| # | Peur / Objection | Mots-clés de détection | Catégorie | Réf. Heritage |
|:-:|------------------|------------------------|-----------|:-------------:|
| 1 | Arnaque | "arnaque", "scam", "faux", "tromper", "pas sûr" | Confiance | CONV-021 |
| 2 | Qualité du bien | "état", "dégât", "abîmé", "propre", "rénové" | Qualité | CONV-021 |
| 3 | Prix trop élevé | "trop cher", "cher", "overpriced", "hors budget" | Prix | CONV-021 |
| 4 | Quartier dangereux | "quartier", "insécurité", "dangereux", "safety" | Environnement | CONV-021 |
| 5 | Absence de titre foncier | "titre foncier", "papier", "document", "land title" | Légal | CONV-021 |
| 6 | Vices cachés | "vice caché", "problème", "caché", "hidden" | Légal | CONV-021 |
| 7 | Litige | "litige", "dispute", "conflit", "héritage" | Légal | CONV-021 |
| 8 | Voisinage | "voisin", "voisinage", "bruit", "calme" | Environnement | CONV-021 |
| 9 | Accessibilité | "transport", "route", "accès", "parking" | Pratique | CONV-021 |
| 10 | Financement | "prêt", "crédit", "financement", "banque" | Financier | CONV-021 |
| 11 | Délai | "délai", "quand", "longtemps", "quand disponible" | Temporel | CONV-021 |
| 12 | Revente | "revente", "plus-value", "investissement" | Investissement | CONV-021 |

### 1.2 Peurs vendeurs (8)

| # | Peur / Objection | Mots-clés de détection | Catégorie | Réf. Heritage |
|:-:|------------------|------------------------|-----------|:-------------:|
| 1 | Prix trop bas | "sous-évalué", "trop bas", "pas assez", "low price" | Prix | CONV-021 |
| 2 | Délai trop long | "trop long", "vite", "rapidement", "slow" | Temporel | CONV-021 |
| 3 | Confidentialité | "confidentiel", "privé", "private", "secret" | Confiance | CONV-021 |
| 4 | Arnaque | "arnaque", "scam", "faux agent" | Confiance | CONV-021 |
| 5 | Visites sans filtre | "n'importe qui", "visite libre", "tout le monde" | Contrôle | CONV-021 |
| 6 | Commission cachée | "commission", "frais caché", "hidden fee" | Financier | CONV-021 |
| 7 | Pas d'acquéreur sérieux | "pas sérieux", "time-waster", "perte de temps" | Confiance | CONV-021 |
| 8 | Paperasse | "papier", "administratif", "document", "paperwork" | Légal | CONV-021 |

---

## 2. Détection des objections

### 2.1 Pipeline de détection

```
Message entrant
    │
    ├── Fact Extractor → extraction entités
    │
    ├── Intent Detector → classification intention
    │
    └── Objection Detector → matching contre catalogue
         │
         ├── Regex mots-clés (FR, EN, PID)
         ├── DeepSeek analyse sémantique (objection implicite)
         └── Pattern contextuel (historique objections)
              │
              ▼
         ObjectionMatch {
           objection_id: string;    // O-01 à O-20
           category: string;        // Confiance | Qualité | Prix | ...
           confidence: number;      // 0.0 - 1.0
           previous_count: number;  // nombre d'occurrences dans la session
           turn_number: number;     // tour actuel pour cette objection
         }
```

### 2.2 Scoring de détection

| Méthode | Poids | Déclenchement |
|---------|:-----:|---------------|
| Regex directe (mot-clé exact) | 0.8 | Correspondance immédiate |
| Regex partielle (racine de mot) | 0.6 | "arnaq" → "arnaque" |
| DeepSeek sémantique | 0.7 - 0.95 | "J'ai peur de me faire avoir" → arnaque |
| Pattern contextuel | 0.5 | "Vous pourriez vérifier" → méfiance |

Seuil de détection : **confidence ≥ 0.65**

---

## 3. Cartographie réponse-objection

### 3.1 Réponses aux objections acheteurs

| # | Objection | Réponse type (FR) | Réponse type (EN) | Principe |
|:-:|-----------|-------------------|-------------------|----------|
| O-01 | Arnaque | "LAWIM vérifie chaque annonce avant publication. Nous sommes un intermédiaire déclaré, pas une plateforme anonyme." | "LAWIM verifies every listing before publication. We are a registered intermediary." | Rassurance institutionnelle |
| O-02 | Qualité du bien | "Je vous invite à visiter le bien pour vous faire votre propre avis. Les photos sont disponibles sur demande." | "I invite you to visit the property to form your own opinion." | Transparence + action |
| O-03 | Prix trop élevé | "Le prix est fixé par le propriétaire. Je peux vous montrer d'autres biens dans votre budget." | "The price is set by the owner. I can show you other properties within your budget." | Alternatives positives |
| O-04 | Quartier dangereux | "Je comprends votre souci. Je vous suggère de visiter le quartier à différents moments de la journée." | "I understand your concern. I suggest visiting the area at different times of day." | Empathie + conseil |
| O-05 | Absence titre foncier | "Je vous recommande de vérifier le titre foncier auprès du cadastre avant tout engagement. Un notaire peut vous assister." | "I recommend verifying the land title at the land registry. A notary can assist you." | Redirection notaire |
| O-06 | Vices cachés | "Une visite avec un expert peut vous rassurer. Je reste à votre disposition pour organiser cela." | "A visit with an expert can reassure you. I'm available to arrange that." | Solution proactive |
| O-07 | Litige | "Si vous suspectez un litige, je vous recommande de consulter un notaire avant d'aller plus loin." | "If you suspect a dispute, I recommend consulting a notary before proceeding." | Redirection notaire |
| O-08 | Voisinage | "Je comprends. Puis-je vous proposer des biens dans des quartiers que vous préférez ?" | "I understand. Can I suggest properties in neighborhoods you prefer?" | Écoute + alternative |
| O-09 | Accessibilité | "Quels sont vos critères d'accessibilité ? Transports en commun, routes, parking ?" | "What are your accessibility criteria? Public transport, roads, parking?" | Clarification + collecte |
| O-10 | Financement | "LAWIM ne propose pas de prêt, mais je peux vous orienter vers des partenaires bancaires." | "LAWIM does not provide loans, but I can refer you to banking partners." | Orientation partenaire |
| O-11 | Délai | "Le bien est disponible immédiatement. Pour la visite, je peux organiser cela sous 48h." | "The property is available immediately. I can arrange a visit within 48 hours." | Réponse précise + rapide |
| O-12 | Revente | "Ce bien se trouve dans un secteur avec une bonne plus-value. Je peux vous montrer les tendances du marché." | "This property is in an area with good appreciation. I can show market trends." | Données + confiance |

### 3.2 Réponses aux objections vendeurs

| # | Objection | Réponse type (FR) | Réponse type (EN) | Principe |
|:-:|-----------|-------------------|-------------------|----------|
| O-13 | Prix trop bas | "L'estimation est basée sur une analyse de marché. Je peux vous détailler les critères." | "The estimate is based on market analysis. I can detail the criteria." | Transparence data |
| O-14 | Délai trop long | "La durée moyenne de vente dans votre secteur est de [X] mois. Nous optimisons la visibilité." | "The average selling time in your area is [X] months. We optimize visibility." | Data + optimisation |
| O-15 | Confidentialité | "Vos informations restent confidentielles. Aucune donnée n'est partagée sans votre accord." | "Your information remains confidential. No data is shared without your consent." | CONV-006, CONV-012 |
| O-16 | Arnaque (vendeur) | "LAWIM est un intermédiaire déclaré. Vous pouvez vérifier notre registre." | "LAWIM is a registered intermediary. You can verify our registration." | Transparence légale |
| O-17 | Visites sans filtre | "Nous pré-qualifions chaque visiteur avant de planifier une visite. Vous gardez le contrôle." | "We pre-qualify every visitor before scheduling a visit. You stay in control." | Contrôle + filtrage |
| O-18 | Commission cachée | "LAWIM ne prend aucune commission sur les transactions. Zéro frais cachés." | "LAWIM takes no commission on transactions. Zero hidden fees." | CONV-002 |
| O-19 | Acquéreur non sérieux | "Nous qualifions chaque acheteur avant la mise en relation. Pas de visites inutiles." | "We qualify every buyer before connecting. No wasted visits." | Qualification + sérieux |
| O-20 | Paperasse | "Nous vous assistons dans les démarches administratives. Un notaire peut finaliser le transfert." | "We assist with administrative procedures. A notary can finalize the transfer." | Accompagnement |

---

## 4. Stratégie multi-tour pour objections persistantes

### 4.1 Cycles de réponse

```
Tour 1 (objection détectée) :
    └─ Réponse standard (voir §3) + relance positive

Tour 2 (même objection, même session) :
    └─ Empathie renforcée + donnée concrète + alternative
       "Je comprends tout à fait votre prudence concernant [sujet].
        Voici ce que je peux vous proposer : [solution concrète].
        Souhaitez-vous explorer cette option ?"

Tour 3 (même objection, même session, utilisateur insatisfait) :
    └─ Proposition d'escalade humaine
       "Je comprends que cela nécessite plus d'attention.
        Puis-je demander à un conseiller de vous contacter ?"
```

### 4.2 Règles d'engagement

| Situation | Action | Limite |
|-----------|--------|:------:|
| Objection persistante (3 tours) | Proposer escalade humaine | 3 occurrences |
| Objection + urgence | Escalade immédiate | 1 occurrence |
| Objection juridique (titre, litige) | Rediriger notaire + escalade si persistant | 2 occurrences |
| Objection financière (prix, commission) | Data + CONV-002 (zéro commission) | 3 occurrences |
| Objection confiance (arnaque) | Transparence + registre + témoignages | 2 occurrences |

---

## 5. Critères d'escalade humaine

### 5.1 Déclencheurs absolus (escalade immédiate)

| # | Condition | Action | Destinataire | Réf. |
|:-:|-----------|--------|--------------|:----:|
| E-01 | Question juridique explicite | "Je vous recommande de consulter un notaire" + escalade | Notaire | CONV-022 |
| E-02 | Commande SIGNALER | Créer dispute + escalade support | Support team | CONV-020, CONV-022 |
| E-03 | Demande explicite de parler à un humain | Transférer au conseiller disponible | Conseiller | CONV-022 |
| E-04 | Signalement d'urgence suspect | Vérification manuelle | Équipe sécurité | CONV-022 |
| E-05 | Menace / insulte / contenu illégal | Blocage + signalement | Modération | CONV-022 |

### 5.2 Déclencheurs progressifs (seuils)

| # | Condition | Seuil | Action | Réf. |
|:-:|-----------|:-----:|--------|:----:|
| E-06 | Objection persistante non résolue | 3 tours | Escalade conseiller | CONV-021 |
| E-07 | Échecs de qualification consécutifs | 3 échecs | Escalade manuelle | CONV-022 |
| E-08 | Feedback 👎 persistant | 3 occurrences | Escalade support | CONV-022, CONV-023 |
| E-09 | 3 messages sans information nouvelle | 3 tours silence info | Arrêt qualification (stop implicite) | CONV-020 §20 |
| E-10 | Stop explicite utilisateur | "Merci, ça suffit" | Arrêt immédiat + archiver | CONV-020 §20 |

---

## 6. Protocole de handover

### 6.1 Séquence de transfert

```
1. DÉTECTION du besoin d'escalade (E-01 à E-10)
    │
2. NOTIFICATION utilisateur :
    "Je transmets votre demande à un conseiller. Vous serez contacté sous 24h."
    │
3. CRÉATION du ticket d'escalade :
    {
      escalation_id: UUID,
      reason: string,           // Code déclencheur (E-01..E-10)
      actor_id: string,
      session_id: string,
      conversation_summary: string,  // Résumé des échanges
      objection_history: ObjectionMatch[],
      priority: 'low' | 'normal' | 'high' | 'critical',
      timestamp: ISO 8601,
      assigned_to: string | null     // Conseiller cible
    }
    │
4. ROUTAGE vers le conseiller :
    - high/critical → notification immédiate (push/email)
    - normal → file d'attente CRM
    - low → traitement différé (24h max)
    │
5. TRACABILITÉ : événement escalation_triggered
    │
6. CLÔTURE du tour bot : turn final avec message d'attente
```

### 6.2 Informations incluses dans le handover

| Information | Source | Obligatoire |
|-------------|--------|:-----------:|
| Actor ID | Identity Resolver | Oui |
| Canal d'origine | Channel Normalizer | Oui |
| Langue | Fact Extractor | Oui |
| Intention détectée | Intent Detector | Oui |
| Résumé de conversation | Context Loader | Oui |
| Entités collectées | Fact Extractor | Oui |
| Objections soulevées | Objection Detector | Oui |
| Score de satisfaction | Turn Persister | Si disponible |
| Niveau de familiarité (J1-J4) | Context Loader | Oui |

### 6.3 Règles de handover

| # | Règle | Réf. |
|:-:|-------|:----:|
| 1 | Ne jamais mentionner "escalade" ou "transféré à un humain" dans le message utilisateur | CONV-014 |
| 2 | Formuler comme "Je transmets à mon équipe" ou "Un conseiller vous contacte" | CONV-003 |
| 3 | Le résumé de conversation doit être en français, même si la conversation était en EN/PID | Standard |
| 4 | Le handover doit être tracé dans les événements de traçabilité | §6 CONV |
| 5 | Le bot reste actif pour des questions simples même après escalade (reprise possible) | CONV-010 |

---

## 7. Gestion des objections par profil d'utilisateur

### 7.1 Adaptation selon le niveau de familiarité

| Niveau | Approche objection | Exemple |
|:------:|-------------------|---------|
| **J1** | Réponse standard + éducation | "LAWIM vérifie chaque annonce..." |
| **J2** | Réponse personnalisée + historique | "Je vois que vous avez déjà visité des biens à Douala..." |
| **J3** | Réponse experte + donnée | "Dans ce secteur, le prix moyen au m² est de X FCFA..." |
| **J4** | Priorité + offre spéciale | "En tant que client prioritaire, je peux vous organiser une visite exclusive..." |

### 7.2 Adaptation selon le canal

| Canal | Traitement objection |
|-------|----------------------|
| WhatsApp | Réponse courte + 1 solution, pas de détail |
| Telegram | Réponse concise + boutons d'action |
| Dashboard | Réponse complète + documentation |
| SMS | Réponse minimale + renvoi vers canal principal |

---

*Document patrimonial Gold — Toute reconstruction doit respecter ce modèle validé.*
