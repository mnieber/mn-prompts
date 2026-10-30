import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("s20_a_developer_builds_and_starts_the_stack")


def run_scenario():
    r.developer = c.External.Actors.Developer
    r.docker_compose = c.External.Actors.DockerCompose
    r.build_base_images_target = c.Compose.Targets.BuildBaseImages
    r.build_target = c.Compose.Targets.Build
    r.up_target = c.Compose.Targets.Up
    r.down_target = c.Compose.Targets.Down
    r.compile_env_files_action = c.Compose.Actions.CompileEnvFiles

    with goal().keep_the(r.developer_settings).in_a(r.local_config_layer):
        the(r.root_module).loads_the(r.base_config)
        it().loads_the(r.local_config).if_it_exists()
        the(r.local_config).overrides_the(r.base_config)

    with goal().build_the(r.images).of_the(r.stack):
        with the(r.developer).runs(r.build_base_images_target):
            it().reads_the(r.custom_packages).from_the(r.config)
            it().asks(r.docker_compose).to_build_the(r.base_images)
        with the(r.developer).runs(r.build_target):
            it().calls(r.compile_env_files_action)
            it().reads(r.use_dockerfile_local).from_the(r.config).unless_the(
                r.local_argument
            ).is_given()
            it().asks(r.docker_compose).to_build_the(r.service_images)

    with goal().compile_the(r.env_files).of_the(r.services):
        with the(r.compile_env_files_action).creates_the(
            r.secrets_file
        ).if_it_is_missing():
            it().renders_each(r.env_file_template).with_the(r.secrets)

    with goal().start_and_stop_the(r.stack):
        with the(r.developer).runs(r.up_target):
            it().creates_the(r.override_file).if_it_is_missing()
            it().calls(r.compile_env_files_action)
            it().asks(r.docker_compose).to_start_the(r.stack).with_the(r.compose_layers)
        with the(r.developer).runs(r.down_target):
            it().asks(r.docker_compose).to_stop_the(r.stack)


markdown_node = sunya.add_markdown_node(
    scenario, "A developer builds and starts the stack"
)

markdown_node.markdown = """
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
containers.</br>

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
    Developer->>CT: jaz compose.down
    CT->>DC: down --remove-orphans
```
"""
