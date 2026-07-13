# Feature Management Operations

Operational guide for activating and controlling LAWIM capabilities.

## Standard flow

- Inspect current module and feature state.
- Verify dependencies and permissions.
- Review scope and rollout target.
- Apply the change with an audit reason.
- Re-check health and visibility in the cockpit.

## Safe operations

- Activate or deactivate a feature.
- Schedule a future activation.
- Restrict a feature to a role, environment, or organization.
- Roll back a feature to the previous configuration.
- Use a kill switch without deleting data.

## Validation

- Confirm the backend manifest reflects the update.
- Confirm the frontend does not expose blocked actions.
- Confirm logs record the change with correlation metadata.

