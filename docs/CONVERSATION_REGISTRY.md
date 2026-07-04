# Conversation Registry

This document captures the additive AAC-C conversation registry layer.

- Conversations are stored once per ConversationID.
- Participants are linked to the conversation rather than duplicating the conversation record.
- Messages and events are attached to the conversation record.
- Media attachments are referenced through MediaID.
- No Google Drive URLs are stored in conversation payloads.
