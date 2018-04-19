FROM python:3.6

COPY ./app /app
COPY ./dictionary.pickle dictionary.pickle
COPY ./tfidf.pickle tfidf.pickle
COPY ./Pipfile Pipfile
COPY ./Pipfile.lock Pipfile.lock

WORKDIR /

EXPOSE 5000

RUN pip install pipenv

RUN pipenv install --system

RUN spacy download en

# RUN python app/manage.py create_db

CMD ["python", "app/manage.py", "runserver"]
