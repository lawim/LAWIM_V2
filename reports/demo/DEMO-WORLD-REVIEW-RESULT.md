# LAWIM Demo World V1 — Full Review Result
**Date:** 2026-07-23  **Dataset:** LAWIM_DEMO_WORLD_V1  **Status:** IN_PROGRESS
## 1. Complete Inventory
| users | 22 |
| professional_profiles | 16 |
| organizations | 12 |
| services | 18 |
| properties | 117 |
| property_media | 0 |
| documents | 0 |
| search_profiles | 0 |
| matches | 0 |
| connections | 0 |
| conversations | 0 |
| messages | 0 |
| appointments | 0 |
| visits | 0 |
| quotes | 0 |
| invoices | 0 |
| payments | 0 |
| notifications | 0 |
| consents | 0 |
| reviews | 0 |
| incidents | 0 |
| scenarios | 12 |
| negative_cases | 8 |

## 2. Users
| ID | Name | Role | City | Status | Verification | Consent | Org |
|---|------|------|------|--------|-------------|---------|-----|
| DEMO-USER-CLIENT-001 | Jean Dupont | client | Yaoundé | active | verified | granted | - |
| DEMO-USER-CLIENT-002 | Alice Mbarga | client | Yaoundé | active | verified | granted | - |
| DEMO-USER-CLIENT-003 | Pierre Kamga | client | Yaoundé | active | verified | granted | - |
| DEMO-USER-CLIENT-004 | Marie Ngo Bissa | client | Yaoundé | active | verified | granted | - |
| DEMO-USER-CLIENT-005 | Paul Etoundi | client | Douala | active | verified | granted | - |
| DEMO-USER-CLIENT-006 | Sarah Nkwi | client | Douala | active | unverified | granted | - |
| DEMO-USER-CLIENT-007 | Robert Tchinda | client | Bafoussam | inactive | unverified | pending | - |
| DEMO-USER-CLIENT-008 | Esther Mvogo | client | Bafoussam | inactive | unverified | denied | - |
| DEMO-USER-OWNER-001 | Thomas Mvogo | owner | Yaoundé | active | verified | granted | - |
| DEMO-USER-OWNER-002 | Christine Eyanga | owner | Yaoundé | active | verified | granted | - |
| DEMO-USER-OWNER-003 | Suzanne Mbah | owner | Yaoundé | active | verified | granted | - |
| DEMO-USER-OWNER-004 | Joseph Obama | owner | Douala | active | unverified | pending | - |
| DEMO-USER-OWNER-005 | Beatrice Simo | owner | Bafoussam | inactive | unverified | denied | - |
| DEMO-USER-AGENT-001 | Luc Tchinda | agent | Yaoundé | active | verified |  | DEMO-ORG-AGENCY-001 |
| DEMO-USER-AGENT-002 | Rosalie Nkwi | agent | Yaoundé | active | verified |  | DEMO-ORG-AGENCY-001 |
| DEMO-USER-AGENT-003 | Emmanuel Simo | agent | Douala | suspended | unverified |  | DEMO-ORG-AGENCY-002 |
| DEMO-USER-PRO-001 | Pierre Atangana | service_provider | Yaoundé | active | verified |  | - |
| DEMO-USER-PRO-002 | Marie Ekwé | service_provider | Yaoundé | active | verified |  | - |
| DEMO-USER-PRO-003 | Jean Meka | service_provider | Yaoundé | active | verified |  | - |
| DEMO-USER-PRO-004 | Chantal Ngo | service_provider | Yaoundé | active | verified |  | - |
| DEMO-USER-SUPPORT-001 | Fabrice Noah | commercial | Yaoundé | active | verified |  | - |
| DEMO-USER-ADMIN-001 | Admin LAWIM | admin | Yaoundé | active | verified |  | - |

