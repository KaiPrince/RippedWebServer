FROM python:3

ENV FLASK_ENV=production \
    POETRY_VERSION=1.1.13

WORKDIR /usr/src

COPY poetry.lock pyproject.toml ./

RUN pip install "poetry==$POETRY_VERSION"

RUN poetry config virtualenvs.create false \
  && poetry install --no-dev --no-interaction --no-ansi

COPY . .

ENTRYPOINT [ "poetry" ]

CMD [ "run", "start" ]
