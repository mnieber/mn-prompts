_run_image service_name use_dockerfile_local use_override_file use_src_overlays cmd="":
    #!/usr/bin/env bash
    set -euox pipefail

    # Build base images
    DOCKER_BUILDKIT=1 \
    COMPOSE_PROJECT_NAME=${COMPOSE_PROJECT_NAME} \
    ROOT_DIR="${ROOT_DIR}" \
    docker compose \
        --file "${COMPOSE_DIR}/docker-compose.yml" \
        {{ if use_src_overlays == "true" { "--file " + "${COMPOSE_DIR}/docker-compose.src-overlays.yml" } else { "" } }} \
        {{ if use_dockerfile_local == "true" { "--file " + "${COMPOSE_DIR}/docker-compose.dockerfile-local.yml" } else { "" } }} \
        {{ if use_override_file == "true" { "--file " + "${COMPOSE_DIR}/docker-compose.override.yml" } else { "" } }} \
        run \
            --rm \
            --remove-orphans \
            --service-ports \
            {{ service_name }} \
            {{ if cmd != "" { "--command " + cmd } else { "" } }}
