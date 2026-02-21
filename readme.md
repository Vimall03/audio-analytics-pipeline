---


Build and start all services:

```
docker compose up --build
```

To start only FastAPI:

```
docker compose up app
```

To start only Celery:

```
docker compose up celery
```


Once FastAPI is running, visit:

```
http://localhost:8000/docs
```
for interactive API documentation and testing.


Postgres and pgAdmin are included in Docker Compose. Access pgAdmin at:

```
http://localhost:5050
```
Login with:
	- Email: admin@admin.com
	- Password: admin

The database and tables are automatically created when the app service starts. 