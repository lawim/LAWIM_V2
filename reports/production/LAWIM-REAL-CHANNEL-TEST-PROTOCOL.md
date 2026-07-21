# LAWIM — Protocole de Test Réel WhatsApp et Telegram

## Prérequis

- 1 téléphone avec WhatsApp contenant le numéro `+237 686 822 667` dans ses contacts
- 1 compte Telegram pouvant envoyer un message à `@lawim_assistant_bot`
- Accès SSH au serveur OVH pour lire les logs pendant le test

---

## Phase 1 — Préparation

### 1.1 Activer les logs détaillés

```bash
ssh ubuntu@164.132.44.192
docker logs lawim-app --tail 0 -f > /tmp/lawim_trace_$(date +%Y%m%d_%H%M%S).log 2>&1 &
```

### 1.2 Vérifier que le serveur est prêt

```bash
curl -sf https://api.lawim.app/healthz && echo " OK"
curl -sf https://api.lawim.app/readyz && echo " OK"
```

---

## Phase 2 — Test WhatsApp

### 2.1 Envoyer depuis le téléphone

| # | Message | Action |
|---|---------|--------|
| 1 | `Bonjour` | Envoyer |
| 2 | `Je cherche un studio à Douala` | Envoyer |
| 3 | `À Makepe, pour 80 000 FCFA maximum` | Envoyer |
| 4 | `Je veux entrer en septembre` | Envoyer |
| 5 | `Je suis disponible samedi pour une visite` | Envoyer |

### 2.2 Critères de succès

Chaque réponse doit :
- Commencer par `🤖 LAWIM AI`
- Être en français
- Contenir au maximum une question
- Ne contenir AUCUN des mots : `jumia`, `seloger`, `facebook`, `lamudi`, `afribaba`, `expat-dakar`
- Ne pas ressembler à un guide généraliste

### 2.3 Vérifier les logs

```bash
grep "TURN correlation=" /tmp/lawim_trace_*.log | head -20
```

Vérifier que `engine_ok=true` et `stage=delivery` pour chaque message.

### 2.4 Vérifier le conversation_id

```bash
grep "TURN correlation=" /tmp/lawim_trace_*.log | grep -oP 'key=\S+' | sort -u
```

Le `conversation_key` doit être le même pour les 5 messages.

---

## Phase 3 — Test Telegram

### 3.1 Envoyer depuis Telegram vers `@lawim_assistant_bot`

| # | Message | Action |
|---|---------|--------|
| 1 | `Bonjour` | Envoyer |
| 2 | `Je cherche un studio à Douala` | Envoyer |
| 3 | `À Makepe, pour 80 000 FCFA maximum` | Envoyer |
| 4 | `Je veux entrer en septembre` | Envoyer |
| 5 | `Je suis disponible samedi pour une visite` | Envoyer |

### 3.2 Mêmes critères que WhatsApp

### 3.3 Vérifier les logs Telegram

```bash
grep "TURN correlation=" /tmp/lawim_trace_*.log | grep telegram
```

---

## Phase 4 — Validation Métier

Après les tests techniques, envoyer depuis un canal quelconque :

| Message | Résultat attendu |
|---------|-----------------|
| `Je cherche un terrain à Douala` | Intention=BUY_LAND, ville=Douala |
| `Je veux vendre ma maison` | Intention=SELL_PROPERTY |
| `Mon budget est finalement de 120 000 FCFA` | Correction du budget |
| `C'est trop cher` | Reformulation ou ajustement |
| `Je veux parler à une personne` | Handover déclenché |
| `Avez-vous des photos ?` | Réponse métier (pas de refus) |

---

## Phase 5 — Après les tests

### Si tous les tests passent

```bash
git tag lawim-v2-conversation-rebuild-production-verified
git push origin lawim-v2-conversation-rebuild-production-verified
```

### Si un test échoue

```bash
# Collecter les logs d'erreur
grep -i "safety\|exception\|error\|fail" /tmp/lawim_trace_*.log > p1_failure_report.txt
# Signaler avec les preuves
```
