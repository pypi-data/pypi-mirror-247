import typer

cli = typer.Typer()

@cli.command()
def run():
    """
    Launch the app
    """
    from .demo import launch
    launch()

@cli.callback(no_args_is_help=True)
def main(ctx: typer.Context):
    """
    """
