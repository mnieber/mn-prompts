# Skill: le-add-spec-src

Applies when adding a `spec_src` directory to a service and wiring it into the root `sunya.config.yaml`.

Primary reference: `../examples/blogs/src/services/blogs_be/extra/spec_src/`, `../examples/blogs/sunya.config.yaml`

---

## What this skill covers

- The `extra/spec_src/` directory structure inside a service
- The per-service `sunya.config.yaml`
- The per-topic layout, where `spec_src` has a subdirectory (with its own `sunya.config.yaml`) per topic
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

### Per-topic layout

A `spec_src` directory can also have a subdirectory per topic (e.g. `changelog` and `release_notes`). Each topic
has its own `sunya.config.yaml` and `scenarios/` directory, and there is no `sunya.config.yaml` directly in
`spec_src`:

```
src/services/<service_name>/
└── extra/
    └── spec_src/
        ├── __init__.py
        ├── changelog/
        │   ├── __init__.py
        │   ├── sunya.config.yaml
        │   └── scenarios/
        │       ├── __init__.py
        │       └── <scenario_name>/
        │           └── scenario.py
        └── release_notes/
            ├── __init__.py
            ├── sunya.config.yaml
            └── scenarios/
                └── ...
```

---

## Per-service sunya.config.yaml

Create `src/services/<service_name>/extra/spec_src/sunya.config.yaml`:

```yaml
output_dir: md_specs
component_name: blogs_be
package_config_by_name:
  blogs_be:
    scenario_paths:
      - ./scenarios/**/scenario.py
```

### Key fields

**output_dir:** Directory (relative to the `sunya.config.yaml` file) where rendered markdown specs are written. Always `md_specs`.

**component_name:** The name of this service/component. Use the service name (e.g. `blogs_be`).

**package_config_by_name:** Maps package names to their config, which contains the glob patterns for finding spec files. The package name matches the service name.

**scenario_paths:** Glob pattern for scenario files. Always `./scenarios/**/scenario.py`.

**RULE:** Use the service name for both `component_name` and the package key under `package_config_by_name`.

### Per-topic sunya.config.yaml

In the per-topic layout, create `src/services/<service_name>/extra/spec_src/<topic>/sunya.config.yaml` for each
topic. It has the same fields as the per-service config, but `component_name` is the topic name:

```yaml
output_dir: md_specs
component_name: changelog
package_config_by_name:
  blogs_be:
    scenario_paths:
      - ./scenarios/**/scenario.py
```

**RULE:** In the per-topic layout, use the topic name for `component_name`. The package key under
`package_config_by_name` is still the service name.

---

## Root sunya.config.yaml

The root `sunya.config.yaml` lives at the stack root (next to `src/`) and lists all per-service configs:

```yaml
configs:
  - src/services/blogs_be/extra/spec_src/sunya.config.yaml
output_dir: /opt/projects/sunya/browse
```

### Key fields

**configs:** List of paths (relative to this file) to per-service `sunya.config.yaml` files. Add one entry per service that has a `spec_src` directory. In the per-topic layout, add one entry per topic instead:

```yaml
configs:
  - src/services/blogs_be/extra/spec_src/changelog/sunya.config.yaml
  - src/services/blogs_be/extra/spec_src/release_notes/sunya.config.yaml
```

**output_dir:** Absolute path to the directory where the combined rendered output is written. This is a developer-local path and should be confirmed with the developer.

**RULE:** When adding a new service's spec_src, append its config path to the `configs` list in the root `sunya.config.yaml`. In the per-topic layout, append the config path of each topic, also when a topic is added later.

**RULE:** Ask the developer for the correct `output_dir` path — it is machine-specific and not committed as a shared value.

---

## Checklist

- [ ] `extra/spec_src/` directory created inside the service
- [ ] `__init__.py` created at `extra/spec_src/`
- [ ] `scenarios/` directory created with `__init__.py` (per topic, in the per-topic layout)
- [ ] Per-service `sunya.config.yaml` created with correct `component_name` and glob patterns (per topic, with the topic name as `component_name`, in the per-topic layout)
- [ ] Root `sunya.config.yaml` updated to include the new service's config path (or the path of each topic's config)
- [ ] `output_dir` in root config confirmed with the developer
