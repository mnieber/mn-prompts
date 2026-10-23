_down use_override_file use_src_overlays:
    #!/usr/bin/env bash
    set -euox pipefail
    DOCKER_BUILDKIT=1 \
    COMPOSE_PROJECT_NAME=${COMPOSE_PROJECT_NAME} \
    ROOT_DIR="${ROOT_DIR}" \
    docker compose \
        --file "${COMPOSE_DIR}/docker-compose.yml" \
        {{ if use_src_overlays == "true" { "--file " + "${COMPOSE_DIR}/docker-compose.src-overlays.yml" } else { "" } }} \
        {{ if use_override_file == "true" { "--file " + "${COMPOSE_DIR}/docker-compose.override.yml" } else { "" } }} \
        down --remove-orphans
