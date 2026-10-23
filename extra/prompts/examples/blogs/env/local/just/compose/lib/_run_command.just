_run_command service_name cmd="":
    #!/usr/bin/env bash
    set -euox pipefail

    COMPOSE_PROJECT_NAME=${COMPOSE_PROJECT_NAME} \
    ROOT_DIR="${ROOT_DIR}" \
    docker compose \
        --file "${COMPOSE_DIR}/docker-compose.yml" \
        exec \
            {{ service_name }} \
            {{ if cmd != "" { cmd } else { "bash" } }}
