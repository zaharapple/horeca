### Setup project:

```bash
    git clone git@github.com:zaharapple/horeca.git &&
    cd horeca &&
    cp .env.template .env &&
    mkdir static &&
    mkdir media
```

##### Need to set up .env

#### Add venv (python 3.12)

```bash
    make venv &&
    make db-up &&
    make migrate
```

```bash
    make create-superuser
```

```bash
    make run
```

