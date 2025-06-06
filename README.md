# Task Service

Simple Django CRUD API for tasks. Includes health and readiness endpoints.

## Development

Install dependencies and run migrations:

```bash
make install
make migrate
```

Run the server:

```bash
make run
```

Run tests:

```bash
make test
```

Database configuration is provided via environment variables:
`APP_ENV`, `PG_HOST`, `PG_PORT`, `PG_DB`, `PG_USER`, `PG_PASSWORD`, `PG_SSLMODE`, `LOG_LEVEL`.
