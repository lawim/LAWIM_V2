# RELEASE PROGRAM AAE - Storage Routing

## Scope

- Official routing policy for MediaID and ConversationID related storage
- Drive ordering, fallback rules, and blocked resource handling
- Admin dashboard visibility for routing decisions

## Implemented

- Video -> Drive 1 -> Drive 2 -> Drive 8
- Photo -> Drive 3 -> Drive 8
- Audio -> Drive 3 -> Drive 8
- Document -> Drive 4 -> Drive 8
- Conversation archive -> Drive 5 -> Drive 8
- Export / report / statistics -> Drive 6 -> Drive 8
- Application backup -> Drive 7 -> Drive 10
- Critical replication -> Drive 8 -> Drive 10
- Reserve -> Drive 9
- Maintenance / migration -> Drive 10

## Validation

- Routing policy is mock-safe
- The first available candidate is selected
- Blocked resources are surfaced in the registry and dashboard
- No Google Drive URL is stored in business data

## Notes

- The routing policy is aligned with the Storage Resource Registry
- The wizard previews the route map before the secure assistant phase

