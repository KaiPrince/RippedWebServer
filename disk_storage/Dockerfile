FROM python:3

ENV FLASK_ENV=production

WORKDIR /usr/src

COPY requirements.txt ./

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENTRYPOINT [ "gunicorn" ]

CMD [ "app:create_app()", "--bind", "0.0.0.0:5000" ]