## 3. Professional Profiles
| ID | Profession | User | Org | Verified | Available |
|---|-----------|------|-----|----------|----------|
| DEMO-PRO-ARCH-001 | architect | DEMO-USER-PRO-001 | DEMO-ORG-ARCHI-001 | True | True |
| DEMO-PRO-ARCH-002 | architect | DEMO-USER-PRO-002 | DEMO-ORG-ARCHI-001 | True | True |
| DEMO-PRO-NOTARY-001 | notary | DEMO-USER-PRO-003 | DEMO-ORG-NOTARY-001 | True | True |
| DEMO-PRO-SURVEYOR-001 | surveyor | DEMO-USER-PRO-004 | DEMO-ORG-SURVEY-001 | True | True |
| DEMO-PRO-LAWYER-001 | lawyer | None | DEMO-ORG-LEGAL-001 | True | True |
| DEMO-PRO-BUILDER-001 | builder | None | DEMO-ORG-CONSTRUCT-001 | True | True |
| DEMO-PRO-ELECTRICIAN-001 | electrician | None | DEMO-ORG-CONSTRUCT-001 | True | True |
| DEMO-PRO-PLUMBER-001 | plumber | None | DEMO-ORG-MAINT-001 | True | True |
| DEMO-PRO-AGENT-001 | real_estate_agent | DEMO-USER-AGENT-001 | DEMO-ORG-AGENCY-001 | True | True |
| DEMO-PRO-AGENT-002 | real_estate_agent | DEMO-USER-AGENT-002 | DEMO-ORG-AGENCY-001 | True | True |
| DEMO-PRO-MOVER-001 | mover | None | DEMO-ORG-MOVER-001 | True | True |
| DEMO-PRO-FINANCE-001 | financial_advisor | None | DEMO-ORG-FINANCE-001 | True | True |
| DEMO-PRO-INSURANCE-001 | insurance_agent | None | DEMO-ORG-FINANCE-001 | True | True |
| DEMO-PRO-MAINT-001 | maintenance_tech | None | DEMO-ORG-MAINT-001 | True | True |
| DEMO-PRO-CLEANER-001 | cleaner | None | DEMO-ORG-MAINT-001 | True | False |
| DEMO-PRO-PHOTO-001 | photographer | None | DEMO-ORG-AGENCY-001 | True | True |

## 4. Organizations
| ID | Name | Category | City | Status |
|---|------|----------|------|--------|
| DEMO-ORG-AGENCY-001 | DEMO Agence Centrale | real_estate_agency | Yaoundé |  |
| DEMO-ORG-AGENCY-002 | DEMO Immo Services | real_estate_agency | Douala |  |
| DEMO-ORG-NOTARY-001 | DEMO Étude Notariale | notary | Yaoundé |  |
| DEMO-ORG-ARCHI-001 | DEMO Architecture Studio | architecture | Yaoundé |  |
| DEMO-ORG-LEGAL-001 | DEMO Cabinet Juridique | legal | Yaoundé |  |
| DEMO-ORG-CONSTRUCT-001 | DEMO Bâtir Plus | construction | Yaoundé |  |
| DEMO-ORG-SURVEY-001 | DEMO Géomètre Expert | surveying | Yaoundé |  |
| DEMO-ORG-MAINT-001 | DEMO Maintenance Pro | maintenance | Yaoundé |  |
| DEMO-ORG-MOVER-001 | DEMO Déménagement Express | moving | Yaoundé |  |
| DEMO-ORG-FINANCE-001 | DEMO Conseil Finance | financial | Yaoundé |  |
| DEMO-ORG-PROPERTYMGMT-001 | DEMO Gestion Immobilière | property_management | Yaoundé |  |
| DEMO-ORG-ASSURANCE-001 | DEMO Assurances | insurance | Douala |  |

## 5. Services
| ID | Name | Provider | Price |
|---|------|----------|-------|
| DEMO-SERVICE-001 | Consultation architecturale initiale | DEMO-PRO-ARCH-001 | 150000 |
| DEMO-SERVICE-002 | Plan de construction | DEMO-PRO-ARCH-001 | 500000 |
| DEMO-SERVICE-003 | Suivi de chantier | DEMO-PRO-ARCH-001 | 800000 |
| DEMO-SERVICE-004 | Vérification de titre foncier | DEMO-PRO-NOTARY-001 | 200000 |
| DEMO-SERVICE-005 | Acte de vente | DEMO-PRO-NOTARY-001 | 350000 |
| DEMO-SERVICE-006 | Bornage de terrain | DEMO-PRO-SURVEYOR-001 | 250000 |
| DEMO-SERVICE-007 | Levé topographique | DEMO-PRO-SURVEYOR-001 | 400000 |
| DEMO-SERVICE-008 | Conseil juridique immobilier | DEMO-PRO-LAWYER-001 | 100000 |
| DEMO-SERVICE-009 | Gros œuvre construction | DEMO-PRO-BUILDER-001 | 2500000 |
| DEMO-SERVICE-010 | Installation électrique complète | DEMO-PRO-ELECTRICIAN-001 | 150000 |
| DEMO-SERVICE-011 | Plomberie complète | DEMO-PRO-PLUMBER-001 | 100000 |
| DEMO-SERVICE-012 | Déménagement local | DEMO-PRO-MOVER-001 | 200000 |
| DEMO-SERVICE-013 | Consultation crédit immobilier | DEMO-PRO-FINANCE-001 | 50000 |
| DEMO-SERVICE-014 | Assurance habitation | DEMO-PRO-INSURANCE-001 | 75000 |
| DEMO-SERVICE-015 | Maintenance urgente | DEMO-PRO-MAINT-001 | 50000 |
| DEMO-SERVICE-016 | Nettoyage professionnel | DEMO-PRO-CLEANER-001 | 35000 |
| DEMO-SERVICE-017 | Photographie immobilière | DEMO-PRO-PHOTO-001 | 80000 |
| DEMO-SERVICE-018 | Recherche et mise en relation | DEMO-USER-AGENT-001 | 0 |

