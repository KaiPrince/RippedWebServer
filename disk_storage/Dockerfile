FROM python:3

ENV FLASK_ENV=production

WORKDIR /usr/src

COPY poetry.lock ./

RUN pip install poetry
RUN poetry install --no-dev

COPY . .

ENTRYPOINT [ "gunicorn" ]

CMD [ "app:create_app()", "--bind", "0.0.0.0:5000" ]
