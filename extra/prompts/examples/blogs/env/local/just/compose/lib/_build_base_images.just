_build_base_images use_no_cache:
    #!/usr/bin/env bash
    set -euox pipefail
    DOCKER_BUILDKIT=1 \
    COMPOSE_BAKE=true \
    COMPOSE_PROJECT_NAME=${COMPOSE_PROJECT_NAME} \
    ROOT_DIR="${ROOT_DIR}" \
    docker compose \
        --file "${COMPOSE_DIR}/docker-compose.base-images.yml" \
        --progress=plain \
        build \
            {{ if env_var_or_default("BLOGS_OS_CUSTOM_PACKAGES", "") != "" { "--build-arg OS_CUSTOM_PACKAGES=\"${BLOGS_OS_CUSTOM_PACKAGES}\"" } else { "" } }} \
            {{ if env_var_or_default("BLOGS_PIP_CUSTOM_PACKAGES", "") != "" { "--build-arg PIP_CUSTOM_PACKAGES=\"${BLOGS_PIP_CUSTOM_PACKAGES}\"" } else { "" } }} \
            {{ if use_no_cache == "true" { "--no-cache" } else { "" } }}
