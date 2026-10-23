# Layer: local_env

This layer describes how to set up and manage a **local development environment** for a stack containing multiple services.

## Overview

A local_env stack runs all services in Docker containers via Docker Compose. Developers use Just commands to build, start, and operate the stack. Environment variables are managed through `.env.in` templates that are compiled into `.env` files before containers start.

## Skills

Read the relevant skill(s) before generating or modifying any files. Each skill covers one concern and cross-references others where they overlap.

### Setting up the stack

| Skill                | When to use                                                                                                                                   |
| -------------------- | --------------------------------------------------------------------------------------------------------------------------------------------- |
| `le-use-compose-ops` | Setting up the justfile structure, ROOT_DIR/COMPOSE_DIR/COMPOSE_PROJECT_NAME, `.local.env`, `secrets.env`, and the compile-env-files workflow |
| `le-add-base-image`  | Creating a shared base Docker image used by multiple Python services                                                                          |

### Adding services

| Skill                              | When to use                                                                                                 |
| ---------------------------------- | ----------------------------------------------------------------------------------------------------------- |
| `le-add-python-service-to-src`     | Creating the source directory structure, Dockerfiles, requirements files, and justfile for a Python service |
| `le-add-python-service-to-compose` | Wiring a Python service into the Docker Compose files and creating its `.env.in` template                   |
| `le-add-react-service-to-compose`  | Wiring a React/Vite frontend service into the Docker Compose files and creating its `.env.in` template      |

### Adding infrastructure

| Skill                        | When to use                                                       |
| ---------------------------- | ----------------------------------------------------------------- |
| `le-add-postgres-to-compose` | Adding a PostgreSQL service to Docker Compose                     |
| `le-add-localstack`          | Adding LocalStack for local AWS service emulation (S3, SQS, etc.) |

### Adding libraries

| Skill                    | When to use                                                                         |
| ------------------------ | ----------------------------------------------------------------------------------- |
| `le-add-python-stub-lib` | Adding a stub for a Python library whose source code lives in a separate repository |

### Developer tooling

| Skill                        | When to use                                                                                        |
| ---------------------------- | -------------------------------------------------------------------------------------------------- |
| `le-write-dodo-config-files` | Setting up dodo_commands config files (`config.yaml`, `stack.root.yaml`, `stack.<service>.yaml`)   |
| `le-add-spec-src`            | Adding an `extra/spec_src/` directory to a service and wiring it into the root `sunya.config.yaml` |

## Typical setup order

When setting up a new stack from scratch, apply the skills in roughly this order:

1. `le-use-compose-ops` — justfile structure, `.local.env`, secrets
2. `le-add-base-image` — shared Python base image
3. `le-add-postgres-to-compose` — database service
4. `le-add-python-service-to-src` + `le-add-python-service-to-compose` — backend service(s)
5. `le-add-react-service-to-compose` — frontend service (if applicable)
6. `le-add-python-stub-lib` — external library stubs (if applicable)
7. `le-write-dodo-config-files` — dodo_commands wiring
8. `le-add-spec-src` — spec source directories (if applicable)
