[comment]: <> (This file is auto-generated. Do not edit directly.)

# s20_a_developer_builds_and_starts_the_stack

## A developer builds and starts the stack

The developer builds and runs the blogs stack with the `compose` layer of the root
module (`jaz compose.build-base-images`, `compose.build`, `compose.up` and
`compose.down`). Each target delegates to `compose_tools.py`, which runs
`docker compose` with the compose files of the local env. The scripts run with
`⚙️.python`, the Python that runs `jaz`, so that they can import `jazzoo`.

### Steps

#### It keeps the developer's settings in a local config layer

The root module loads `env/local/config/base.yaml`, and then
`env/local/config/local.yaml` if it exists.</br>
`local.yaml` belongs to the developer and is not in git. Because it is loaded last,
it overrides `base.yaml`, e.g. `/compose/use_dockerfile_local`,
`/compose/os_custom_packages` and `/docker/shell`.</br>

#### It builds the images of the stack

The developer runs `jaz compose.build-base-images`. It passes the custom packages of
`/compose` as build args, and builds the images of
`docker-compose.base-images.yml`.</br>
The developer runs `jaz compose.build`. It first compiles the env files. The images
are built from the `Dockerfile.local` files when `local=true` is given, or when
`/compose/use_dockerfile_local` is true and `local` is not given.</br>

#### It compiles the env files of the services

`compile_env_files` creates an empty `secrets.env` if it is missing, and renders each
`env/local/docker/env_files/<service>.env.in` into `<service>.env`, filling in the
secrets of `secrets.env`.</br>

#### It starts and stops the stack

The developer runs `jaz compose.up`. It creates an empty
`docker-compose.override.yml` if it is missing, compiles the env files, and starts
the stack with the compose layers: the base file, the src overlays, the
`Dockerfile.local` images (when local is on) and the override file.</br>
The developer runs `jaz compose.down`, which stops the stack and removes its
containers. With `volumes=true`, it also removes the volumes of the stack, so that
the next `compose.up` starts with a new and uninitialised stack.</br>

### Diagram

```mermaid
sequenceDiagram
    actor Developer
    participant Root as root module
    participant CT as compose_tools.py
    participant CEF as compile_env_files
    participant DC as docker compose

    Note over Developer,DC: Keep the developer's settings in a local config layer
    Root->>Root: load base.yaml
    Root->>Root: load local.yaml (if it exists)

    Note over Developer,DC: Build the images of the stack
    Developer->>CT: jaz compose.build-base-images
    CT->>DC: build (base-images, --build-arg ...)
    Developer->>CT: jaz compose.build [local=]
    CT->>CEF: compile
    CT->>DC: build (base [+ dockerfile-local])

    Note over Developer,DC: Compile the env files
    CEF->>CEF: create secrets.env if missing
    CEF->>CEF: render *.env.in into *.env

    Note over Developer,DC: Start and stop the stack
    Developer->>CT: jaz compose.up [local=]
    CT->>CT: create override file if missing
    CT->>CEF: compile
    CT->>DC: up (base, src-overlays [, dockerfile-local], override)
    Developer->>CT: jaz compose.down [volumes=]
    CT->>DC: down --remove-orphans [--volumes]
```

