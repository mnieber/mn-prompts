import './build.just'
import './lib/_run_image.just'
import './lib/_run_command.just'
import './lib/_down.just'
import './lib/_up.just'

up use_dockerfile_local=default_use_dockerfile_local: \
    (_touch_compose_override) \
    (compile-env-files) \
    (_up use_dockerfile_local "true" "true")

down: (compile-env-files) (_down "true" "true")

shell service_name: (compile-env-files) (_run_command service_name "${BLOGS_SHELL_COMMAND}")

run_cmd service_name cmd use_dockerfile_local=default_use_dockerfile_local: \
    (compile-env-files) \
    (_run_image service_name use_dockerfile_local "true" "true" cmd)
