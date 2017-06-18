# LUNA

> "She's getting here as fast as she can" -- Stella de How I Met Your Mother.

## Requirements

- Docker, [see how to install](https://docs.docker.com/engine/installation/linux/ubuntu/)
- Docker-Compose, [see how to install](https://docs.docker.com/compose/install/)

## Build and deploy

```sh
$ ./deploy
```

## Run the application

```sh
$ ./up 
```

### Workflow

1. Define your table at `backend/migrations/NUMBER_create_YOUR_TABLE_NAME_table.sql`
2. Migrate your new table: `./migrate NUMBER_create_YOUR_TABLE_NAME_table.sql`
2. Define your model at `backend/luna/server/models.py`
3. Define your repository at `backend/luna/server/repositories.py`
4. Create your views, templates and urls