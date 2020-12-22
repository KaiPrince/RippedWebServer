import click
from flask.cli import with_appcontext

from .service import init_db, create_super_user


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


@click.command("create-superuser")
@click.argument("username")
@with_appcontext
def create_superuser_command(username):
    """Create new user with all permissions."""

    password = click.prompt(
        "Enter your password",
        hide_input=True,
        confirmation_prompt=True,
    )

    create_super_user(username, password)

    click.echo("Created user.")
