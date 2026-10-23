import './run.just'
import './build.just'
import './env-files.just'

restart use_dockerfile_local=default_use_dockerfile_local use_no_cache="false": \
    (down) \
    (pip-compile) \
    (build use_dockerfile_local use_no_cache) \
    (up use_dockerfile_local) \
