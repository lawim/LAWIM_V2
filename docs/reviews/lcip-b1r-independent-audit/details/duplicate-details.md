# Duplicate Details — Audit B.1R

## Analyse

Les 990 conversations proviennent de 10 blocs distincts avec des dialogues
différents. Aucun ID dupliqué dans la séquence migrée.

## Par bloc

Chaque bloc couvre une plage de conversations différentes :
- Bloc 01 : 0001-0100
- Bloc 02 : 0101-0200
- Bloc 03 : 0201-0290 (90 conversations)
- ...
- Bloc 10 : 0901-0990

## Conclusion

Aucune conversation dupliquée. Les 10 conversations manquantes viennent du
bloc 03 qui contient 90 conversations au lieu de 100.

## Contrôle

DUP-0001 : PASS
