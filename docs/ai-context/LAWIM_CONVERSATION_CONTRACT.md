# LAWIM — Contrat Conversationnel Canonique

## Architecture canonique

```
message entrant
→ normalisation
→ résolution de l'acteur
→ résolution de la conversation
→ chargement de la mémoire
→ détection de la langue
→ détection de l'intention
→ extraction des critères
→ fusion avec l'état existant
→ moteur de qualification
→ choix de la prochaine action
→ agent métier
→ formulation
→ validation
→ rendu du canal
→ persistance
→ livraison
```

## Rôle du LLM

Le LLM peut :

- reformuler
- résumer
- expliquer
- rédiger une réponse
- rendre une question naturelle

Le LLM ne peut pas décider seul :

- de l'intention métier
- de l'état de la conversation
- de la prochaine étape métier
- de la disponibilité d'un bien
- du statut d'une visite
- du statut d'un paiement
- de la création d'un handover

## Mémoire obligatoire

Le système doit conserver les informations déjà fournies.

Exemple canonique :

```
Utilisateur :
Je cherche un appartement de deux chambres à Douala.

Utilisateur :
Mon budget est de 180 000 FCFA par mois.

Utilisateur :
Je préfère Bonamoussadi.
```

État attendu :

```yaml
intent: rental_search
property_type: apartment
bedrooms: 2
city: Douala
budget_xaf: 180000
district: Bonamoussadi
qualification_status: in_progress
```

Le système ne doit plus demander :

- le type de bien
- le nombre de chambres
- la ville
- le budget
- le quartier

une fois qu'ils ont été fournis.

## Prochaine question

Chaque réponse doit poser au maximum une seule prochaine question utile.

## Handover

Un handover humain nécessite obligatoirement :

- `handover_required=true`
- `handover_id`
- raison
- équipe cible
- statut persistant
- audit

Aucune salutation ou demande ordinaire ne doit provoquer automatiquement un handover.

## Footer IA

Le footer français canonique doit comporter au maximum dix mots :

`ℹ️ LAWIM AI peut se tromper. Vérifiez les informations importantes.`

Il doit être :

- discret
- non bloquant
- séparé du contenu
- adapté au canal

## Règles d'identité

- Messages utilisateur : `👤 <nom/identifiant>`
- Messages LAWIM : `🤖 LAWIM AI`
- Jamais de noms de fournisseurs IA visibles
