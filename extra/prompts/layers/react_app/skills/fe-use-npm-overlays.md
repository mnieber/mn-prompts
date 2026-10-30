# Skill: fe-use-npm-overlays

Applies when a developer wants to work on an npm library (e.g. `skandha`) at the same time as the React app that uses it. Instead of installing the
published version, the app uses the library's source code from the developer's machine, so that changes to the library are picked up immediately.

See the `le-add-react-service-to-compose` skill (local_env layer) for how the frontend service is added to Docker Compose.

---

## How it works

The pattern combines three things:

1. A volume in `docker-compose.override.yml` that mounts the library's directory on the host to `/npm/<package-name>` in the container.
2. A `portal:/npm/<package-name>` dependency in the app's `package.json`, which makes yarn use the mounted directory as the package.
3. A `dependencies_overlaid` section in `package.json` that records the published version of each overlaid package.

Primary reference: `blogs_fe/package.json`, `blogs/env/local/docker/docker-compose.override.yml`

---

## 1. Mount the library — `docker-compose.override.yml`

```yaml
services:
  blogs_fe:
    volumes:
      # General overlays
      - /opt/projects/sunya/blogs_fe/fish_history:/root/.local/share/fish/fish_history
      # Npm package overlays
      - /home/maarten/projects/skandha/src:/npm/skandha
      - /home/maarten/projects/skandha-mobx/src:/npm/skandha-mobx
```

### Key rules

- **Mount to `/npm/<package-name>`** — the mount point uses the npm package name.
- **Mount the directory that contains the library's `package.json`** — in the example this is the library's `src` directory.
- **Use absolute host paths** — `docker-compose.override.yml` is developer-specific (and gitignored), so don't use `${ROOT_DIR}`.
- **Group the mounts** under a `# Npm package overlays` comment.
- **Ask the developer** which libraries they want to overlay, and where these libraries live on their machine.

---

## 2. Use the mounted library — `package.json`

```json
{
  "name": "blogs-fe",
  "dependencies_overlaid": {
    "skandha": "^0.14.0",
    "skandha-mobx": "^0.14.0"
  },
  "dependencies": {
    "mobx": "^6.9.0",
    "skandha": "portal:/npm/skandha",
    "skandha-mobx": "portal:/npm/skandha-mobx"
  },
  "packageManager": "yarn@4.16.0"
}
```

### Key rules

- **Use `portal:`, not `link:`** — a portal is a package: yarn also installs the dependencies that are declared in the library's
  `package.json`. A `link:` dependency is only a symlink, and its dependencies are ignored.
- **The portal path is the container path** (`/npm/<package-name>`), not the host path.
- **Record the published version in `dependencies_overlaid`** — for every `portal:` dependency, add the version range that is used when the
  package is not overlaid. This allows you to switch back to the published package by moving the version from `dependencies_overlaid` to
  `dependencies`.
- **Portals require yarn 2+** — set `packageManager` to a yarn version, and run `corepack enable` in `Dockerfile.local`.
- **Run `yarn install` inside the container** after adding or removing a portal, because `/npm/<package-name>` only exists there.
- **Don't work around failing installs elsewhere** — outside the local environment (e.g. in a production build) `yarn install` fails on the
  `portal:` dependencies. This is accepted: switch back to the published versions first.

---

## 3. Use the library's source code (optional)

When the library's `package.json` has an `exports` entry with a `development` condition that points to its TypeScript source, Vite's dev server
uses that source directly, so the library does not need to be rebuilt after each change:

```json
{
  "name": "skandha",
  "exports": {
    ".": {
      "development": "./index.ts",
      "default": "./index.js"
    }
  }
}
```

---

## Checklist

- [ ] Each overlaid library is mounted to `/npm/<package-name>` in `docker-compose.override.yml`, under `# Npm package overlays`
- [ ] Each overlaid library has a `portal:/npm/<package-name>` dependency in `package.json`
- [ ] Each `portal:` dependency has its published version in `dependencies_overlaid`
- [ ] `yarn install` was run inside the container
