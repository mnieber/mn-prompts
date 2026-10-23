# Skill: le-write-dodo-config-files

Applies when setting up dodo_commands configuration files for a stack.

Primary reference: `../examples/blogs/src/.dodo/`, `../examples/blogs/src/services/blogs_be/.dodo/`, `../examples/blogs/src/services/blogs_fe/.dodo/`

---

## What this skill covers

This skill describes the dodo_commands config files that can optionally be used (when the user indicates this) for a stack:

- The main `.dodo_commands/config.yaml` file at the project root (outside `src/`)
- The `stack.root.yaml` file for the root of the `src/` directory
- The `stack.<service_name>.yaml` files for each service

## What this skill does NOT cover

- **dodo commands themselves** → see target-specific documentation
- **tmux/menu configuration** → only the `stack.root.yaml` structure is covered here

---

## The main config.yaml

The `config.yaml` file lives at `<project_root>/.dodo_commands/config.yaml` (i.e. **outside** `src/`). It is not part of the `src/` directory that is checked into the stack's git repository. If you want to update this file, you can try running `dodo which --config` or else ask the user for its location.

```yaml
ROOT:
  command_path:
    - /home/maarten/.dodo_commands/default_project/commands/*
  version: 1.0.0
  src_dir: /path/to/project/examples/blogs/src

DIAL:
  default:
    "1": "dodo root."
    "2": "dodo blogs_be."
    "3": "dodo blogs_fe."
  shift:
    "1": ${/ROOT/src_dir}/
    "2": ${/ROOT/src_dir}/services/blogs_be
    "3": ${/ROOT/src_dir}/services/blogs_fe
  ctrl:
    "1": ${/ROOT/project_dir}/
    "2": ${/ROOT/config_dir}/
    "3": ~/

LAYER_GROUPS:
  stack:
    - root:
        target_path: ${/ROOT/src_dir}/.dodo/stack.root.yaml
    - blogs_be:
        target_path: ${/ROOT/src_dir}/services/blogs_be/.dodo/stack.blogs_be.yaml
    - blogs_fe:
        target_path: ${/ROOT/src_dir}/services/blogs_fe/.dodo/stack.blogs_fe.yaml
```

### Key fields

**ROOT.src_dir:** Absolute path to the `src/` directory of the stack. Set this to the developer's actual checkout path.

**DIAL:** Keyboard shortcut bindings for quickly jumping to directories. The `default` group types a prefix in the current terminal window, which makes it faster to run commands for that lyayer. The `shift` (when the shift key is pressed) and `ctrl` (when ctrl is pressed) keys cd to a directory.

**LAYER_GROUPS.stack:** Lists every dodo layer file in the stack. Each entry has a name and a `target_path` pointing to the corresponding `stack.<name>.yaml` file. Add one entry per service.

**RULE:** `src_dir` must be an absolute path on the developer's machine. This file is not committed to the repo.

**RULE:** Every service that has a `stack.<name>.yaml` file must be listed in `LAYER_GROUPS.stack`.

---

## stack.root.yaml

Located at `src/.dodo/stack.root.yaml`. Defines top-level commands and the tmux session for the whole stack.

Primary reference: `../examples/blogs/src/.dodo/stack.root.yaml`

```yaml
COMMANDS:
  list:
    "~build":
      run: [cmd: just, build, ""]
    "~down":
      run: [cmd: just, down]
    "~restart":
      run: [cmd: just, restart]
    "~mt":
      run: [cmd: dodo, root.menu, --tmux]
    "~up":
      run: [cmd: just, up]

MENU:
  session_id: blogs
  commands:
    serve:
      - dodo blogs_be.serve
      - dodo blogs_fe.serve

ROOT: {}
```

### Key fields

**COMMANDS.list:** Shortcut commands runnable from the stack root. Each key starting with `~` is a named shortcut. The `run` field specifies the command to execute.

**MENU.session_id:** The tmux session name for this stack. Use the stack name (e.g., `blogs`).

**MENU.commands.serve:** The list of dodo commands that are launched when starting a development session. Add one entry per service that needs to run a server.

**RULE:** Add a `serve` entry for each service that has a `serve` command in its stack yaml.

---

## stack.\<service_name\>.yaml

Located at `src/services/<service_name>/.dodo/stack.<service_name>.yaml`. Defines the commands and Docker container for a specific service.

### Python service example

Primary reference: `../examples/blogs/src/services/blogs_be/.dodo/stack.blogs_be.yaml`

```yaml
COMMANDS:
  list:
    "~dm":
      run: [in: docker, cmd: python, manage.py]
    "~just":
      run: [in: docker, cmd: just]
    "~serve":
      run: [in: docker, cmd: just, run-server]
    "~shell":
      run: [in: docker, cmd: fish]

DOCKER:
  container: blogs_be

ROOT: {}

SERVER:
  install_dir: /app
  src_dir: ${/SERVER/install_dir}/src
```

### Frontend service example

Primary reference: `../examples/blogs/src/services/blogs_fe/.dodo/stack.blogs_fe.yaml`

```yaml
COMMANDS:
  list:
    "~just":
      run: [in: docker, cmd: just]
    "~serve":
      run: [in: docker, cmd: just, run-server]
    "~shell":
      run: [in: docker, cmd: fish]

DOCKER:
  container: blogs_fe

ROOT:
  decorators:
    docker:
      - exec
      - make
      - npm-publish

SERVER:
  install_dir: /app
  src_dir: ${/SERVER/install_dir}/src
```

### Key fields

**DOCKER.container:** The Docker container name that dodo will `exec` into when running commands with `in: docker`. This must match the `container_name` set in `docker-compose.yml` for this service (see `layers/local_env/skills/le-add-python-service-to-compose.md`).

```yaml
DOCKER:
  container: blogs_be # must match container_name in docker-compose.yml
```

**COMMANDS.list:** Named shortcut commands for this service. Commands with `in: docker` are executed inside the container.

**SERVER.install_dir / SERVER.src_dir:** Paths inside the container. `install_dir` is `/app` and `src_dir` is `/app/src`, matching the WORKDIR set in the Dockerfile.

**ROOT:** Can be empty (`{}`) or contain `decorators` for additional dodo decorator support.

**RULE:** `DOCKER.container` must exactly match the `container_name` value in `docker-compose.yml`. If they differ, dodo commands will fail to find the container.

**RULE:** Every service stack yaml must include a `~serve` command that starts the service's development server.

**RULE:** Every service stack yaml must include a `~shell` command for opening an interactive shell in the container.

---

## Checklist

- [ ] `.dodo_commands/config.yaml` created at the project root (outside `src/`)
- [ ] `ROOT.src_dir` set to the correct absolute path for this developer's checkout
- [ ] All services listed in `LAYER_GROUPS.stack` with correct `target_path` values
- [ ] `src/.dodo/stack.root.yaml` created with `MENU.session_id` set to the stack name
- [ ] `MENU.commands.serve` lists all services that have a `serve` command
- [ ] Each service has `src/services/<name>/.dodo/stack.<name>.yaml`
- [ ] `DOCKER.container` in each service stack yaml matches `container_name` in `docker-compose.yml`
- [ ] Each service stack yaml includes `~serve` and `~shell` commands
- [ ] `SERVER.install_dir` and `SERVER.src_dir` reflect the container's `/app` layout
