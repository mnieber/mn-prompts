# Skill: le-add-react-service-to-compose

Applies when adding a React (Vite) frontend service to the Docker Compose configuration for local development.

Primary reference: `../examples/blogs/src/services/blogs_fe/`, `../examples/blogs/env/local/docker/`

---

## What this skill covers

- The frontend service's Dockerfile and Dockerfile.local
- Adding the service to `docker-compose.yml`
- Adding the service to `docker-compose.dockerfile-local.yml`
- Adding the service to `docker-compose.src-overlays.yml`
- Creating the service's environment file template
- Minimal Justfile commands for the service

## What this skill does NOT cover

- **Adding the service to `docker-compose.override.yml`** → follow the same interactive process described in `layers/local_env/skills/le-add-python-service-to-compose.md`
- **React/Vite project structure and configuration** → see `targets/react_app`

---

## Dockerfile and Dockerfile.local

Unlike Python services, the frontend service does **not** use a shared base image. It builds directly from an official Node image.

### Dockerfile (production)

```dockerfile
FROM node:18-alpine

# install pkg dependencies
RUN apk update && apk add \
    make

# install dev pkg dependencies
RUN apk update && apk add \
    curl \
    fish \
    nano

WORKDIR /app/src
```

### Dockerfile.local (development)

`Dockerfile.local` uses a newer Node version, enables corepack (for yarn), and installs `just`:

```dockerfile
FROM node:20-alpine

# install pkg dependencies
RUN apk update && apk add \
    make

RUN corepack enable

# install dev pkg dependencies
RUN apk update && apk add \
    bash \
    curl \
    fish \
    nano

# Install just
RUN curl --proto '=https' --tlsv1.2 -sSf https://just.systems/install.sh | bash -s -- --to /usr/local/bin

WORKDIR /app/src
```

**RULE:** Node modules are not installed during the Docker build. They are installed at runtime via `just install` (or `just init-dev`) after the container starts, because they live inside the src-overlaid directory.

**RULE:** Set `WORKDIR` to `/app/src` to match the src-overlay mount point.

---

## Adding to docker-compose.yml

```yaml
services:
  blogs_fe:
    container_name: blogs_fe
    build:
      context: ${ROOT_DIR}/src
      dockerfile: services/blogs_fe/Dockerfile
    command: sleep infinity
    depends_on:
      - blogs_be
    env_file:
      - ./env_files/blogs_fe.env
    image: blogs_fe
    ports:
      - 3000:3000 # React
      - 6008:6008 # Storybook
```

**depends_on:** The frontend depends on the backend service so the API is available when the frontend starts.

**ports:** Expose the Vite dev server port (3000) and Storybook port (6008). Adjust if your project uses different ports.

---

## Adding to docker-compose.dockerfile-local.yml

```yaml
services:
  blogs_fe:
    build:
      context: ${ROOT_DIR}/src
      dockerfile: services/blogs_fe/Dockerfile.local
    image: blogs_fe_local
```

---

## Adding to docker-compose.src-overlays.yml

```yaml
services:
  blogs_fe:
    volumes:
      - ${ROOT_DIR}/src/services/blogs_fe:/app/src
```

The entire service directory is mounted to `/app/src`. This includes `package.json`, source files, and — once installed — `node_modules`.

**RULE:** Do not add a separate volume for `node_modules`. They live inside the mounted service directory and are installed there at runtime.

---

## Creating the environment file template

Create `env/local/docker/env_files/blogs_fe.env.in`:

```bash
VITE_LOCALHOST_API_ENDPOINT=http://localhost:8000/api
```

Frontend environment variables exposed to Vite must be prefixed with `VITE_`. Non-secret values like API endpoints are hard-coded directly in the `.env.in` file.

**RULE:** Find out which port (e.g. `8000`) is used by the backend service (e.g. `blogs_be`) that is targetted by the react service (e.g. `blogs_fe`).

**RULE:** Only add a variable to `secrets.env` if it is genuinely secret. API endpoint URLs are not secrets and belong directly in `.env.in`.

---

## Minimal Justfile commands

Every frontend service must provide at minimum:

```makefile
#
# React
#

install:
    yarn install

run-server:
    yarn dev --host

storybook:
    yarn storybook dev --port 6008

#
# Stack
#

init-dev: \
    install
```

**run-server:** Must pass `--host` so the Vite dev server binds to `0.0.0.0` and is reachable from the host machine via the exposed port.

**init-dev:** Called once after the container first starts to install node modules.

## Optional Justfile commands

It can optionally also provide this command (which is run on the host)

```
create-opt-paths:
    sudo mkdir -p /opt/projects/blogs/blogs_fe
    sudo echo     "- cmd: echo 'start of the fish history'" >> /opt/projects/blogs/blogs_fe/fish_history
    sudo chmod -R 777 /opt/projects/blogs
```

---

## Checklist

- [ ] `Dockerfile` created using `node:18-alpine` (or appropriate version)
- [ ] `Dockerfile.local` created using a newer Node version with `corepack enable` and `just` installed
- [ ] Both Dockerfiles use `WORKDIR /app/src`
- [ ] Service added to `docker-compose.yml` with `sleep infinity`, correct ports, and `depends_on` the backend
- [ ] Service added to `docker-compose.dockerfile-local.yml` with `_local` image suffix
- [ ] Service added to `docker-compose.src-overlays.yml` mounting to `/app/src`
- [ ] Environment file template created at `env_files/blogs_fe.env.in`
- [ ] `VITE_` prefix used for variables that must be accessible in the browser
- [ ] Justfile includes `install`, `run-server` (with `--host`), and `init-dev`
