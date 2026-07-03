# Agent Registry

The registry is the source of truth for agent discovery.

## Agent Fields

Each agent exposes:

- `id`
- `name`
- `description`
- `version`
- `capabilities`
- `permissions`
- `health`
- `availability`
- `supportedIntents`
- `supportedModules`
- `dependencies`

## Main Operations

- `register(agent)`
- `registerMany(agents)`
- `unregister(agentId)`
- `update(agentId, patch)`
- `get(agentId)`
- `list()`
- `available()`
- `healthy()`
- `findByIntent(intent)`
- `findByModule(module)`
- `resolveIntent(intent, module?)`
- `createRoutingPlan(intent, module?)`

## Brain Usage

- The Brain queries the registry before delegating work.
- Routing returns coordination candidates only.
- The registry does not make business decisions.
