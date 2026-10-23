_touch_secrets_env:
    touch ${ROOT_DIR}/env/local/secrets.env

compile-env-files: (_touch_secrets_env)
    python ${ROOT_DIR}/env/local/scripts/compile_env_files.py \
        --input=${ROOT_DIR}/env/local/secrets.env \
        ${ROOT_DIR}/env/local/docker/env_files
