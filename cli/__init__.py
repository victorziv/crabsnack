import click

from crabsnack import create_app


@click.command()
def cli():
    """
    Run the application
    """
    app = create_app()
    with app.app_context():
        print("In context")
    app.run()
