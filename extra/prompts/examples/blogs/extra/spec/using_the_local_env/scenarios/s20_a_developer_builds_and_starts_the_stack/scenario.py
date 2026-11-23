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
The developer builds and runs the blogs stack with the `compose` layer of the root module. The targets run
`docker compose` with the compose files of the local env.

## Diagram

```mermaid
flowchart TD
    load(["jaz loads the root module"]) --> base

    subgraph settings ["Keep the developer's settings in a local config layer"]
        base["Load base.yaml"] --> has_local{{"Does local.yaml exist?"}}:::choice
        has_local -- yes --> local["Load local.yaml, which overrides base.yaml [1]"]
    end

    build_base(["The developer runs jaz compose.build-base-images"]) --> base_images
    build_stack(["The developer runs jaz compose.build"]) --> compile_for_build

    subgraph build ["Build the images of the stack"]
        base_images["Build the base images with the custom packages [2]"]
        compile_for_build["Compile the env files"] --> use_local{{"Use the Dockerfile.local files? [3]"}}:::choice
        use_local -- yes --> local_images["Build the images from the Dockerfile.local files"]
        use_local -- no --> images["Build the images from the Dockerfiles"]
    end

    compile(["compose.build and compose.up compile the env files"]) --> has_secrets

    subgraph env_files ["Compile the env files of the services"]
        has_secrets{{"Does secrets.env exist?"}}:::choice
        has_secrets -- no --> create_secrets["Create an empty secrets.env"]
        has_secrets -- yes --> render["Render each env file template with the secrets [4]"]
        create_secrets --> render
    end

    up(["The developer runs jaz compose.up"]) --> override
    down(["The developer runs jaz compose.down"]) --> stop

    subgraph start_and_stop ["Start and stop the stack"]
        override["Create the override file if it is missing"] --> compile_for_up["Compile the env files"]
        compile_for_up --> start["Start the stack with the compose layers [5]"]
        stop["Stop the stack [6]"]
    end

    classDef choice color:#c9a227
```

### Footnotes

#### [1] - local.yaml holds the settings of the developer

`local.yaml` belongs to the developer and is not in git. Because it is loaded last, it overrides `base.yaml`, e.g.
`/compose/use_dockerfile_local`, `/compose/os_custom_packages` and `/docker/shell`.</br>

#### [2] - The compose targets delegate to compose_tools.py

Each target delegates to `compose_tools.py`, which runs with `⚙️.python`, the Python that runs `jaz`, so that it can
import `jazzoo`.</br>
`compose.build-base-images` passes the custom packages of `/compose` as build args, and builds the images of
`docker-compose.base-images.yml`.</br>

#### [3] - The local argument overrides the config

The images are built from the `Dockerfile.local` files when `local=true` is given, or when
`/compose/use_dockerfile_local` is true and `local` is not given.</br>

#### [4] - The env files are rendered from templates

`compile_env_files` renders each `env/local/docker/env_files/<service>.env.in` into `<service>.env`, filling in the
secrets of `secrets.env`.</br>

#### [5] - The stack is started with the compose layers

The compose layers are the base file, the src overlays, the `Dockerfile.local` images (when local is on) and the
override file.</br>

#### [6] - compose.down can also remove the volumes

`compose.down` stops the stack and removes its containers. With `volumes=true`, it also removes the volumes of the
stack, so that the next `compose.up` starts with a new and uninitialised stack.</br>
"""
