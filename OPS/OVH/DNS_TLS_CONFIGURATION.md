# DNS and TLS Configuration

## Current state

- validation can be performed on the temporary IPv4 endpoint `164.132.44.192`;
- host Nginx is active;
- a temporary certificate path is available for local validation;
- final DNS records are still a separate operational task if a production domain is later confirmed.

## Final target

1. add the public A and AAAA records;
2. configure `server_name` on Nginx;
3. issue a production certificate with Certbot;
4. redirect HTTP to HTTPS;
5. verify all health endpoints over HTTPS;
6. record the certificate renewal timer and command.
