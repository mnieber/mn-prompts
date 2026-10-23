_build use_dockerfile_local use_no_cache:
    #!/usr/bin/env bash
    set -euox pipefail
    DOCKER_BUILDKIT=1 \
    COMPOSE_BAKE=true \
    COMPOSE_PROJECT_NAME=${COMPOSE_PROJECT_NAME} \
    ROOT_DIR="${ROOT_DIR}" \
    docker compose \
        --file "${COMPOSE_DIR}/docker-compose.yml" \
        {{ if use_dockerfile_local == "true" { "--file " + "${COMPOSE_DIR}/docker-compose.dockerfile-local.yml" } else { "" } }} \
        --progress=plain \
        build {{ if use_no_cache == "true" { "--no-cache" } else { "" } }}
