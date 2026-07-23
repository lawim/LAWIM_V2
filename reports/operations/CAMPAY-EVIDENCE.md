# Campay Sandbox Validation Report

**Programme:** G.6
**Service:** Campay Sandbox
**Status:** NOT VALIDATED
**Date:** 2026-07-23

---

## Prérequis non satisfaits

Ce test nécessite :

- `CAMPAY_API_USERNAME` — non configuré
- `CAMPAY_API_PASSWORD` — non configuré
- `CAMPAY_WEBHOOK_SECRET` — non configuré
- URL publique HTTPS pour recevoir les callbacks Campay
- Compte Campay Sandbox actif

## Procédure de validation

Une fois les credentials disponibles, exécuter :

```bash
# 1. Créer une intention de paiement via PaymentRuntime
python3 -c "
from lawim_runtime.domains.base.request import DomainRuntimeRequest
from lawim_runtime.domains.payment.runtime import PaymentRuntime
pay = PaymentRuntime()
req = DomainRuntimeRequest(
    action_code='CREATE_PAYMENT_INTENT',
    parameters={
        'project_id': 'g6-campay-test',
        'transaction_id': 'tx-g6-001',
        'amount': 1000,
        'currency': 'XAF',
        'payment_method': 'mobile_money',
    },
    idempotency_key='g6-campay-idemp-001',
)
result = pay.execute(req)
print(f'Status: {result.status}, IntentID: {result.output}')
"

# 2. Vérifier la réception du callback Campay (webhook)
# 3. Vérifier la confirmation du paiement
# 4. Vérifier la mise à jour du ProjectProfile
# 5. Vérifier la mise à jour CRM
```

## Scénarios à valider

| # | Scénario | Statut | Preuve |
|---|----------|--------|--------|
| 1 | Création d'intention de paiement | NON VALIDÉ | Requiert sandbox |
| 2 | Paiement mobile money | NON VALIDÉ | Requiert sandbox |
| 3 | Callback reçu et traité | NON VALIDÉ | Requiert URL publique |
| 4 | Confirmation persistée | NON VALIDÉ | Requiert sandbox |
| 5 | Journal CRM mis à jour | NON VALIDÉ | Requiert flux E2E |
| 6 | ProjectProfile mis à jour | NON VALIDÉ | Requiert flux E2E |
| 7 | Idempotence (même requête 2x) | NON VALIDÉ | Requiert sandbox |
| 8 | Aucune perte de données | NON VALIDÉ | Requiert sandbox |

## Conclusion

**Campay L6 : NON VALIDÉ.** Le PaymentRuntime est implémenté (L3) mais aucun test sandbox réel n'a été exécuté. La validation nécessite des credentials Campay Sandbox et une URL publique HTTPS.
