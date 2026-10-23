# Skill: le-add-postgres-to-compose

Applies when adding a PostgreSQL database service to the Docker Compose configuration for local development.

Primary reference: `../examples/blogs/env/local/docker/docker-compose.yml`, `../examples/blogs/env/local/docker/env_files/postgres.env.in`

---

## What this skill covers

- Adding the `postgres` service to `docker-compose.yml`
- Creating the postgres environment file template
- Wiring application services to depend on postgres

## What this skill does NOT cover

- **Application service environment variables for connecting to postgres** → see `layers/local_env/skills/le-add-python-service-to-compose.md`
- **Django database configuration** → see `targets/django_app`

---

## Adding postgres to docker-compose.yml

Add the postgres service definition to `env/local/docker/docker-compose.yml` and a named volume for persistent data:

```yaml
services:
  postgres:
    container_name: blogs_postgres
    env_file:
      - ./env_files/postgres.env
    image: postgres:14.0
    ports:
      - 5432:5432
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data: {}
```

### Service definition fields

**container_name:** Use `<stack_name>_postgres` to namespace it and avoid collisions with other stacks running locally.

```yaml
container_name: blogs_postgres
```

**image:** Pin to a specific postgres version for reproducibility.

```yaml
image: postgres:14.0
```

**volumes:** Use a named volume (not a bind mount) so that database data persists across `docker compose down` and is managed by Docker.

```yaml
volumes:
  postgres_data: {}
```

**RULE:** Declare the named volume at the top level of `docker-compose.yml` (under `volumes:`), not just under the service.

**RULE:** Do not use a bind mount for the data directory. A named volume avoids permission issues and survives container recreation.

---

## Creating the environment file template

Create `env/local/docker/env_files/postgres.env.in`:

```bash
POSTGRES_HOST=postgres
POSTGRES_PORT=5432
POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
```

The `POSTGRES_PASSWORD` variable is sourced from `secrets.env` at compile time (see `layers/local_env/skills/le-add-secrets-env.md`).

**RULE:** `POSTGRES_HOST` must be the Docker Compose service name (`postgres`), not `localhost`.

---

## Wiring application services to depend on postgres

Any service that needs postgres must declare the dependency in `docker-compose.yml`:

```yaml
services:
  blogs_be:
    depends_on:
      - postgres
```

This ensures postgres starts before the application service. The application service connects using `POSTGRES_HOST=postgres` (the service name, not `localhost`).

---

## Checklist

- [ ] `postgres` service added to `docker-compose.yml` with pinned image version
- [ ] `container_name` uses `<stack_name>_postgres` pattern
- [ ] Named volume `postgres_data` declared at the top-level `volumes:` key
- [ ] `env/local/docker/env_files/postgres.env.in` created with `POSTGRES_HOST`, `POSTGRES_PORT`, `POSTGRES_PASSWORD`
- [ ] `POSTGRES_PASSWORD` references a variable from `secrets.env`
- [ ] Application services that use postgres have `depends_on: - postgres`
