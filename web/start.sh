 rm flask_context.db
 APP_CONFIG=development APP_DEVELOPMENT_DATABASE_URI=postgres://keynews:123456@localhost:5432/keynews python app/manage.py runserver