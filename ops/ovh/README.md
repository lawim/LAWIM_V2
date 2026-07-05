# OVH Operations Workspace

This directory is local-only. It is the operator workspace for the OVH VPS and is never copied into the production payload.

Purpose:

- keep the server inventory in one place;
- document the deployment plan for `/opt/lawim`;
- keep environment templates and secret handling notes out of the runtime bundle;
- track DNS, TLS, healthchecks and incident steps during Gate 2B.

Target server:

- host: `vps-6da158cc.vps.ovh.net`
- IPv4: `164.132.44.192`
- IPv6: `2001:41d0:305:2100::1:2af1`
- OS: Ubuntu 26.04
- initial user: `ubuntu`
- application user: `lawim`
- production root: `/opt/lawim`

Runtime architecture:

- application in Docker
- PostgreSQL in Docker
- Redis in Docker
- Nginx installed natively on Ubuntu
- default language: `fr`
- AAD disabled by default
- Cameroon geolocation enabled at runtime

This folder must remain local to the master repository.
