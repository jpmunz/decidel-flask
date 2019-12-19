Swagger UI at https://api.decidel.ca/v1/docs

[Front-end](https://github.com/jpmunz/decidel-web) at https://decidel.ca

See [DEPLOYMENT.md](DEPLOYMENT.md) for deployment instructions.

View the [Roadmap on Trello](https://trello.com/b/z4REn8Mg/decidel-roadmap).

### DEVELOPMENT

### Setup

```
  python3 -m venv venv
  . venv/bin/activate
  pip install -r requirements.txt
```

Make sure redis is installed

```
  wget http://download.redis.io/redis-stable.tar.gz
  tar xvzf redis-stable.tar.gz
  cd redis-stable
  make
```

### Run

```
  redis-server
```

```
  . venv/bin/activate
  FLASK_APP=decidel FLASK_ENV=development flask run
```

### Deployment

See [these instructions](https://development-recipes.readthedocs.io/en/latest/hosting.html) for initial setup.

Actual deployment is handled by the [Deploy Action](.github/workflows/deploy.yml).

![](https://github.com/jpmunz/decidel-flask/workflows/Build%20and%20Deploy/badge.svg)
