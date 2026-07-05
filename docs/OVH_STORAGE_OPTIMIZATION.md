# OVH Storage Optimization

The LAWIM_V2 storage layer is prepared for OVH production with mock-safe optimization policies.

## Optimization rules

- Thumbnails stay on OVH
- Cold originals move to the Google Drive layer
- Conversation archives route to Drive 5 first and Drive 8 as overflow
- Application backups route to Drive 7 and Drive 10
- Overflow routes use Drive 8
- Strategic reserve stays on Drive 9
- Maintenance and migration stay on Drive 10

## Safety notes

- No real Google Drive URL is stored in business data
- No real token, client secret, or refresh token is stored in the repository
- Duplicate storage is controlled through the registry and the routing policy
