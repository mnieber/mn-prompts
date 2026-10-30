# Skill: le-use-compose-ops

Applies when adding the `jaz compose.*` and `jaz python.*` targets to a stack: they build and run the
stack with Docker Compose, compile the env files, and compile the requirements of the Python services.

The `examples/blogs` stack has a complete setup. Copy its files and adapt the config.

---

## What the developer sees

```
$ jaz compose.build-base-images             # build the base images
$ jaz compose.build                         # build the images of the services
$ jaz compose.up                            # start the stack
$ jaz compose.init                          # init the services, run their servers, check the stack
$ jaz compose.down                          # stop the stack, remove its containers
$ jaz compose.down volumes=true             # ... and its volumes: the next up starts a new stack
$ jaz compose.restart                       # down, python.pip-compile, build, up
$ jaz compose.run blogs_be cmd="pytest"     # run a command in a new container
$ jaz compose.compile-env-files             # compile the .env.in files
$ jaz python.pip-compile                    # compile requirements.txt of the Python services
$ jaz python.publish package-dir=src/libs/x # build a library and upload it to PyPI
```

`jaz --list compose` lists the targets.

- `build`, `up`, `init`, `restart` and `run` take `local=true` to use the `Dockerfile.local` images, and `local=false`
  to use the `Dockerfile` images. Without `local`, `/compose/use_dockerfile_local` decides.
- `build`, `build-base-images` and `restart` take `no-cache=true` to build without the docker cache.
- `down` takes `volumes=true` (default `false`) to also remove the volumes of the stack (`down --volumes`), so that
  the next `up` starts with a new and uninitialised stack (e.g. an empty database).
- `build`, `up`, `down`, `run` and `init` first compile the env files. `up` and `init` first create an empty
  `docker-compose.override.yml` if it is missing.
- `run` passes the words of `cmd` after the service name; without `cmd`, the service runs its own command.
  The container is removed when the command ends.
- `python.publish` asks for the password before the upload. Its config (`/python/pypi`) and its rules are in
  [py-publish-to-pypi](../../python_lib/skills/py-publish-to-pypi.md).
- To open a shell in a running container, use `jaz docker.exec` (see
  [le-manage-docker-containers](./le-manage-docker-containers.md)); there is no `compose.shell`.

**When to use which target.** `compose.run` is the target to run commands when debugging or operating the
stack together with the developer. `compose.up`, `compose.down`, `compose.restart` and `compose.init` change the
developer's running stack: only run them when the developer asks.

### Typical workflow

```bash
# Initial setup
jaz compose.build-base-images
jaz compose.build
jaz compose.up

# Prepare the services (init-dev), and check that the stack works
jaz compose.init

# After dependency changes
jaz compose.restart
```

### Initialising the stack

In the base compose file, the services run `sleep infinity`, and the developer starts each server by hand (with
`jaz docker.exec` or the tmux menu). `compose.init` starts the stack in "init mode" instead, with
`docker-compose.init-stack.yml` as the last compose file:

- The overlay replaces the `command` of each service with `sh -c "jaz init-dev && exec jaz run-server"`, and gives
  it a healthcheck that runs `jaz check`. Its `depends_on` conditions start the services in order (blogs_be waits
  until postgres is healthy, blogs_fe until blogs_be is healthy).
- It runs `up --detach --force-recreate --wait --wait-timeout 600`: `--force-recreate` makes `init-dev` run again
  when the config did not change, and `--wait` fails when a service does not become healthy (or a failing
  `init-dev` stops its container). On a failure, it prints `logs --tail=50` of the stack.
- It then gets `/compose/init/homepage` from the host, and in a terminal asks whether to open it in the browser.
- The servers keep running in their containers. The next `compose.up` recreates the containers with
  `sleep infinity`, because the config of the services changed.

**RULE:** Every service in the overlay must have the `init-dev`, `run-server` and `check` targets (see
[le-add-python-service-to-src](./le-add-python-service-to-src.md) and
[le-add-react-service-to-compose](./le-add-react-service-to-compose.md)). `init-dev` must be safe to run again.

**RULE:** A service that has a `depends_on` with `condition: service_healthy` depends on a service with a
healthcheck: postgres has one (`pg_isready`) in the base compose file, the services get one in the overlay.

## Files

```
<stack>/
    jazzoo                                    # root module: loads the config, exports the layers
    env/local/
        .gitignore                            # docker/env_files/*.env, secrets.env, config/local.yaml
        secrets.env                           # the secrets of the env files (gitignored)
        config/base.yaml                      # /docker, /compose and /python
        config/local.yaml                     # the developer's own settings (gitignored, optional)
        jaz/compose/compose.jaz               # the compose targets
        jaz/compose/compose_tools.py          # the script that does the work
        jaz/python/python.jaz                 # the python targets
        jaz/python/python_tools.py            # the script that does the work
        scripts/compile_env_files.py          # compiles the .env.in files
        docker/                               # the compose files (incl. docker-compose.init-stack.yml)
                                              # and env_files/*.env.in
```

The root module loads the config and exports the layers:

```
⚙️.load_config(path=⚙️.module.dirname / "env/local/config/base.yaml")
⚙️.load_config(path=⚙️.module.dirname / "env/local/config/local.yaml", required=false)

from ./env/local/jaz/compose/compose.jaz export * as compose
from ./env/local/jaz/python/python.jaz export * as python
```

