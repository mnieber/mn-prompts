import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("s40_a_developer_runs_the_servers")


def run_scenario():
    r.developer = c.External.Actors.Developer
    r.docker_compose = c.External.Actors.DockerCompose
    r.jazzoo_stub = c.Libs.Libraries.JazzooStub
    r.service_module = c.Services.Modules.ServiceJazzooFile
    r.init_dev_target = c.Services.Targets.InitDev
    r.run_server_target = c.Services.Targets.RunServer
    r.exec_target = c.Docker.Targets.Exec
    r.tmux_target = c.Tmux.Targets.Tmux
    r.service_run_server_target = c.ServiceLayers.Targets.RunServer
    r.service_shell_target = c.ServiceLayers.Targets.Shell
    r.service_tools = c.ServiceLayers.Scripts.ServiceTools

    with goal().install_the(r.jazzoo_stub).in_the(r.service_images):
        the(r.service_image).installs_the(r.jazzoo_stub).in_editable_mode()
        it().gets_the(r.console_scripts).from_the(r.stub_metadata)
        with the(r.docker_compose).starts_the(r.service_container):
            it().mounts_the(r.real_jazzoo_code).over_the(r.jazzoo_stub)

    with goal().prepare_a(r.service).for_development():
        with the(r.developer).runs(r.exec_target).with_the(r.init_dev_target):
            it().runs(r.jaz).in_the(r.service_container)
            the(r.jaz).loads_the(r.service_module).from_the(r.working_dir)
            it().runs_the(r.init_dev_target)

    with goal().run_the(r.servers).from_the(r.tmux_menu):
        the(r.developer).runs(r.tmux_target)
        it().picks_the(r.serve_commands).from_the(r.menu)
        with the(r.service_run_server_target).calls(r.service_tools):
            it().runs(r.run_server_target).in_the(r.service_container)
            it().shows_the(r.output).of_the(r.server).in_a(r.pane)

    with goal().open_a(r.shell).in_a(r.service_container):
        with the(r.developer).runs(r.service_shell_target):
            it().reads_the(r.shell_command).from_the(r.config)
            it().calls(r.service_tools).with_the(r.shell_command)


markdown_node = sunya.add_markdown_node(scenario, "A developer runs the servers")

markdown_node.markdown = """
Each service has a `jazzoo` file with its own targets, which run inside the container of the service: blogs_be has
the Postgres and Django targets (`create-db`, `migrate`, `run-server`, `init-dev`, ...), and blogs_fe has the React
targets (`install`, `run-server`, `init-dev`). jazzoo comes into the containers as a stub library.

## Diagram

```mermaid
flowchart TD
    build(["docker compose builds a service image"]) --> install
    start(["docker compose starts a service container"]) --> mount

    subgraph stub ["Install the jazzoo stub in the service images"]
        install["Install the jazzoo stub in editable mode [1]"] --> scripts["Create the console scripts of the stub [2]"]
        mount["Mount the real jazzoo code over the stub [3]"]
    end

    init(["The developer runs jaz init-dev in a service container with docker.exec"]) --> load

    subgraph prepare ["Prepare a service for development"]
        load["Load the jazzoo file of the service [4]"] --> init_dev["Run the init-dev target [5]"]
    end

    serve(["The developer runs jaz tmux, and picks the serve commands"]) --> run_server

    subgraph servers ["Run the servers from the tmux menu"]
        run_server["Run jaz run-server in the container of each service [6]"] --> output["Show the output of each server in its own pane"]
    end

    shell(["The developer runs jaz be.shell or jaz fe.shell"]) --> shell_command

    subgraph open_shell ["Open a shell in a service container"]
        shell_command["Read the shell command from the config [7]"] --> open["Open the shell in the container of the service"]
    end
```

### Footnotes

#### [1] - The service images install the stub from src/libs

Each service image installs the stub library in `src/libs/jazzoo` in editable mode. blogs_be installs it through
`requirements.editable`; the blogs_fe images first install `python3` and `bash`, which the alpine Node image
lacks.</br>

#### [2] - The stub declares the console scripts of jazzoo

The stub declares the same console scripts as jazzoo (`jaz`, `zoo`, ...), so the install creates them.</br>

#### [3] - jaz runs the real code without a rebuild

The real jazzoo code (`/home/maarten/projects/jazzoo/src`) is mounted over the stub in
`docker-compose.override.yml`.</br>

#### [4] - jaz loads the jazzoo file of the working directory

The developer runs e.g. `jaz docker.exec be cmd="jaz init-dev"`. In the container, `jaz` loads the `jazzoo` file of
the working directory (`/app/src`, the source of the service).</br>

#### [5] - init-dev prepares the database

The `init-dev` target creates the database and runs the migrations.</br>

#### [6] - The host has a layer per service

On the host, the `be` and `fe` layers (`env/local/jaz/be/be.jaz`, `env/local/jaz/fe/fe.jaz`) have the targets of
blogs_be and blogs_fe.</br>
The developer runs `jaz compose.up`, which starts the containers without the servers, and then `jaz tmux`, and picks
the commands of the `serve` category of the menu: `jaz be.run-server` and `jaz fe.run-server`.</br>
Each runs `jaz run-server` in the container of the service (`/be/container`, `/fe/container`) with
`service_tools.py`, which uses jazzoo's `run_docker`.</br>

#### [7] - The shell follows the docker shell by default

The shell command is `/be/shell` or `/fe/shell`. By default these follow `/docker/shell`.</br>
`jaz be.exec` and `jaz fe.exec` run any other command in the container in the same way.</br>
"""
