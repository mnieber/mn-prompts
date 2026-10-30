# Blogs

An example stack with a Django backend (`src/services/blogs_be`), a React frontend (`src/services/blogs_fe`) and
PostgreSQL, which run in Docker containers. You operate the stack with `jaz` targets: run them from this directory.
`jaz --list-all` lists them.

## Requirements

- `jaz` (jazzoo), with `expandvars` installed next to it (`pip install expandvars`)
- `docker` with compose, and `tmux`

## First time: initialise the stack

Build the images, and then initialise the stack:

```
$ jaz compose.build-base-images
$ jaz compose.build
$ jaz compose.init
```

`compose.init` prepares every service for development (it creates the database, runs the migrations, creates the
superuser and installs the node modules), starts the servers and waits until the stack is healthy. Then it checks
the homepage (http://localhost:3000/) and offers to open it in the browser.

The servers keep running in their containers. `docker logs -f blogs_be` shows the output of a server.

## Day to day: start the services by hand

When the stack is initialised, start it without the servers, and run the servers yourself:

```
$ jaz compose.up       # start the containers (the servers don't run yet)
$ jaz tmux             # in another terminal: open the tmux session of the stack
```

The tmux session shows a menu with two commands:

```
 1 [serve] - jaz be.run-server
 2 [serve] - jaz fe.run-server
```

Pick `1,2` to run both servers, each in its own pane, so that you can watch their output and restart them.

To work in a container, open its shell, or run a command in it:

```
$ jaz be.shell         # the shell of /be/shell in blogs_be
$ jaz fe.shell         # the shell of /fe/shell in blogs_fe
$ jaz be.exec "python manage.py check"
```

`jaz compose.down` stops the stack. `jaz compose.down volumes=true` also removes its volumes (e.g. the database), so
that you can start again with `jaz compose.init`.

## Configuration

The config is in `env/local/config/base.yaml`. Put your own settings in `env/local/config/local.yaml`, which
overrides it and is not checked in, e.g.:

```yaml
docker:
  shell: fish # the shell of docker.exec, and of be.shell and fe.shell
compose:
  use_dockerfile_local: true # build and run the Dockerfile.local images
```

`jaz config.print` prints the merged config, and `jaz config.edit` opens the config files.

## Function keys (fish)

`zoo dial.install-fish` installs key bindings in fish (see `/dial` in the config):

| Key      | Does                                  |
| -------- | ------------------------------------- |
| F2       | inserts `zoo be.`                     |
| F3       | inserts `zoo fe.`                     |
| Shift+F1 | goes to this directory                |
| Shift+F2 | goes to `src/services/blogs_be`       |
| Shift+F3 | goes to `src/services/blogs_fe`       |