**RULE:** Copy `compose.jaz`, `compose_tools.py`, `python.jaz`, `python_tools.py` and `compile_env_files.py`
as they are. The only stack-specific name in them is `BLOGS_LIBS_DIR` in `python_tools.py`: rename it to
`<STACK>_LIBS_DIR`.

## The config

```yaml
# env/local/config/base.yaml
docker:
  compose_project: blogs
  shell: sh
compose:
  use_dockerfile_local: false
  os_custom_packages: ""
  pip_custom_packages: ""
  init:
    homepage: http://localhost:3000/
python:
  services:
    - blogs_be
  pypi:
    username: __token__
    publish_url: https://upload.pypi.org/legacy/
```

- `/docker/compose_project` is the Docker Compose project name: the stack name, in lower case. It prefixes
  the container names and networks.
- `/compose/use_dockerfile_local` is the default of `local`.
- `/compose/os_custom_packages` and `/compose/pip_custom_packages` are passed to `build-base-images` as the
  build args `OS_CUSTOM_PACKAGES` and `PIP_CUSTOM_PACKAGES` when they are not empty (see
  [le-add-base-image](./le-add-base-image.md)).
- `/compose/init/homepage` is the url that `compose.init` checks from the host, and offers to open.
- `/python/services` lists the services whose requirements `python.pip-compile` compiles.
- `/python/pypi` holds the user name and the upload url of `python.publish`.

### The developer's own settings

`env/local/config/local.yaml` is a config layer that belongs to the developer. It is not in git, and the
stack works without it. Because the root module loads it after `base.yaml`, it overrides it:

```yaml
# env/local/config/local.yaml
docker:
  shell: fish
compose:
  use_dockerfile_local: true
  os_custom_packages: nano curl fish
```

**RULE:** Don't create or edit `local.yaml` for the developer, unless they ask. Put the defaults of the
stack in `base.yaml`.

## How the targets work

`compose.jaz` is a thin wrapper that calls `⚙️.python compose_tools.py <action> --root-dir=<root dir> ...`.
It turns the arguments into flags of the script (`--local`, `--no-cache`, `--volumes`), so that jazzoo decides
whether an argument is true. The default of `local` is a call in the parameter list
(`local=🐭.use-dockerfile-local()`), which reads `/compose/use_dockerfile_local` with `⚙️.get_config`.
The script runs `docker compose` with `ROOT_DIR` (the compose files use `${ROOT_DIR}`),
`COMPOSE_PROJECT_NAME` (from `/docker/compose_project`) and `DOCKER_BUILDKIT=1` in its environment. The
compose files of each command:

| command           | compose files                                                                          |
| ----------------- | -------------------------------------------------------------------------------------- |
| build             | `docker-compose.yml` (+ `docker-compose.dockerfile-local.yml`)                         |
| build-base-images | `docker-compose.base-images.yml`                                                       |
| up, run           | `docker-compose.yml`, `.src-overlays.yml` (+ `.dockerfile-local.yml`), `.override.yml` |
| init              | the files of up, then `.init-stack.yml`                                                |
| down              | `docker-compose.yml`, `.src-overlays.yml`, `.override.yml`                             |

`python_tools.py pip-compile` runs `uv pip compile` in `src/services/<service>` of each service in
`/python/services`, with `<STACK>_LIBS_DIR` set to `<root dir>/src/libs`, so that the `-e
${<STACK>_LIBS_DIR}/...` lines of `requirements.editable` resolve.

A failing `docker` or `uv` command ends the target with its exit code, without a traceback.

## Env files

`compose.compile-env-files` creates `secrets.env` if it is missing, and runs `compile_env_files.py`, which
renders each `env/local/docker/env_files/<service>.env.in` into `<service>.env`.

- In a `.env.in` file, reference a secret with `${VARIABLE_NAME}`, where `VARIABLE_NAME` is defined in
  `secrets.env`. Non-secrets are hard-coded in the `.env.in` file.
- A secret that is not defined in `secrets.env` (or the environment) makes the compilation fail.
- `compile_env_files.py` needs `expandvars`: the developer installs it next to jazzoo
  (`pip install expandvars`).

## Requirements

- `jaz` is installed, and `⚙️.python` (the Python that runs `jaz`) has `expandvars`.
- `docker` (with compose) and `uv` are on the `PATH`.

## Checklist

- [ ] The root `jazzoo` file loads `base.yaml` and the optional `local.yaml`, and exports `compose` and `python`
- [ ] `compose.jaz`, `compose_tools.py`, `python.jaz`, `python_tools.py` and `compile_env_files.py` are copied
- [ ] `BLOGS_LIBS_DIR` is renamed to `<STACK>_LIBS_DIR` in `python_tools.py`
- [ ] `base.yaml` has `/docker/compose_project`, `/compose/*` (with `/compose/init/homepage`), `/python/services`
      and `/python/pypi`
- [ ] `docker/docker-compose.init-stack.yml` gives each service the init-and-serve `command`, a `jaz check`
      healthcheck and its `depends_on` conditions
- [ ] `env/local/.gitignore` excludes `docker/env_files/*.env`, `secrets.env` and `config/local.yaml`
- [ ] Non-secrets are hard-coded in the `.env.in` files
