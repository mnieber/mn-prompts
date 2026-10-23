_pip_compile:
    #!/usr/bin/env bash
    set -euo pipefail
    for service_dir in "${ROOT_DIR}/src/services"/*/; do
        if just --justfile "${service_dir}justfile.host" --working-directory "${service_dir}" --list 2>/dev/null | grep -qE '^\s+pip-compile(\s|$)'; then
            echo "Running pip-compile in ${service_dir}"
            BLOGS_LIBS_DIR="${ROOT_DIR}/src/libs" just --justfile "${service_dir}justfile.host" --working-directory "${service_dir}" pip-compile
        fi
    done
