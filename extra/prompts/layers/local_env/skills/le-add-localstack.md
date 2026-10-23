# Skill: le-add-localstack

Applies when adding LocalStack to a stack for local AWS service emulation (S3, SQS, etc.).

---

## What is LocalStack?

LocalStack is a local AWS cloud service emulator that allows you to develop and test cloud applications offline. It provides mock implementations of AWS services like S3, SQS, DynamoDB, and more.

## Docker Compose service definition

Add the following service to your `docker-compose.yml`:

```yaml
services:
  localstack:
    container_name: <stack_name>_localstack
    image: "localstack/localstack:3.4.0"
    ports:
      - 4566:4566
    env_file:
      - env_files/localstack.env
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:4566/health"]
      interval: 5s
      timeout: 5s
      retries: 5
    volumes:
      - "${ROOT_DIR}/src/services/localstack/scripts/initaws.d:/docker-entrypoint-initaws.d"
```

## Environment file

Create an empty environment file at `env/local/docker/env_files/localstack.env.in`. LocalStack works with default configuration for most development scenarios.

## Initialization scripts

LocalStack automatically runs scripts placed in `/docker-entrypoint-initaws.d` on startup. Create initialization scripts at:

```
src/services/localstack/scripts/initaws.d/
```

### Example: S3 bucket initialization

Create `src/services/localstack/scripts/initaws.d/init_s3.sh`:

```bash
#!/bin/bash

for bucket in files; do
  aws --endpoint-url=http://localstack:4566 s3 mb s3://$bucket && aws --endpoint-url=http://localstack:4566 s3api put-bucket-acl --bucket $bucket --acl public-read-write
done
```

RULE: List all required buckets/resources in the initialization script. Modify the `for bucket in files;` line to include all bucket names your application needs.

## Service dependencies

Services that depend on LocalStack should declare the dependency in their docker-compose service definition:

```yaml
services:
  my_service:
    depends_on:
      localstack:
        condition: service_healthy
```

## Checklist

- [ ] LocalStack service added to docker-compose.yml with correct container name
- [ ] Port 4566 exposed
- [ ] Healthcheck configured
- [ ] Volume mount configured for init scripts: `${ROOT_DIR}/src/services/localstack/scripts/initaws.d:/docker-entrypoint-initaws.d`
- [ ] Empty localstack.env file created at `env/local/docker/env_files/localstack.env.in`
- [ ] Initialization scripts created in `src/services/localstack/scripts/initaws.d/`
- [ ] Init scripts are executable and use correct endpoint URL
- [ ] Dependent services use `depends_on` with `condition: service_healthy`
