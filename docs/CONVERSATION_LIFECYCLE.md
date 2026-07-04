# Conversation Lifecycle

The AAC-C lifecycle engine keeps conversations in a lightweight mock-safe state machine:

- active
- archived

Archived conversations can be restored through the restore engine without materializing any real secrets or external credentials.
