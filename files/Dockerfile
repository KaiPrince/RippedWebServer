FROM python:3

ENV FLASK_ENV=production

WORKDIR /usr/src

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Initialize DB
# RUN if [ ! -f "$DATABASE" ]; then echo "Initializing DB..."; flask init-db; fi

ENTRYPOINT [ "gunicorn" ]

CMD [ "app:app", "--bind", "0.0.0.0:5000" ]