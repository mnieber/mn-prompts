# Skill: le-manage-docker-containers

Applies when adding the `jaz docker.*` targets to a stack: they open a shell in, kill, inspect or commit the
stack's running containers.

The `examples/blogs` stack has a complete setup. Copy its files and adapt the config.

---

## What the developer sees

```
$ jaz docker.exec be                    # a shell in blogs_be
$ jaz docker.exec be cmd=bash           # bash instead of the default shell
$ jaz docker.exec postgres user=postgres cmd=psql
$ jaz docker.kill                       # pick one or more containers to kill
$ jaz docker.inspect be                 # docker inspect blogs_be
$ jaz docker.inspect ip=true            # pick containers, print their IP addresses
$ jaz docker.commit be                  # commit blogs_be to its image
```

`jaz --list docker` lists the targets.

**Picking a container.** `name` is the first parameter, so it may be given without `name=`.

- A name that is exactly the name of a container picks that container.
- Otherwise, a name that is part of exactly one container's name picks that container (`be` → `blogs_be`).
- Without a name, when the name matches several containers, or when it matches none, the developer picks from
  a numbered list of containers, or types `0` to exit. `kill` and `inspect` accept several containers
  (`1,3-4`); `exec` and `commit` take one.

**exec.** Without `cmd`, `exec` opens the shell in `/docker/shell`. `cmd` is split into words like a shell
would, but it does not run in a shell: use `cmd="sh -c '...'"` for pipes, `$VAR` or `$(...)`. The exit code
of the shell or command becomes the exit code of the target.

## Files

```
<stack>/
    jazzoo                                  # root module: loads the config, exports the docker layer
    env/local/config/base.yaml              # the compose project and the default shell
    env/local/jaz/docker/docker.jaz         # the docker.* targets
    env/local/jaz/docker/docker_tools.py    # the script that does the work
```

Copy `docker.jaz` and `docker_tools.py` from `examples/blogs/env/local/jaz/docker/` unchanged. They contain
nothing that is specific to the stack.

## The root module

If the stack has no `jazzoo` file yet, create it. Otherwise add the missing lines to the existing one:

```
⚙️.load_config(path=⚙️.module.dirname / "env/local/config/base.yaml")

from ./env/local/jaz/docker/docker.jaz export * as docker
```

## The config

```yaml
# env/local/config/base.yaml
docker:
  compose_project: <stack_name>
  shell: sh
```

- `/docker/compose_project` limits the containers to the running containers of that compose project (the
  `com.docker.compose.project` label). Without it, all running containers are listed.
- `/docker/shell` is the shell that `exec` opens when no `cmd` is given. Without it, `sh` is used.

`/docker/compose_project` is also the `COMPOSE_PROJECT_NAME` that the `compose` layer starts the stack with
(see `le-use-compose-ops`), so the two always match.

RULE: use a shell that exists in every container of the stack. `sh` does; `bash` and `fish` are often missing
in images such as `postgres`. A developer who prefers another shell passes `cmd=fish`, or sets `/docker/shell`
in their own `env/local/config/local.yaml`.

## How it works, and what to keep when changing it

Each target calls `⚙️.python docker_tools.py <action> --name=<name> ...`. The script lists the containers with
`docker ps`, picks one or more, and runs docker with `from jazzoo import run`. It reads `/docker` with
`from jazzoo import get_config`.

RULE: the targets are `[interactive]`, so that `jaz` does not capture their output: the picker asks the
developer, and `exec` needs the terminal (`docker exec -it`).

RULE: the targets quote their string arguments with `⚙️.sh-quote`, because they are command-line arguments.

RULE: `commit` writes to the image that the container was started from, so that the next `up` uses it. It
does not create a new image name.

Compose itself (`up`, `down`, `build`) is not part of this layer: it goes through the `compose` layer (see
`le-use-compose-ops`).

## Requirements

- `docker` is installed, and the developer may run it without `sudo`.
- `jaz` is installed. The scripts run with `⚙️.python`, the Python that runs `jaz`, so they can import `jazzoo`.

## Checklist

- [ ] `docker.jaz` and `docker_tools.py` copied to `env/local/jaz/docker/`
- [ ] `env/local/config/base.yaml` defines `/docker/compose_project` (and optionally `/docker/shell`)
- [ ] The root `jazzoo` module loads the config and exports the `docker` layer
- [ ] `jaz --list docker` shows `docker.exec`, `docker.kill`, `docker.inspect` and `docker.commit`
- [ ] With the stack running, `jaz docker.exec` lists the stack's containers and opens a shell in the picked one
