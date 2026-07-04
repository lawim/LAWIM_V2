# AAD Sequence

1. The application resolves the AAD configuration from environment variables.
2. The authentication layer evaluates the local path first.
3. If AAD is enabled, the scaffold provider may produce a mock identity and audit event.
4. Authorization uses role, policy, or claim rules without changing the default local behavior.
