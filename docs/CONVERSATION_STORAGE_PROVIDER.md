# Conversation Storage Provider

Conversation archives are routed through the storage orchestrator using Drive 8 for conversation archives and archive index material.

- ConversationID -> registry -> provider -> access token
- Media attachments remain resolved through MediaID
- No direct Google Drive URLs are exposed in the mock access layer
