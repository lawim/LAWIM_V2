# Specification Cible Qualification

Version: 1.0
Date: 2026-07-14
Commit de reference: d30d61e1d89427ece9c180cec4639cce77fdcba3
Statut: CANONICAL

## Statut
Qualification conversationnelle actuelle: REBUILD_FROM_ZERO.

## Role
Transformer les messages et formulaires en faits normalises, criteres executables et maturite de projet. La qualification ne choisit pas arbitrairement et ne cree ni matching ni relation.

## Matrices minimales
| Parcours | Champs requis | Recommandes | Eliminatoires |
| --- | --- | --- | --- |
| location | ville/quartier, budget, type, delai | pieces, garanties, preferences | budget absent apres clarification, localisation inconnue |
| achat | ville/quartier, budget, type, financement, delai | surface, titre, usage | budget ou capacite non clarifiee |
| vente | bien, localisation, droit de proposer, prix attendu | documents, occupation | absence de droit declare |
| mise en location | bien, loyer, disponibilite, droit de proposer | photos, reglement | bien non identifiable |
| investissement | objectif, budget, horizon, rendement vise | risque, zones | objectif incoherent non clarifie |
| construction | terrain ou zone, budget, type projet | plan, prestataires | absence de localisation exploitable |
| recherche de professionnel | metier, lieu, besoin, delai | budget, certification | metier ou lieu inconnu |
| documentation | sujet, contexte, juridiction | document source | demande juridique engageante sans orientation notaire |
| suivi transactionnel | dossier, etape, partie, action attendue | documents, echeance | dossier non choisi |

## Regles
Les faits ont provenance, confiance, auteur, horodatage et statut. Les criteres requis bloquent la recherche si absents. Les criteres recommandes ameliorent le score mais ne bloquent pas. Toute correction supersede l'ancien fait au lieu de l'effacer silencieusement.
