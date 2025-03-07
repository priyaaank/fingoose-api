import click
from flask.cli import FlaskGroup
from app import create_app, db

app = create_app()
cli = FlaskGroup(app)

@cli.command("init_db")
def init_db():
    """Initialize the database."""
    click.echo('Creating database tables...')
    db.create_all()
    click.echo('Database tables created!')

@cli.command("drop_db")
def drop_db():
    """Drop the database."""
    if click.confirm('Are you sure you want to drop all tables?', abort=True):
        db.drop_all()
        click.echo('Database tables dropped!')

if __name__ == "__main__":
    cli() 