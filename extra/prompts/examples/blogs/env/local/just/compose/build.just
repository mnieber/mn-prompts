import './env-files.just'
import './lib/_build.just'
import './lib/_build_base_images.just'

# Local variables
default_use_dockerfile_local := env_var_or_default("BLOGS_USE_DOCKERFILE_LOCAL", "false")

build use_dockerfile_local=default_use_dockerfile_local use_no_cache="false": \
    (compile-env-files) \
    (_build use_dockerfile_local use_no_cache)

build-base-images use_no_cache="false": \
    (_build_base_images use_no_cache)

_touch_compose_override:
    touch ${ROOT_DIR}/env/local/docker/docker-compose.override.yml
