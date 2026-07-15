# NEGOTIATION MODEL — Modèle de négociation LAWIM

**Sources :** LAWIM `Directive/48-LAWIM-SALES-PLAYBOOK.md`, `KNOWLEDGE/negotiation-patterns.md`, `KNOWLEDGE/trust-and-objection-patterns.md`, `KNOWLEDGE/conversation-style-guide.md`, `KNOWLEDGE/commercial/closing_techniques.md`, `KNOWLEDGE/commercial/objection_handling.md`, `KNOWLEDGE/commercial/negotiation_techniques.md`, `KNOWLEDGE/diaspora-behavior-model.md`, LAWIMA `03_ENGINE/response_router.py`, `multilingual_responses.py`
**Principe :** Documentation exhaustive des connaissances en négociation

---

## 1. Techniques commerciales LAWIM

**Source :** LAWIM `KNOWLEDGE/commercial/` (4 documents)

### 1.1 Closing techniques
Document dédié dans `knowledge_unified/commercial/closing_techniques.md`

### 1.2 Objection handling
Document dédié dans `knowledge_unified/commercial/objection_handling.md`

### 1.3 Negotiation techniques
Document dédié dans `knowledge_unified/commercial/negotiation_techniques.md`

### 1.4 Follow-up strategies
Document dédié dans `knowledge_unified/commercial/follow_up_strategies.md`

## 2. Dynamiques du marché camerounais

**Source :** LAWIM `KNOWLEDGE/negotiation-patterns.md`, `Directive/48-LAWIM-SALES-PLAYBOOK.md`

### 2.1 Profils d'acheteurs camerounais

- **Acheteur national** : sensible au prix, recherche de bonnes affaires, négociation serrée
- **Acheteur diaspora** : pouvoir d'achat plus élevé, recherche de sécurité juridique, confiance essentielle
- **Investisseur** : focalisé sur le rendement, analyse du ROI, horizon long-terme
- **Jeune actif** : budget limité, recherche de primo-accession, flexible sur la localisation

### 2.2 Profils de vendeurs camerounais

- **Vendeur particulier** : attachement émotionnel au bien, méfiance envers les intermédiaires
- **Promoteur** : volume, rotation rapide, marge商业
- **Propriétaire bailleur** : rentabilité locative, gestion locative

### 2.3 Moments clés de l'année

Périodes de forte activité identifiées dans le playbook :
- Fin d'année (diaspora rentre au pays)
- Rentrée scolaire
- Saison sèche (travaux de construction)
- Périodes de transferts d'argent (diaspora)

## 3. Objections et réponses

**Source :** LAWIM `KNOWLEDGE/trust-and-objection-patterns.md`

### 3.1 Peurs des acheteurs (12 identifiées)

1. Arnaque / fraude
2. Titre foncier non valide
3. Prix trop élevé
4. Vices cachés
5. Litige sur le bien
6. Difficultés administratives
7. Mauvaise localisation
8. Problèmes de voisinage
9. Accessibilité (routes, transports)
10. Financement (pas de prêt)
11. Délais trop longs
12. Changement d'avis du vendeur

### 3.2 Peurs des vendeurs (8 identifiées)

1. Ne pas trouver d'acheteur
2. Vendre en dessous du prix du marché
3. Acheteur non solvable
4. Arnaque au paiement
5. Délais de vente trop longs
6. Occupants illégaux
7. Litiges de propriété
8. Biens saisis

### 3.3 Réponses types

Non extraites textuellement ici — voir les documents sources pour les formulations exactes.

## 4. Argumentaires de vente

**Source :** LAWIM `Directive/48-LAWIM-SALES-PLAYBOOK.md`

### 4.1 Arguments LAWIM
- Zéro commission
- Mise en relation directe
- Matching intelligent
- Accompagnement personnalisé (50k FCFA)
- Présence sur WhatsApp (accessible à tous)
- Réseau d'agents vérifiés

### 4.2 Arguments propriétés
- Proximité des commodités
- Accessibilité (routes, transports)
- Sécurité du quartier
- Potentiel de valorisation
- cadre de vie

## 5. Signaux de négociation

**Source :** LAWIMA `03_ENGINE/lawim_engine_v1.py`, `02_KNOWLEDGE/whatsapp_language/negotiation.json`

### 5.1 Expressions de négociation de prix

- `prix ferme` : prix non négociable
- `à débattre` : prix négociable
- `dernier prix` : ultime proposition
- `je peux descendre` : marge de négociation
- `c'est trop cher` :反对 prix
- `faites moi une offre` : invite à négocier

### 5.2 Signaux d'urgence

- `urgent` : besoin rapide
- `asap` : urgence
- `vite` : urgence
- `immédiatement` : urgence
- `now` : urgence

### 5.3 Signaux d'investisseur

- `investir` : intention d'investissement
- `rentable` : recherche de rentabilité
- `ROI` : retour sur investissement
- `cash flow` : flux de trésorerie
- `rendement` : recherche de rendement

### 5.4 Signaux diaspora

- `diaspora` : indication d'appartenance
- `je vis à` + pays étranger
- Indicatifs téléphoniques étrangers (+33, +1, +44, etc.)
- Références à des villes étrangères (Paris, Londres, New York)

## 6. Psychologie de la vente

**Source :** LAWIM `KNOWLEDGE/commercial/conversation_tone.md`

### 6.1 Principes de ton
- Professionnel mais chaleureux
- Expertise rassurante
- Patience et écoute
- Adaptation au rythme du client
- Validation des émotions du client

### 6.2 Séquence de confiance
1. Écoute active → reformulation
2. Apport d'information → démonstration d'expertise
3. Proposition → solution adaptée
4. Traitement des objections → réassurance
5. Closing → passage à l'action

## 7. Relance commerciale

**Source :** LAWIMA `03_ENGINE/follow_up_system.py`

### 7.1 Calendrier de relance

| J+ | Message |
|----|---------|
| 1 | Nouveaux biens correspondant à la recherche |
| 7 | Offre spéciale, nouveaux arrivages |
| 30 | Statistiques du marché, tendances |
| 90 | Relance complète, réactivation |

### 7.2 Messages de relance types

**J1** : "Bonjour [nom], j'ai trouvé [N] nouveaux biens correspondant à votre recherche à [ville]..."
**J7** : "Bonjour [nom], une offre spéciale cette semaine sur [type] à [ville]..."
**J30** : "Bonjour [nom], voici les tendances du marché immobilier à [ville] ce mois-ci..."
**J90** : "Bonjour [nom], votre recherche est toujours active ? J'ai [N] nouveaux biens à vous proposer..."

## 8. Prise de rendez-vous

**Source :** LAWIM `KNOWLEDGE/commercial/closing_techniques.md`

Techniques de prise de rendez-vous décrites dans le document source.

## 9. Sales Playbook complet

**Source :** LAWIM `Directive/48-LAWIM-SALES-PLAYBOOK.md`

Document complet de 22 sections dédié aux ventes LAWIM (non détaillé ici, voir la source).

## 10. Marque et branding

**Source :** LAWIM `Directive/LAWIM-BRAND-BOOK.md`

Charte graphique et guide de marque LAWIM — document source à consulter pour les détails.

---

*Document patrimonial — Aucune décision de reconstruction n'est prise ici.*
