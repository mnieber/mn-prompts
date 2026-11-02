import sunya
from sunya import C as c
from sunya import R as r
from sunya import goal, it, the

scenario = sunya.add_scenario("s30_a_developer_restarts_the_stack")


def run_scenario():
    r.developer = c.External.Actors.Developer
    r.docker_compose = c.External.Actors.DockerCompose
    r.uv = c.External.Actors.Uv
    r.pip_compile_target = c.Python.Targets.PipCompile
    r.restart_target = c.Compose.Targets.Restart
    r.down_target = c.Compose.Targets.Down
    r.build_target = c.Compose.Targets.Build
    r.up_target = c.Compose.Targets.Up
    r.run_target = c.Compose.Targets.Run

    with goal().compile_the(r.requirements).of_the(r.python_services):
        with the(r.developer).runs(r.pip_compile_target):
            it().reads_the(r.python_services).from_the(r.config)
            with it().for_each_of_the(r.python_services):
                it().asks(r.uv).to_compile_the(r.requirements).with_the(r.libs_dir)

    with goal().restart_the(r.stack).after_a_change_of_the(r.dependencies):
        with the(r.developer).runs(r.restart_target):
            it().calls(r.down_target)
            it().calls(r.pip_compile_target)
            it().calls(r.build_target)
            it().calls(r.up_target)
            it().stops().if_a(r.step).fails()

    with goal().run_a(r.command).in_a(r.new_container):
        with the(r.developer).runs(r.run_target).with_a(r.service).and_a(r.command):
            it().asks(r.docker_compose).to_run_the(r.command).in_a(r.new_container)
            the(r.docker_compose).removes_the(r.new_container).when_the(
                r.command
            ).ends()


markdown_node = sunya.add_markdown_node(scenario, "A developer restarts the stack")

markdown_node.markdown = """
After a change of the dependencies, the developer compiles the requirements of the
Python services and restarts the stack. They also run one-off commands (e.g. the
migrations) in a new container of a service. `python.pip-compile` delegates to
`python_tools.py`, and the compose targets to `compose_tools.py`.

### Steps

#### It compiles the requirements of the Python services

The developer runs `jaz python.pip-compile`, which reads the services from
`/python/services`.</br>
For each service, it runs `uv pip compile` in the directory of the service, which
compiles `requirements.in` and `requirements.editable` into `requirements.txt`.
`BLOGS_LIBS_DIR` points to `src/libs`, so that the editable libraries
(`-e ${BLOGS_LIBS_DIR}/jazzoo`, ...) resolve.</br>

#### It restarts the stack

The developer runs `jaz compose.restart`, which stops the stack, compiles the
requirements, builds the images and starts the stack. Its `local` and `no-cache`
arguments are passed on to `build` and `up`.</br>
When a step fails, the restart stops.</br>

#### It runs a command in a new container

The developer runs e.g. `jaz compose.run blogs_be cmd="python manage.py migrate"`.
docker compose runs the command in a new container of the service, with the same
compose files as `up`, and removes the container when the command ends. Without
`cmd`, the container runs the command of the service.</br>

### Diagram

```mermaid
sequenceDiagram
    actor Developer
    participant PT as python_tools.py
    participant CT as compose_tools.py
    participant UV as uv
    participant DC as docker compose

    Note over Developer,DC: Compile the requirements
    Developer->>PT: jaz python.pip-compile
    PT->>PT: read /python/services
    loop each service
        PT->>UV: pip compile (BLOGS_LIBS_DIR=src/libs)
    end

    Note over Developer,DC: Restart the stack
    Developer->>CT: jaz compose.restart
    CT->>DC: down
    CT->>PT: pip-compile
    PT->>UV: pip compile
    CT->>DC: build
    CT->>DC: up

    Note over Developer,DC: Run a command in a new container
    Developer->>CT: jaz compose.run blogs_be cmd=...
    CT->>DC: run --rm blogs_be <cmd>
```
"""
