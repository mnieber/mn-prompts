[comment]: <> (This file is auto-generated. Do not edit directly.)

# s30_a_developer_restarts_the_stack

## A developer restarts the stack

After a change of the dependencies, the developer compiles the requirements of the Python services and restarts
the stack. They also run one-off commands (e.g. the migrations) in a new container of a service.

## Diagram

```mermaid
flowchart TD
    pip_compile(["The developer runs jaz python.pip-compile"]) --> services

    subgraph compile ["Compile the requirements of the Python services"]
        services["Read the Python services from the config"] --> each_service["Compile the requirements of each service with uv [1]"]
    end

    restart(["The developer runs jaz compose.restart"]) --> stop

    subgraph restart_stack ["Restart the stack after a change of the dependencies"]
        stop["Stop the stack"] --> requirements["Compile the requirements"]
        requirements --> build["Build the images"]
        build --> start["Start the stack [2]"]
    end

    run(["The developer runs jaz compose.run with a service and a command"]) --> new_container

    subgraph run_command ["Run a command in a new container"]
        new_container["Run the command in a new container of the service [3]"] --> remove["Remove the container when the command ends"]
    end
```

### Footnotes

#### [1] - uv resolves the editable libraries in src/libs

`python.pip-compile` delegates to `python_tools.py`, which reads the services from `/python/services`.</br>
For each service, it runs `uv pip compile` in the directory of the service, which compiles `requirements.in` and
`requirements.editable` into `requirements.txt`. `BLOGS_LIBS_DIR` points to `src/libs`, so that the editable
libraries (`-e ${BLOGS_LIBS_DIR}/jazzoo`, ...) resolve.</br>

#### [2] - The restart stops when a step fails

`compose.restart` delegates to `compose_tools.py`. Its `local` and `no-cache` arguments are passed on to `build` and
`up`.</br>
When a step fails, the restart stops.</br>

#### [3] - The command runs with the compose files of up

The developer runs e.g. `jaz compose.run blogs_be cmd="python manage.py migrate"`. docker compose runs the command in
a new container of the service, with the same compose files as `up`. Without `cmd`, the container runs the command of
the service.</br>

