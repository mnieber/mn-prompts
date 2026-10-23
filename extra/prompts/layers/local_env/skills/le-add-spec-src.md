# Skill: le-add-spec-src

Applies when adding a `spec_src` directory to a service and wiring it into the root `sunya.config.yaml`.

Primary reference: `../examples/blogs/src/services/blogs_be/extra/spec_src/`, `../examples/blogs/sunya.config.yaml`

---

## What this skill covers

- The `extra/spec_src/` directory structure inside a service
- The per-service `sunya.config.yaml`
- The root `sunya.config.yaml` that aggregates all services

## What this skill does NOT cover

- **How scenario files are written** → see target-specific documentation

---

## Directory structure

Each service that has specs gets an `extra/spec_src/` directory:

```
src/services/<service_name>/
└── extra/
    └── spec_src/
        ├── __init__.py
        ├── sunya.config.yaml
        └── scenarios/
            ├── __init__.py
            └── <scenario_name>/
                └── scenario.py
```

---

## Per-service sunya.config.yaml

Create `src/services/<service_name>/extra/spec_src/sunya.config.yaml`:

```yaml
output_dir: md_specs
component_name: blogs_be
spec_paths_by_package:
  blogs_be:
    scenario_paths:
      - ./scenarios/**/scenario.py
```

### Key fields

**output_dir:** Directory (relative to the `sunya.config.yaml` file) where rendered markdown specs are written. Always `md_specs`.

**component_name:** The name of this service/component. Use the service name (e.g. `blogs_be`).

**spec_paths_by_package:** Maps package names to glob patterns for finding spec files. The package name matches the service name.

**scenario_paths:** Glob pattern for scenario files. Always `./scenarios/**/scenario.py`.

**RULE:** Use the service name for both `component_name` and the package key under `spec_paths_by_package`.

---

## Root sunya.config.yaml

The root `sunya.config.yaml` lives at the stack root (next to `src/`) and lists all per-service configs:

```yaml
configs:
  - src/services/blogs_be/extra/spec_src/sunya.config.yaml
output_dir: /opt/projects/sunya/browse
```

### Key fields

**configs:** List of paths (relative to this file) to per-service `sunya.config.yaml` files. Add one entry per service that has a `spec_src` directory.

**output_dir:** Absolute path to the directory where the combined rendered output is written. This is a developer-local path and should be confirmed with the developer.

**RULE:** When adding a new service's spec_src, append its config path to the `configs` list in the root `sunya.config.yaml`.

**RULE:** Ask the developer for the correct `output_dir` path — it is machine-specific and not committed as a shared value.

---

## Checklist

- [ ] `extra/spec_src/` directory created inside the service
- [ ] `__init__.py` created at `extra/spec_src/`
- [ ] `scenarios/` directory created with `__init__.py`
- [ ] Per-service `sunya.config.yaml` created with correct `component_name` and glob patterns
- [ ] Root `sunya.config.yaml` updated to include the new service's config path
- [ ] `output_dir` in root config confirmed with the developer
