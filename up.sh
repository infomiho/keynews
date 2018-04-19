docker-compose build
docker-compose up -d postgres
# Source: https://github.com/juggernaut/nginx-flask-postgres-docker-compose-example
docker-compose run --rm web /bin/bash -c "python app/manage.py create_db"
docker-compose up -d web
