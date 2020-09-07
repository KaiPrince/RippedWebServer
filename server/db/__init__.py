from flask import Flask
from .service import close_db
from .command import init_db_command


def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
