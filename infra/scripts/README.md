# Scripts

Ce dossier reserve les scripts operationnels.

Familles attendues:
- bootstrap;
- verification;
- sauvegarde;
- restauration;
- controle de sante;
- rotation ou nettoyage.

Les scripts devront etre idempotents, traces et explicites.

Squelettes deja presents:
- `../install.sh` : preparation d'hebergement;
- `../check-env.sh` : verification de prerequis et de variables.

Principes:
- ne jamais exposer de secret dans la sortie;
- documenter les codes de sortie;
- garder des effets de bord previsibles;
- reutiliser les conventions du dossier `ovh/` quand un script cible l'hebergement.
