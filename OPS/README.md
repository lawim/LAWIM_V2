# OPS

This tree is the durable local operations memory for LAWIM_V2.
It stays in the master repository and is never copied into the OVH runtime payload.

Scope:

- server inventory and host architecture;
- deployment history and post-deployment reports;
- environment, secrets, backup and restore references;
- maintenance, monitoring, healthcheck and incident runbooks;
- Git and GitHub integration notes.

Current deployment snapshot:

- target host: `vps-6da158cc.vps.ovh.net`
- IPv4: `164.132.44.192`
- IPv6: `2001:41d0:305:2100::1:2af1`
- production root: `/opt/lawim`
- runtime model: Docker app, Docker PostgreSQL, Docker Redis, native Nginx
- application user: `lawim`
- default language: `fr`
- AAD: disabled by default
- bundle commit: `bc46a686`
- bundle checksum: `7644e58bfa80414309b54c38d724cc75b7ced93d8748b6f5b18e95e45cf8b7f2`

The compact working notes under `ops/ovh/` remain useful during live operations.
The `OPS/` tree exists for the long-lived certified record.
