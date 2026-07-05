# Users and Access

## System users

- `ubuntu`: initial SSH entry account provided by the VPS host;
- `lawim`: dedicated application system user for `/opt/lawim`.

## Access model

- SSH access should use keys, not passwords;
- secret files are owned by root or `lawim` and kept non-world-readable;
- the application user only needs access to runtime paths, not to the whole repository history.

## Grouping

- `lawim` owns the runtime tree;
- Nginx remains a host-level service;
- database and cache containers isolate their own data volumes.

## Prohibited

- storing passwords in documents;
- copying private keys into the bundle;
- exposing any secret in logs or notes.
