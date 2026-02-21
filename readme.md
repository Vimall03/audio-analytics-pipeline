## Running FastAPI and Celery Individually

To start the FastAPI server only:

```
docker compose up app
```

To start the Celery worker only:

```
docker compose up celery
```

This will launch just the selected service and its dependencies. Use `docker compose up` to start everything together.