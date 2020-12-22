from flask import Flask

from .command import init_db_command
from .service import close_db


def init_app(app: Flask):
    app.teardown_appcontext(close_db)

    app.cli.add_command(init_db_command)
