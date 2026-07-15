# LANGUAGE SCORE — Heritage Gold Readiness

**Audité par :** Language Expert (H0.3)
**Date :** 2026-07-15

## Score global : 71/100

## Sous-dimensions

| # | Dimension | Score | Justification |
|---|-----------|:-----:|---------------|
| 1 | **Synonyms & aliases** | 50 | search_aliases.json : 17 entrées correctes mais direction mal représentée (FR→[synonymes] et non EN→FR). Entity linking : seulement 9/20 paires annoncées existent. Items 10-20 (parking↔stationnement, piscine↔swimming pool, etc.) sont FABRIQUÉS. Manque : FCFA↔XAF, sdb→sdb, YDE→Yaoundé, DLA→Douala. |
| 2 | **Cameroonian RE expressions** | 85 | Corpus 697 lignes correct. 4 langues (FR/EN/PID/Camfranglais) exactes. Gold liste 6 intents mais le fichier en a 7 (manque : urgent, diaspora). Exemples représentatifs. |
| 3 | **Spelling variations & typos** | 75 | 10 villes correctes. Gold annonce 11 quartiers mais le tableau en montre 6 (source en a 9). Types de bien : liste 9 (incl. duplex, commerce) mais source en a 8 (incl. magasin). Base agrégée : 49 entrées / 346 lignes correct. |
| 4 | **Language detection keywords** | 85 | FR 18 et EN 18 identiques à language_detector_ia.py. PID : en-tête dit "14 mots-clés" mais tableau en montre 13 (manque : now now). La source a bien 14. |
| 5 | **Multilingual response templates** | 60 | Gold annonce 8 templates mais multilingual_responses.py en a 7 (language_changed absent). Texte simplifié : emojis, formatage et formulations naturelles absents. language_changed existe dans language_handler.py seulement. |
| 6 | **Pricing expressions** | 65 | Fourchette milliers correcte. Millions : source va jusqu'à 100M, Gold dit 200M (non vérifié). "Franc CFA" pas dans la source (seulement FCFA/CFA/XAF). 4 termes de négociation absents de la source. |
| 7 | **WhatsApp language patterns** | 75 | Fichiers non fournis pour vérification (diaspora_language.json, investor_language.json, etc.). Contenu de whatsapp_language.json supporte les patterns décrits. |
| 8 | **Language detection pipeline** | 95 | Hiérarchie 3 niveaux (DeepSeek→Gemini→Local) identique à language_detector_ia.py. Persistance utilisateur OK. Commande LANGUE OK. |
| 9 | **Cross-language normalization** | 50 | IDs normalisés (APT, STU, CHB, etc.) sont INVENTÉS — pas dans les sources. La normalisation existe via search_aliases.json + typo databases mais pas de tableau structuré. |
| 10 | **Real estate vocabulary** | 70 | 30 termes plausibles et cohérents. Beaucoup vérifiables via entity_linking, search_aliases, pricing. Fichier real_estate_vocabulary.json non fourni. |

## Forces

- Pipeline de détection de langue : excellent (95/100)
- Corpus WhatsApp : bon (85/100)
- Mots-clés de détection : bon (85/100)
- Variations orthographiques : bon (75/100)

## Faiblesses critiques

- Entity linking : 50% fabriqué (10/20 paires inventées)
- IDs normalisés (APT, STU, etc.) : complètement inventés
- Templates : textes simplifiés, pas de emojis
- Pricing : millions borne supérieure non vérifiée, "Franc CFA" absent de la source

## Conclusion

La langue est correcte sur les aspects fondamentaux (détection, corpus) mais a des erreurs factuelles dans les données d'entity linking et les IDs normalisés qui pourraient induire en erreur la reconstruction. 50% des paires entity_linking sont fabriquées — c'est un problème de qualité qui doit être corrigé avant intégration.
