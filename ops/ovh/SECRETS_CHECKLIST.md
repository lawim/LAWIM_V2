# Secrets Checklist

## Must exist only on the server

- application secret key
- PostgreSQL password
- Redis password
- any mail or WhatsApp credentials
- any future TLS material

## Must not exist in Git

- real passwords
- real tokens
- private keys
- certificates
- API keys
- backup passphrases

## Checks before exposure

1. verify the runtime bundle contains only placeholder example files;
2. verify no secret file was copied from the workstation;
3. create secrets with root or `lawim` ownership on the server;
4. restrict secret directories to `750` or tighter;
5. rotate any provisional password before opening public access.

