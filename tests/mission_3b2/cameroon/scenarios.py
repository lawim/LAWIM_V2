#!/usr/bin/env python3
"""LAWIM V2 Mission 3B.2 — Cameroon Realistic User Simulator
Total: 150 scenarios (100 Search/Matching + 50 Consent/Relationship)
Uses real Cameroonian expressions, neighborhoods, and behaviors.
"""

CAMEROON_SCENARIOS = [
    # ===== PART 1: SEARCH / MATCHING (1–100) =====
    ## Greetings & basic intents (1-10)
    {"id":"cm-s-001","cat":"search","msg":["bjr","je cherche une maison à Douala","50 mil","50 millions","Oui"],"facts":{"city":"Douala","property_type":"HOUSE","budget_max":50000000}},
    {"id":"cm-s-002","cat":"search","msg":["slt","stuf","je cherche un appart à Makepe","ya koi comme budget?","100 batons","ouais c'est bon"],"facts":{"city":"Douala","district":"Makepe","property_type":"APARTMENT","budget_max":100000}},
    {"id":"cm-s-003","cat":"search","msg":["terrain odza","acheter","25 mil","25 millions","ok"],"facts":{"city":"Yaoundé","district":"Odza","property_type":"LAND","budget_max":25000000}},
    {"id":"cm-s-004","cat":"search","msg":["villa bastos","acheter 200 millions","oui"],"facts":{"city":"Yaoundé","district":"Bastos","property_type":"VILLA","budget_max":200000000}},
    {"id":"cm-s-005","cat":"search","msg":["studio bonamoussadi","location","50 mille","dac"],"facts":{"city":"Douala","district":"Bonamoussadi","property_type":"STUDIO","budget_max":50000}},
    {"id":"cm-s-006","cat":"search","msg":["appart 3 pièces bonapriso","location 200 mille","vas-y"],"facts":{"city":"Douala","district":"Bonapriso","property_type":"APARTMENT","budget_max":200000}},
    {"id":"cm-s-007","cat":"search","msg":["maison mvog-mbi","acheter 80 millions","oui je valide"],"facts":{"city":"Yaoundé","district":"Mvog-Mbi","property_type":"HOUSE","budget_max":80000000}},
    {"id":"cm-s-008","cat":"search","msg":["terrain kribi","acheter près de la plage","75 millions","ok"],"facts":{"city":"Kribi","property_type":"LAND","budget_max":75000000}},
    {"id":"cm-s-009","cat":"search","msg":["immeuble akwa","investissement 300 millions","oui"],"facts":{"city":"Douala","district":"Akwa","property_type":"BUILDING","budget_max":300000000}},
    {"id":"cm-s-010","cat":"search","msg":["maison bafoussam","acheter 30 millions","oui"],"facts":{"city":"Bafoussam","property_type":"HOUSE","budget_max":30000000}},

    ## More cities (11-20)
    {"id":"cm-s-011","cat":"search","msg":["terrain garoua roumde","acheter","10 millions","ok"],"facts":{"city":"Garoua","district":"Roumde-Adje","property_type":"LAND","budget_max":10000000}},
    {"id":"cm-s-012","cat":"search","msg":["villa limbe","200 millions vue mer","ok"],"facts":{"city":"Limbe","property_type":"VILLA","budget_max":200000000}},
    {"id":"cm-s-013","cat":"search","msg":["appart deido","location 80 mille","oui"],"facts":{"city":"Douala","district":"Deido","property_type":"APARTMENT","budget_max":80000}},
    {"id":"cm-s-014","cat":"search","msg":["studio bassa","location 40 mille","yes"],"facts":{"city":"Douala","district":"Bassa","property_type":"STUDIO","budget_max":40000}},
    {"id":"cm-s-015","cat":"search","msg":["maison ebolowa","acheter","25 millions maximum","oui c'est bon"],"facts":{"city":"Ebolowa","property_type":"HOUSE","budget_max":25000000}},
    {"id":"cm-s-016","cat":"search","msg":["terrain dschang","acheter 10 millions","oui"],"facts":{"city":"Dschang","property_type":"LAND","budget_max":10000000}},
    {"id":"cm-s-017","cat":"search","msg":["maison nkongsamba","acheter 7 millions","ok"],"facts":{"city":"Nkongsamba","property_type":"HOUSE","budget_max":7000000}},
    {"id":"cm-s-018","cat":"search","msg":["terrain bertoua","acheter","1 million 500","ok"],"facts":{"city":"Bertoua","property_type":"LAND","budget_max":1500000}},
    {"id":"cm-s-019","cat":"search","msg":["maison maroua","acheter 8 millions","oui"],"facts":{"city":"Maroua","property_type":"HOUSE","budget_max":8000000}},
    {"id":"cm-s-020","cat":"search","msg":["terrain sangmelima","acheter 2 millions","oui"],"facts":{"city":"Sangmelima","property_type":"LAND","budget_max":2000000}},

    ## Professional searches (21-25)
    {"id":"cm-s-021","cat":"search","msg":["je cherche un notaire à Douala","Bonapriso","Oui"],"facts":{"city":"Douala","district":"Bonapriso","transaction_type":"FIND"}},
    {"id":"cm-s-022","cat":"search","msg":["je veux un architecte à Yaoundé","bastos","oui"],"facts":{"city":"Yaoundé","district":"Bastos","transaction_type":"FIND"}},
    {"id":"cm-s-023","cat":"search","msg":["je cherche un géomètre à Kribi","pour bornage terrain","oui"],"facts":{"city":"Kribi","transaction_type":"FIND"}},
    {"id":"cm-s-024","cat":"search","msg":["je cherche un entrepreneur pour construire","Douala Makepe","15 millions budget","oui"],"facts":{"city":"Douala","district":"Makepe","budget_max":15000000}},
    {"id":"cm-s-025","cat":"search","msg":["je cherche un agent immobilier à Bafoussam","pour vendre ma maison","ok"],"facts":{"city":"Bafoussam","transaction_type":"FIND"}},

    ## Budget ambiguity (26-30)
    {"id":"cm-s-026","cat":"search","msg":["maison douala","acheter","109 mil","109 millions","oui"],"facts":{"city":"Douala","budget_max":109000000}},
    {"id":"cm-s-027","cat":"search","msg":["maison douala 50 mille","50 millions je veux dire","acheter","oui"],"facts":{"city":"Douala","budget_max":50000000}},
    {"id":"cm-s-028","cat":"search","msg":["appart douala","100","100 millions","oui"],"facts":{"city":"Douala","budget_max":100000000}},
    {"id":"cm-s-029","cat":"search","msg":["villa douala","50 000 FCFA","non 50 millions FCFA","oui"],"facts":{"city":"Douala","property_type":"VILLA","budget_max":50000000}},
    {"id":"cm-s-030","cat":"search","msg":["villa limbe","200 mille dollars","200 000 USD","oui"],"facts":{"city":"Limbe","property_type":"VILLA","budget_max":200000}},

    ## Multiple criteria (31-35)
    {"id":"cm-s-031","cat":"search","msg":["maison 4 chambres douala","avec piscine acheter","150 millions","oui"],"facts":{"city":"Douala","property_type":"HOUSE","bedroom_count":4,"budget_max":150000000}},
    {"id":"cm-s-032","cat":"search","msg":["terrain 500 m2 buea","acheter 5 millions","ok"],"facts":{"city":"Buea","property_type":"LAND","surface_sqm":500,"budget_max":5000000}},
    {"id":"cm-s-033","cat":"search","msg":["appart meublé bonamoussadi location","100 mille","d'accord"],"facts":{"city":"Douala","district":"Bonamoussadi","property_type":"APARTMENT","budget_max":100000}},
    {"id":"cm-s-034","cat":"search","msg":["studio meublé yaoundé","location 70 mille","oui"],"facts":{"city":"Yaoundé","property_type":"STUDIO","budget_max":70000}},
    {"id":"cm-s-035","cat":"search","msg":["maison grand terrain douala","acheter 100 millions","oui"],"facts":{"city":"Douala","property_type":"HOUSE","budget_max":100000000}},

    ## Change of mind (36-40)
    {"id":"cm-s-036","cat":"search","msg":["studio location douala","finalement je veux acheter","50 millions","oui"],"facts":{"city":"Douala","transaction_type":"BUY","budget_max":50000000}},
    {"id":"cm-s-037","cat":"search","msg":["terrain acheter douala","en fait je veux construire","terrain à bâtir","25 millions","oui"],"facts":{"city":"Douala","budget_max":25000000}},
    {"id":"cm-s-038","cat":"search","msg":["appart bonapriso","non finalement akwa","location 150 mille","oui"],"facts":{"city":"Douala","district":"Akwa","budget_max":150000}},
    {"id":"cm-s-039","cat":"search","msg":["villa makepe","non une maison simple","80 millions","oui"],"facts":{"city":"Douala","district":"Makepe","property_type":"HOUSE","budget_max":80000000}},
    {"id":"cm-s-040","cat":"search","msg":["maison douala","laisse tomber","non finalement je cherche","appart yaoundé","60 millions","oui"],"facts":{"city":"Yaoundé","property_type":"APARTMENT","budget_max":60000000}},

    ## Cameroonian expressions (41-50)
    {"id":"cm-s-041","cat":"search","msg":["ya koi comme appart à douala?","location","100 batons","ok"],"facts":{"city":"Douala","property_type":"APARTMENT","budget_max":100000}},
    {"id":"cm-s-042","cat":"search","msg":["maison douala","c'est pas mon budget 50 mil","50 millions","oui"],"facts":{"city":"Douala","budget_max":50000000}},
    {"id":"cm-s-043","cat":"search","msg":["maison douala","acheter 80 millions","on peut visiter demain?"],"rules":["visit_request_requires_match_first"]},
    {"id":"cm-s-044","cat":"search","msg":["studio yaoundé","location 50 batons","oui"],"facts":{"city":"Yaoundé","property_type":"STUDIO","budget_max":50000}},
    {"id":"cm-s-045","cat":"search","msg":["maison bonapriso","je veux voir le proprio"],"rules":["consent_required_before_contact"]},
    {"id":"cm-s-046","cat":"search","msg":["mon pote a un terrain à douala","30 millions","oui"],"facts":{"city":"Douala","property_type":"LAND","budget_max":30000000}},
    {"id":"cm-s-047","cat":"search","msg":["j'ai vu une annonce sur la route","maison à vendre douala","45 millions","oui"],"facts":{"city":"Douala","property_type":"HOUSE","budget_max":45000000}},
    {"id":"cm-s-048","cat":"search","msg":["immeuble de rapport douala","investissement","250 millions","vas-y"],"facts":{"city":"Douala","property_type":"BUILDING","budget_max":250000000}},
    {"id":"cm-s-049","cat":"search","msg":["maison avec terrain yaoundé","acheter 60 millions","ok"],"facts":{"city":"Yaoundé","property_type":"HOUSE","budget_max":60000000}},
    {"id":"cm-s-050","cat":"search","msg":["terrain constructible douala","acheter 20 millions","oui"],"facts":{"city":"Douala","property_type":"LAND","budget_max":20000000}},

    ## More locations (51-60)
    {"id":"cm-s-051","cat":"search","msg":["villa kribi pied dans l'eau","acheter 350 millions","oui"],"facts":{"city":"Kribi","property_type":"VILLA","budget_max":350000000}},
    {"id":"cm-s-052","cat":"search","msg":["appart 2 chambres bonamoussadi","location 120 mille","oui"],"facts":{"city":"Douala","district":"Bonamoussadi","bedroom_count":2,"budget_max":120000}},
    {"id":"cm-s-053","cat":"search","msg":["terrain bali","acheter 3 millions","ok"],"facts":{"city":"Bali","property_type":"LAND","budget_max":3000000}},
    {"id":"cm-s-054","cat":"search","msg":["maison mbouda","22 millions","oui"],"facts":{"city":"Mbouda","property_type":"HOUSE","budget_max":22000000}},
    {"id":"cm-s-055","cat":"search","msg":["terrain foumban","1 million","oui"],"facts":{"city":"Foumban","property_type":"LAND","budget_max":1000000}},
    {"id":"cm-s-056","cat":"search","msg":["maison mbandjoun","35 millions","ok"],"facts":{"city":"Mbandjoun","property_type":"HOUSE","budget_max":35000000}},
    {"id":"cm-s-057","cat":"search","msg":["appart new bell","location 60 mille","dac"],"facts":{"city":"Douala","district":"New Bell","property_type":"APARTMENT","budget_max":60000}},
    {"id":"cm-s-058","cat":"search","msg":["terrain muyuka","acheter 4 millions 500","ok"],"facts":{"city":"Muyuka","property_type":"LAND","budget_max":4500000}},
    {"id":"cm-s-059","cat":"search","msg":["maison ngaoundéré","5 millions","oui"],"facts":{"city":"Ngaoundéré","property_type":"HOUSE","budget_max":5000000}},
    {"id":"cm-s-060","cat":"search","msg":["appart meublé akwa","200 mille par mois","c'est bon"],"facts":{"city":"Douala","district":"Akwa","property_type":"APARTMENT","budget_max":200000}},

    ## Various (61-70)
    {"id":"cm-s-061","cat":"search","msg":["bjr je cherche terrain","douala","10 millions","oui"],"facts":{"city":"Douala","property_type":"LAND","budget_max":10000000}},
    {"id":"cm-s-062","cat":"search","msg":["slt ya des studios à douala?","location 50 mille","oui"],"facts":{"city":"Douala","property_type":"STUDIO","budget_max":50000}},
    {"id":"cm-s-063","cat":"search","msg":["je veux un terrain à Buea","2 millions 500","oui"],"facts":{"city":"Buea","property_type":"LAND","budget_max":2500000}},
    {"id":"cm-s-064","cat":"search","msg":["maison kousseri","12 millions","ok"],"facts":{"city":"Kousseri","property_type":"HOUSE","budget_max":12000000}},
    {"id":"cm-s-065","cat":"search","msg":["terrain mbanga","16 millions","oui"],"facts":{"city":"Mbanga","property_type":"LAND","budget_max":16000000}},
    {"id":"cm-s-066","cat":"search","msg":["immeuble bonanjo","200 millions","recherche"],"facts":{"city":"Douala","district":"Bonanjo","property_type":"BUILDING","budget_max":200000000}},
    {"id":"cm-s-067","cat":"search","msg":["appart 3 pièces mfoundi","location 150 mille","oui"],"facts":{"city":"Yaoundé","district":"Mfoundi","property_type":"APARTMENT","budget_max":150000}},
    {"id":"cm-s-068","cat":"search","msg":["je veux construire maison douala","terrain déjà","bonamoussadi","30 millions budget","oui"],"facts":{"city":"Douala","district":"Bonamoussadi","budget_max":30000000}},
    {"id":"cm-s-069","cat":"search","msg":["terrain ekounou yaoundé","15 millions","oui"],"facts":{"city":"Yaoundé","district":"Ekounou","property_type":"LAND","budget_max":15000000}},
    {"id":"cm-s-070","cat":"search","msg":["maison biyem-assi","acheter","70 millions","oui"],"facts":{"city":"Yaoundé","district":"Biyem-Assi","property_type":"HOUSE","budget_max":70000000}},

    ## Diversity (71-80)
    {"id":"cm-s-071","cat":"search","msg":["villa haut standing bonapriso","300 millions","oui"],"facts":{"city":"Douala","district":"Bonapriso","property_type":"VILLA","budget_max":300000000}},
    {"id":"cm-s-072","cat":"search","msg":["terrain constructible odza","20 millions","oui"],"facts":{"city":"Yaoundé","district":"Odza","property_type":"LAND","budget_max":20000000}},
    {"id":"cm-s-073","cat":"search","msg":["appart t3 douala","location 250 mille","oui"],"facts":{"city":"Douala","property_type":"APARTMENT","budget_max":250000}},
    {"id":"cm-s-074","cat":"search","msg":["studio 1 pièce yaoundé","location 40 mille","ok"],"facts":{"city":"Yaoundé","property_type":"STUDIO","budget_max":40000}},
    {"id":"cm-s-075","cat":"search","msg":["maison 5 chambres douala","200 millions","oui"],"facts":{"city":"Douala","property_type":"HOUSE","bedroom_count":5,"budget_max":200000000}},
    {"id":"cm-s-076","cat":"search","msg":["terrain agricole muyuka","8 millions","oui"],"facts":{"city":"Muyuka","property_type":"LAND","budget_max":8000000}},
    {"id":"cm-s-077","cat":"search","msg":["investissement locatif douala","studios meublés","100 millions","oui"],"facts":{"city":"Douala","budget_max":100000000}},
    {"id":"cm-s-078","cat":"search","msg":["maison plain-pied yaoundé","acheter","85 millions","oui"],"facts":{"city":"Yaoundé","property_type":"HOUSE","budget_max":85000000}},
    {"id":"cm-s-079","cat":"search","msg":["duplex bonamoussadi","location 350 mille","oui"],"facts":{"city":"Douala","district":"Bonamoussadi","property_type":"DUPLEX","budget_max":350000}},
    {"id":"cm-s-080","cat":"search","msg":["terrain 1000 m2 douala","50 millions","oui"],"facts":{"city":"Douala","property_type":"LAND","surface_sqm":1000,"budget_max":50000000}},

    ## Final 20 search (81-100)
    {"id":"cm-s-081","cat":"search","msg":["studio nlongkak yaoundé","60 mille","ok"],"facts":{"city":"Yaoundé","district":"Nlongkak","property_type":"STUDIO","budget_max":60000}},
    {"id":"cm-s-082","cat":"search","msg":["appart 2 chambres mvog-mbi","location 100 mille","oui"],"facts":{"city":"Yaoundé","district":"Mvog-Mbi","property_type":"APARTMENT","bedroom_count":2,"budget_max":100000}},
    {"id":"cm-s-083","cat":"search","msg":["maison avec piscine bastos","250 millions","oui"],"facts":{"city":"Yaoundé","district":"Bastos","property_type":"HOUSE","budget_max":250000000}},
    {"id":"cm-s-084","cat":"search","msg":["terrain bali","6 millions","oui"],"facts":{"city":"Bali","property_type":"LAND","budget_max":6000000}},
    {"id":"cm-s-085","cat":"search","msg":["investir à kribi","terrain plage","100 millions","oui"],"facts":{"city":"Kribi","property_type":"LAND","budget_max":100000000}},
    {"id":"cm-s-086","cat":"search","msg":["maison dschang vue montagne","20 millions","ok"],"facts":{"city":"Dschang","property_type":"HOUSE","budget_max":20000000}},
    {"id":"cm-s-087","cat":"search","msg":["villa limbe plage","300 millions","oui"],"facts":{"city":"Limbe","property_type":"VILLA","budget_max":300000000}},
    {"id":"cm-s-088","cat":"search","msg":["je cherche un architecte douala","construction villa","oui"],"facts":{"city":"Douala","transaction_type":"FIND"}},
    {"id":"cm-s-089","cat":"search","msg":["agent immobilier yaoundé","pour vendre terrain","ok"],"facts":{"city":"Yaoundé","transaction_type":"FIND"}},
    {"id":"cm-s-090","cat":"search","msg":["notaire bafoussam","pour achat terrain","oui"],"facts":{"city":"Bafoussam","transaction_type":"FIND"}},
    {"id":"cm-s-091","cat":"search","msg":["c'est combien les loyers à makepe?","appart 2 chambres","je peux mettre 150 mille","oui"],"facts":{"city":"Douala","district":"Makepe","budget_max":150000}},
    {"id":"cm-s-092","cat":"search","msg":["j'ai 30 millions","je cherche une maison à douala","oui"],"facts":{"city":"Douala","property_type":"HOUSE","budget_max":30000000}},
    {"id":"cm-s-093","cat":"search","msg":["je veux acheter un terrain à limbe","pas plus de 15 millions","ok"],"facts":{"city":"Limbe","property_type":"LAND","budget_max":15000000}},
    {"id":"cm-s-094","cat":"search","msg":["location maison 3 chambres douala","bonapriso","300 mille","d'accord"],"facts":{"city":"Douala","district":"Bonapriso","property_type":"HOUSE","bedroom_count":3,"budget_max":300000}},
    {"id":"cm-s-095","cat":"search","msg":["où trouver un géomètre à douala?","pour morcellement terrain","ok"],"facts":{"city":"Douala","transaction_type":"FIND"}},
    {"id":"cm-s-096","cat":"search","msg":["terrain 200m2 yaoundé","acheter","8 millions","oui"],"facts":{"city":"Yaoundé","property_type":"LAND","surface_sqm":200,"budget_max":8000000}},
    {"id":"cm-s-097","cat":"search","msg":["je veux un terrain à kribi","résidence secondaire","25 millions","oui"],"facts":{"city":"Kribi","property_type":"LAND","budget_max":25000000}},
    {"id":"cm-s-098","cat":"search","msg":["maison avec garage douala","acheter","80 millions","vas-y"],"facts":{"city":"Douala","property_type":"HOUSE","budget_max":80000000}},
    {"id":"cm-s-099","cat":"search","msg":["villa moderne bastos","150 millions","oui"],"facts":{"city":"Yaoundé","district":"Bastos","property_type":"VILLA","budget_max":150000000}},
    {"id":"cm-s-100","cat":"search","msg":["terrain garoua","7 millions","acheter","oui c'est bon"],"facts":{"city":"Garoua","property_type":"LAND","budget_max":7000000}},

    # ===== PART 2: CONSENT / RELATIONSHIP (101–150) =====
    {"id":"cm-c-001","cat":"consent","msg":["maison douala","60 millions","oui","je veux le contacter","oui j'accepte"],"rules":["consent_granted","relationship_proposed"]},
    {"id":"cm-c-002","cat":"consent","msg":["appart douala","100 mille","oui","je veux le contact","non finalement"],"rules":["consent_denied","back_to_qualifying"]},
    {"id":"cm-c-003","cat":"consent","msg":["terrain odza","20 millions","oui","pas encore je réfléchis"],"rules":["consent_deferred"]},
    {"id":"cm-c-004","cat":"consent","msg":["maison douala","80 millions","oui","le contact stp","oui je veux le contact pour mon autre projet"],"rules":["project_switch_for_consent"]},
    {"id":"cm-c-005","cat":"consent","msg":["maison yaoundé","50 millions","oui","je veux","oui","finalement je retire mon consentement"],"rules":["consent_revoked","relationship_cancelled"]},
    {"id":"cm-c-006","cat":"consent","msg":["maison douala","donne directement son numéro"],"rules":["consent_required","no_direct_contact"]},
    {"id":"cm-c-007","cat":"consent","msg":["maison bonapriso","je peux le voir maintenant?"],"rules":["match_required_first","consent_required"]},
    {"id":"cm-c-008","cat":"consent","msg":["villa makepe","200 millions","oui","visite","oui pour visiter mais pas pour autre chose"],"rules":["limited_consent_respected"]},
    {"id":"cm-c-009","cat":"consent","msg":["appart akwa","150 mille","oui","non pas intéressé","finalement oui je veux","oui"],"rules":["consent_state_reachable_after_revisit"]},
    {"id":"cm-c-010","cat":"consent","msg":["maison douala","c'est pour mon frère et moi","100 millions","oui","je veux le contact","oui pour moi et mon frère"],"rules":["multi_party_consent_handled"]},
    {"id":"cm-c-011","cat":"consent","msg":["maison douala","je ne veux pas partager mes infos"],"rules":["privacy_preference_honored"]},
    {"id":"cm-c-012","cat":"consent","msg":["je connais déjà le propriétaire"],"rules":["existing_relationship_check"]},
    {"id":"cm-c-013","cat":"consent","msg":["maison douala","80 millions","oui","contact stp","oui","accepté","je ne veux plus"],"rules":["relationship_terminated","consent_revocation_respected"]},
    {"id":"cm-c-014","cat":"consent","msg":["mets-moi en relation avec un propriétaire"],"rules":["qualification_required_first"]},
    {"id":"cm-c-015","cat":"consent","msg":["maison yaoundé","oui","contact","oui","stop"],"rules":["consent_always_revocable"]},
    {"id":"cm-c-016","cat":"consent","msg":["maison douala","oui","contact","le proprio ne veut pas"],"rules":["bilateral_consent_required"]},
    {"id":"cm-c-017","cat":"consent","msg":["maison douala","oui","juste une question au proprio","oui mais juste une question"],"rules":["consent_purpose_limited"]},
    {"id":"cm-c-018","cat":"consent","msg":["nous sommes 3 acheteurs","maison douala","100 millions","oui","contact pour nous 3"],"rules":["multi_consent_handled"]},
    {"id":"cm-c-019","cat":"consent","msg":["maison douala","80 millions","oui","visite","non"],"rules":["no_visit_without_relationship"]},
    {"id":"cm-c-020","cat":"consent","msg":["on m'a déjà mis en relation avec le vendeur"],"rules":["existing_relationship_detected"]},
    {"id":"cm-c-021","cat":"consent","msg":["maison douala","oui","contact","oui mais seulement par email"],"rules":["consent_channel_preference"]},
    {"id":"cm-c-022","cat":"consent","msg":["je suis propriétaire à Douala","un acheteur est intéressé","je veux son contact"],"rules":["bilateral_consent_required","asymmetric_flow"]},
    {"id":"cm-c-023","cat":"consent","msg":["j'ai déjà visité la maison","je veux le contact du propriétaire"],"rules":["consent_still_required_for_digital_contact"]},
    {"id":"cm-c-024","cat":"consent","msg":["je veux juste voir la photo du bien","pas besoin de consentement pour ça"],"rules":["property_photos_public","no_personal_data_shared"]},
    {"id":"cm-c-025","cat":"consent","msg":["maison douala","oui","contact","oui pour le suivi commercial"],"rules":["consent_purpose_documented"]},
    {"id":"cm-c-026","cat":"consent","msg":["maison douala","oui","contact","oui","accepté","j'ai visité, plus besoin"],"rules":["relationship_closed_after_visit"]},
    {"id":"cm-c-027","cat":"consent","msg":["maison douala","oui","contact","oui","je retire","finalement je veux re-contacter","oui"],"rules":["reconsent_possible"]},
    {"id":"cm-c-028","cat":"consent","msg":["appart douala","je ne veux pas laisser mes données","c'est personnel"],"rules":["data_minimization_respected"]},
    {"id":"cm-c-029","cat":"consent","msg":["terrain yaoundé","je veux le contacter maintenant","oui","oui je suis sûr"],"rules":["consent_granted_immediate"]},
    {"id":"cm-c-030","cat":"consent","msg":["maison douala","je ne veux pas de mise en relation","je cherche juste"],"rules":["consent_bypass_honored"]},
    {"id":"cm-c-031","cat":"consent","msg":["maison douala","100 millions","oui","je veux le contact du vendeur","oui je confirme","ok contactez-le"],"rules":["consent_flow_completed"]},
    {"id":"cm-c-032","cat":"consent","msg":["je vends ma maison douala","je ne veux pas qu'on donne mon numéro à tout le monde"],"rules":["owner_privacy_respected"]},
    {"id":"cm-c-033","cat":"consent","msg":["maison douala","je suis intéressé","c'est pour un ami","oui pour lui aussi"],"rules":["third_party_consent_handled"]},
    {"id":"cm-c-034","cat":"consent","msg":["je suis propriétaire","je retire mon offre de vente"],"rules":["listing_withdrawn","consent_revoked_for_listing"]},
    {"id":"cm-c-035","cat":"consent","msg":["maison douala","oui","contact","oui","je ne veux pas que vous gardiez mes données"],"rules":["erasure_request_accepted"]},
    {"id":"cm-c-036","cat":"consent","msg":["maison yaoundé","je change d'avis","je ne veux plus être contacté par personne"],"rules":["communication_opt_out"]},
    {"id":"cm-c-037","cat":"consent","msg":["je suis acheteur","je ne veux pas donner mon email","donne par WhatsApp"],"rules":["contact_channel_preference"]},
    {"id":"cm-c-038","cat":"consent","msg":["j'ai trouvé la maison sur votre app","le vendeur m'a contacté direct","pas besoin de consentement"],"rules":["off_platform_contact_noted"]},
    {"id":"cm-c-039","cat":"consent","msg":["je veux le contact maintenant","oui","oui et je veux visiter samedi"],"rules":["consent_and_visit_requested"]},
    {"id":"cm-c-040","cat":"consent","msg":["je cherche un terrain","je ne veux pas qu'on sache mon budget"],"rules":["budget_privacy_respected"]},
    {"id":"cm-c-041","cat":"consent","msg":["maison douala","on est plusieurs dans la famille","ma mère veut aussi parler au vendeur"],"rules":["family_consent_handled"]},
    {"id":"cm-c-042","cat":"consent","msg":["villa kribi","je veux voir","non finalement je ne veux pas partager mes infos","ok laisse"],"rules":["consent_withdrawn_before_proposal"]},
    {"id":"cm-c-043","cat":"consent","msg":["appart akwa","c'est mon agent qui gère","il a mon accord"],"rules":["agent_authorization_verified"]},
    {"id":"cm-c-044","cat":"consent","msg":["maison douala","je cherche pour ma mère","elle est âgée","je gère tout"],"rules":["proxy_consent_boundary"]},
    {"id":"cm-c-045","cat":"consent","msg":["je veux visiter","c'est pour décider","je ne veux pas m'engager"],"rules":["visit_only_requires_limited_consent"]},
    {"id":"cm-c-046","cat":"consent","msg":["vous avez partagé mes données sans mon accord"],"rules":["compliance_check_complaint_handled"]},
    {"id":"cm-c-047","cat":"consent","msg":["maison douala","je veux le contact pour aujourd'hui","c'est urgent"],"rules":["urgency_does_not_bypass_consent"]},
    {"id":"cm-c-048","cat":"consent","msg":["je ne veux pas qu'on garde mon historique"],"rules":["data_retention_opt_out"]},
    {"id":"cm-c-049","cat":"consent","msg":["maison douala","j'ai trouvé par moi-même","vous avez donné mon contact sans mon accord"],"rules":["unauthorized_sharing_complaint"]},
    {"id":"cm-c-050","cat":"consent","msg":["je suis le propriétaire","j'accepte la mise en relation avec l'acheteur sérieux"],"rules":["owner_consent_granted"]},
]

def get_scenarios(category=None):
    if category is None:
        return CAMEROON_SCENARIOS
    return [s for s in CAMEROON_SCENARIOS if s["cat"] == category]

def get_scenario_ids():
    return [s["id"] for s in CAMEROON_SCENARIOS]
