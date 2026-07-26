# Deployment Details

Git repo aligned to main at dc9caee6.
Build failed: V3 Dockerfile (deployment/compose/docker-compose.prod.yml) references files not present in V2 main branch.
Old container remains healthy and running.
Health endpoint: 200.

## Status
OVH Access: PASS
Git Sync: PASS (OVH_GIT_HEAD=dc9caee6=TARGET_SHA)
Container Build: FAILED (V3 Dockerfile incompatible with V2 code)
Service: RUNNING (old container healthy)