## 6. Scenarios
| ID | Title | Category | Status | Personas | Properties | Services |
|---|-------|----------|--------|----------|------------|---------|
| SCENARIO-0001 | Location appartement 2 chambres à Mvan | property_rental | READY | 3 | 3 | 1 |
| SCENARIO-0002 | Location studio à Mvan | property_rental | READY | 2 | 1 | 0 |
| SCENARIO-0003 | Achat maison à Bastos | property_purchase | READY | 3 | 1 | 2 |
| SCENARIO-0004 | Achat terrain Nkoabang avec géomètre | land_purchase | READY | 3 | 2 | 3 |
| SCENARIO-0005 | Recherche architecte pour construction | professional_search | READY | 2 | 0 | 3 |
| SCENARIO-0006 | Consultation notariale | professional_search | READY | 2 | 0 | 2 |
| SCENARIO-0007 | Travaux rénovation maison | renovation | READY | 3 | 1 | 2 |
| SCENARIO-0008 | Maintenance urgence plomberie | maintenance | READY | 2 | 0 | 2 |
| SCENARIO-0009 | Recherche géomètre bornage terrain | professional_search | READY | 2 | 0 | 1 |
| SCENARIO-0010 | Déménagement vers nouveau logement | moving | READY | 2 | 0 | 1 |
| SCENARIO-0011 | Financement acquisition immobilière | financial | READY | 2 | 0 | 1 |
| SCENARIO-0012 | Location gestion locative | property_management | READY | 2 | 1 | 1 |

## 7. Negative Cases
- NEG-NO-MATCH-001: Aucun bien ne correspond aux critères (budget trop bas)
- NEG-NO-CONSENT-001: Propriétaire sans consentement pour mise en relation
- NEG-SUSPENDED-001: Bien suspendu sélectionné
- NEG-DUPLICATE-CONNECTION-001: Double tentative de connexion sur le même match
- NEG-BLOCKED-USER-001: Utilisateur suspendu tente une recherche
- NEG-UNAVAILABLE-PRO-001: Professionnel indisponible pour une mission
- NEG-NO-DOCUMENT-001: Document manquant pour finaliser une transaction
- NEG-EXPIRED-PROPERTY-001: Bien expiré ou retiré pendant la conversation

## 8. Properties by City
- Bafoussam: 9
- Douala: 26
- Kribi: 7
- Limbé: 8
- Yaoundé: 67

## 9. Properties by Type
- APARTMENT: 51
- HOUSE: 39
- LAND: 7
- STUDIO: 20

## 10. Coverage Gaps
- MISSING role: locataire
- MISSING role: acheteur
- MISSING role: vendeur
- MISSING role: propriétaire
- MISSING role: bailleur
- MISSING role: investisseur
- MISSING role: promoteur
- MISSING role: agent immobilier
- MISSING role: commercial LAWIM
- MISSING role: gestionnaire
- MISSING role: support
- MISSING role: administrateur
- MISSING profession: agent immobilier
- MISSING profession: gestionnaire locatif
- MISSING profession: architecte
- MISSING profession: notaire
- MISSING profession: avocat
- MISSING profession: géomètre
- MISSING profession: ingénieur
- MISSING profession: entrepreneur
- MISSING profession: plombier
- MISSING profession: électricien
- MISSING profession: maintenance
- MISSING profession: déménageur
- MISSING profession: assureur
- MISSING profession: conseiller crédit
- MISSING profession: photographe
- MISSING profession: sécurité
- MISSING profession: nettoyage

