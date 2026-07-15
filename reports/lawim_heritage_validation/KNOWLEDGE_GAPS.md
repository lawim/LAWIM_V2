# KNOWLEDGE GAPS — Lacunes de Connaissance dans le Patrimoine

**Statut :** Lacunes documentées par KNOWLEDGE_COVERAGE_MATRIX.md et quality_report.md

---

## 1. Domaines les Moins Aboutis (KNOWLEDGE_COVERAGE_MATRIX.md §3)

| Rang | Domaine | Lacune Identifiée | Gravité |
|------|---------|------------------|---------|
| 1 | **Négociation** | Playbook existe mais pas de règles structurées exploitables | Haute |
| 2 | **Monétisation** | Feature flags désactivés, logique partielle | Haute |
| 3 | **Fraude** | 25 signaux documentés mais pas de règles de détection automatisées | Haute |
| 4 | **Partenaires externes** | Rôles listés mais pas de processus associés | Moyenne |
| 5 | **Workflows avancés** | États et événements définis mais pas de règles de transition | Moyenne |

---

## 2. Lacunes Techniques Identifiées

### Absence de Sources Implémentation

| Technologie | Source manquante | Impact |
|-------------|-----------------|--------|
| Python engine | 15 fichiers 03_ENGINE/*.py | Perte de toute la logique d'implémentation |
| Règles JSON | 5 versions RULE_ENGINE_V*.json | Perte de l'évolution des règles |
| Feature flags | FEATURE_FLAGS.json | Perte de la matrice des fonctionnalités |
| Config IA | 6 fichiers 06_AI_MODELS/*.json | Perte des modèles IA |
| SQL | implement_all.sql, setup_database.sql | Perte des schémas de base de données |
| CSV runtime | 6 fichiers runtime/*.csv | Perte des données d'exemple |
| CSV Supabase | 9 fichiers ready_for_supabase/*.csv + supabase_ready/*.csv | Perte des données préparées |
| CSV templates | 5 fichiers templates/*.csv | Perte des templates |
| CamPay config | CAMPAY_CONFIG.json | Perte de la configuration de paiement |
| GreenAPI config | GREEN_API_CONFIG.json | Perte de la configuration WhatsApp |

---

## 3. Lacunes de Couverture (quality_report.md)

| Domaine | Qualité Rapportée | Gaps |
|---------|------------------|------|
| Géographie | HIGH | GPS quartiers non incorporé. 3 fichiers .txt (districts manquants) non traités. |
| Qualification | HIGH | Backlog implémentation (14.3KB) non entièrement implémenté. |
| Matching | HIGH | Rayons de mobilité par défaut non définis. |
| Langage | HIGH | Tags de canal non appliqués aux expressions. |
| Commercial | HIGH | Règles omnicanales partiellement appliquées. |
| Immobilier | NEW | Taxonomie en cours de création. |
| Professionnels | NEW | Catégories en cours de définition. |
| Légal | NEW | En cours de création. |

---

## 4. Lacunes de Traçabilité

| Connaissance | HERITAGE_INDEX.md | TRACEABILITY_MATRIX.md | knowledge_unified/ |
|-------------|------------------|----------------------|-------------------|
| Feature flags | §8 unique | Non tracé | Absent |
| Anti-spam | §6 concept | Non tracé | Absent |
| Rule engine V2-V5 | §7 dupliqué | Non tracé | Absent |
| Monétisation | §8 unique | Non tracé | Absent |
| Identity resolution | §8 unique | Non tracé | Absent |
| Data quality engine | §8 unique | Non tracé | Absent |

---

## 5. Formats non Exploitables

| Fichier | Format | Contenu présumé |
|---------|--------|-----------------|
| 4-Matching Engine LAWIM.docx | DOCX | Architecture matching |
| 3-Request Engine - Module 3.docx | DOCX | Architecture request engine |
| Documents financiers (07_DOCUMENTATION/finance/) | DOCX | Données financières |
| Documents marketing (07_DOCUMENTATION/marketing/) | ODT | Contenu marketing |
| Documents techniques (07_DOCUMENTATION/technical/) | DOCX | Documentation technique |

---

## 6. Recommandations

1. **Priorité Haute** : Restaurer les fichiers 03_ENGINE/ et 08_CONFIG/ depuis une sauvegarde externe
2. **Priorité Haute** : Restaurer FEATURE_FLAGS.json et implement_all.sql
3. **Priorité Moyenne** : Restaurer 06_AI_MODELS/ pour les modèles IA legacy
4. **Priorité Moyenne** : Extraire le contenu des fichiers .docx et .odt
5. **Priorité Basse** : Restaurer les CSV runtime et Supabase
6. **Priorité Basse** : Compléter la traçabilité des connaissances non tracées dans TRACEABILITY_MATRIX.md
