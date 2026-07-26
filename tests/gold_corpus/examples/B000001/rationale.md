# B000001 — Recherche appartement Douala

## Objectif

Tester le parcours de recherche locative de base : l'utilisateur cherche un
appartement deux chambres à Douala, quartier Bonamoussadi, budget 180 000 FCFA.

## Points testés

1. Détection de l'intention `rental_search`
2. Extraction des critères (property_type, bedrooms, city, district, budget)
3. Qualification progressive (une question par tour)
4. Respect du budget en FCFA
5. Mémoire conservée entre les messages

## Résultat attendu

- Intention : `rental_search`
- Qualification : `qualified`
- Budget reconnu : 180000
- Une seule question par réponse
