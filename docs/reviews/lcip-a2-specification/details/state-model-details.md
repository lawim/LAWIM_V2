# State Model Details — LCIP A.2

## Fichier créé

`tests/gold_corpus/specification/schema/canonical_state.schema.json`

## Contenu

Modèle officiel décrivant l'état canonique d'une conversation LAWIM à tout
moment. 12 propriétés racines :

| Propriété | Type | Description |
|-----------|------|-------------|
| conversation_id | string | Identifiant persistant |
| phase | enum | initial, in_progress, qualified, unqualified, completed, handover, error |
| intent | string | Intention courante |
| qualification | object | Status, level, criteria_collected, criteria_missing |
| memory | object | Active, expired, retention_count |
| business | object | object_type, object_id, decision, action |
| turn_count | integer | Nombre de tours |
| language | enum | fr, en, pcm |
| channel | enum | web, telegram, whatsapp, api |

## Validation

```bash
python -c "import json; json.load(open('tests/gold_corpus/specification/schema/canonical_state.schema.json'))"
```

## Contrôle

STATE-0001 : PASS
