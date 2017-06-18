# Luna Web

> "She's getting here as fast as she can" -- Stella de How I Met Your Mother.

## Requirements

- Python 3 and pip, [see how to install](https://stackoverflow.com/questions/6587507/how-to-install-pip-with-python-3)
- pipenv, [see how to install](https://github.com/kennethreitz/pipenv/#-installation)

## Build and deploy

Install the dependencies

```sh
$ pipenv install --dev
```

Set the `.env` file and configure the DB_ variables

```sh
$ cp .env.example .env
```

Generate a new APP_KEY

```sh
$ pipenv run python generate_key.py
```

Create the tables

```sh
$ pipenv run python manage.py create_db
```

## Run the application

```sh
$ pipenv run python manage.py runserver
```

So access the application at the address http://localhost:5000/

> Want to specify a different port?
> `$ pipenv run python manage.py runserver -h 0.0.0.0 -p 8080`

### Workflow

1. Define your table at `backend/migrations/NUMBER_create_YOUR_TABLE_NAME_table.sql`
2. Migrate your new table: `./migrate NUMBER_create_YOUR_TABLE_NAME_table.sql`
2. Define your model at `backend/luna/server/models.py`
3. Define your repository at `backend/luna/server/repositories.py`
4. Create your views, templates and urls