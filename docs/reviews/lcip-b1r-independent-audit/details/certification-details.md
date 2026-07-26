# Certification Details — Audit B.1R

## Problème principal : Tautologie

Le moteur de certification compare les fichiers `expected_*` avec
eux-mêmes. Il n'y a pas de source de données "actuelle" indépendante.

## Preuve de tautologie

```python
# batch_certify.py ligne 39 :
result = orchestrator.certify(conv_dir, conv_dir, ...)
#                               ↑↑↑↑↑↑↑    ↑↑↑↑↑↑↑
#                              spec_dir = actual_dir
```

```python
# certification_engine.py, load_actual() :
for fname in ["actual_state.json", "actual_business.json"]:
    path = os.path.join(actual_dir, fname)
    if os.path.isfile(path):  # ← FILES NEVER EXIST
        ...
# Retourne {} (dict vide)
```

```python
# certification_engine.py, _evaluate_single_assertion() :
# actual_value = None (car dict vide)
# expected = None (car chargé depuis expected_state.json sans path)
# result = (None == None) → True (PASS)
```

## Pourquoi les tests négatifs passent

Les 7 tests négatifs ont tous obtenu PASS car :
1. Les fichiers `expected_*` contiennent des valeurs erronées
2. Les fichiers `actual_*` n'existent pas
3. L'assertion compare `None == None` → True
4. **Aucune vérification réelle n'a lieu**

## Contrôle

CERT-0001 : INVALID — Certification tautologique, pas de vérification runtime

TAUT-0001 : FAIL — expected et actual chargés depuis le même dossier
