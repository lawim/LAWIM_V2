# AAD Architecture

This document describes the optional Microsoft Entra ID scaffold in LAWIM_V2.

## Principles
- The integration is optional and disabled by default.
- Local authentication remains the default path.
- No Microsoft dependency or network call is introduced.
- Future providers can be plugged in through the identity provider abstraction.
