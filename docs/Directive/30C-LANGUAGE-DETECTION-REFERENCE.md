# LAWIM

# 30C-LANGUAGE-DETECTION-REFERENCE.md

# Référentiel officiel de détection de langue

Version 1.0

---

# CHAPITRE 1 — OBJECTIF

Le présent document définit la détection automatique de langue dans LAWIM.

Il s'applique à :

* la conversation ;
* le matching ;
* les notifications ;
* l'IA ;
* les réponses API ;
* les emails ;
* les SMS ;
* Campay.

---

# CHAPITRE 2 — SIGNALS DE DÉTECTION

La langue peut être déduite à partir de :

* la préférence utilisateur ;
* la session ;
* l'appareil ;
* `Accept-Language` ;
* le texte saisi ;
* l'historique conversationnel ;
* la configuration du canal.

---

# CHAPITRE 3 — RÈGLES

La détection doit :

* produire une langue principale ;
* produire un niveau de confiance ;
* conserver la langue de repli ;
* journaliser la décision ;
* permettre une correction manuelle.

---

# CHAPITRE 4 — REPLI

En cas d'ambiguïté, LAWIM doit :

* rester dans la langue précédente si elle est connue ;
* sinon basculer sur le Français ;
* sinon demander une clarification explicite.

---

# CHAPITRE 5 — QUALITÉ

La détection doit être évaluée sur :

* la précision ;
* le rappel ;
* le taux de correction manuelle ;
* le taux de fallback ;
* la stabilité des réponses.

---

# CHAPITRE 6 — OBJECTIF FINAL

Le moteur de détection de langue doit permettre à LAWIM de répondre dans la langue appropriée sans perturber le modèle métier.

