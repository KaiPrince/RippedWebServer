from flask import Flask

from .command import init_db_command, create_superuser_command
from .service import close_db


def init_app(app: Flask):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(create_superuser_command)
