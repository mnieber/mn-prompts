Consult [local_env_layer/index.md](./local_env_layer/index.md) for a local development stack of multiple services:

- the Docker Compose files, and the `jaz` targets that build, start, initialise and operate the stack
- adding Python and React services, PostgreSQL, base images and stub libraries to the stack
- the environment variables of the services

Reference app: [examples/blogs/](./examples/blogs/) is a complete stack (a Django backend with PostgreSQL, a React
frontend, Docker Compose and `jaz` targets), and the primary template for the local_env patterns.
