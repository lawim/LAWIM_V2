#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
ALIAS_DIR="${ROOT}/docker/compose"

declare -A LINKS=(
  ["docker-compose.base.yml"]="../../compose/docker-compose.base.yml"
  ["docker-compose.development.yml"]="../../compose/docker-compose.dev.yml"
  ["docker-compose.staging.yml"]="../../compose/docker-compose.staging.yml"
  ["docker-compose.production.yml"]="../../compose/docker-compose.prod.yml"
  ["docker-compose.postgres.yml"]="../../compose/docker-compose.postgres.yml"
)

mkdir -p "${ALIAS_DIR}"
for name in "${!LINKS[@]}"; do
  target="${LINKS[$name]}"
  link="${ALIAS_DIR}/${name}"
  ln -sfn "${target}" "${link}"
  echo "linked ${link} -> ${target}"
done

echo "Compose aliases synchronized."
