# DNS and TLS Plan

## Temporary stage

- use the IPv4 address `164.132.44.192` for first validation;
- keep HTTP access only until the production domain is confirmed;
- do not claim HTTPS readiness until a real certificate is issued.

## Final stage

When the domain becomes available:

1. add the A and AAAA records;
2. configure Nginx `server_name` for the chosen hostnames;
3. issue certificates with Certbot;
4. redirect HTTP to HTTPS;
5. verify `/healthz`, `/readyz` and `/api/health` over HTTPS;
6. record the certificate renewal command and timer.

