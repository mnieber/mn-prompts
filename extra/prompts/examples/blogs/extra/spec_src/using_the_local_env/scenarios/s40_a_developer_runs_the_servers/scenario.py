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
        with the(r.exec_target).runs(r.run_server_target).in_each(r.service_container):
            it().shows_the(r.output).of_the(r.server).in_a(r.pane)


markdown_node = sunya.add_markdown_node(scenario, "A developer runs the servers")

markdown_node.markdown = """
Each service has a `jazzoo` file with its own targets, which run inside the
container of the service: blogs_be has the Postgres and Django targets (`create-db`,
`migrate`, `run-server`, `init-dev`, ...), and blogs_fe has the React targets
(`install`, `run-server`, `init-dev`). jazzoo comes into the containers as a stub
library.

### Steps

#### It installs the jazzoo stub in the service images

Each service image installs the stub library in `src/libs/jazzoo` in editable mode.
blogs_be installs it through `requirements.editable`; the blogs_fe images first
install `python3` and `bash`, which the alpine Node image lacks.</br>
The stub declares the same console scripts as jazzoo (`jaz`, `zoo`, ...), so the
install creates them.</br>
When docker compose starts a container, it mounts the real jazzoo code
(`/home/maarten/projects/jazzoo/src`, in `docker-compose.override.yml`) over the
stub, so that `jaz` runs the real code without a rebuild.</br>

#### It prepares a service for development

The developer runs e.g. `jaz docker.exec be cmd="jaz init-dev"`.</br>
In the container, `jaz` loads the `jazzoo` file of the working directory
(`/app/src`, the source of the service), and runs its `init-dev` target, which
creates the database and runs the migrations.</br>

#### It runs the servers from the tmux menu

The developer runs `jaz tmux`, and picks the commands of the `serve` category of
the menu.</br>
Each command (`zoo docker.exec blogs_be cmd="jaz run-server"`, ...) runs the
`run-server` target in the container of the service, and shows the output of the
server in its own pane.</br>

### Diagram

```mermaid
sequenceDiagram
    actor Developer
    participant Image as service image
    participant DC as docker compose
    participant Exec as docker.exec
    participant Jaz as jaz (in the container)
    participant Tmux as tmux menu

    Note over Developer,Tmux: Install the jazzoo stub
    Image->>Image: pip install -e /app/libs/jazzoo (stub)
    DC->>DC: mount jazzoo/src over /app/libs/jazzoo

    Note over Developer,Tmux: Prepare a service for development
    Developer->>Exec: jaz docker.exec be cmd="jaz init-dev"
    Exec->>Jaz: jaz init-dev
    Jaz->>Jaz: load /app/src/jazzoo
    Jaz->>Jaz: create-db, migrate, collect-static, create-superuser

    Note over Developer,Tmux: Run the servers
    Developer->>Tmux: jaz tmux, pick the serve commands
    loop each serve command
        Tmux->>Exec: zoo docker.exec <service> cmd="jaz run-server"
        Exec->>Jaz: jaz run-server
    end
```
"""
