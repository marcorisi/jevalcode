from pathlib import Path

import click
from typesafe_sdk import TypeSafeError

from .evaluator import evaluate_file

DEFAULT_CONFIDENCE_THRESHOLD = 0.6


@click.command()
@click.argument(
    "paths",
    nargs=-1,
    required=True,
    type=click.Path(exists=True, dir_okay=False, path_type=Path),
)
@click.option(
    "--threshold",
    default=DEFAULT_CONFIDENCE_THRESHOLD,
    show_default=True,
    help="Confidence below which a score is flagged for review.",
)
def cli(paths: tuple[Path, ...], threshold: float) -> None:
    """Score one or more source files against the jevalcode rubric."""
    for path in paths:
        try:
            response = evaluate_file(path)
        except TypeSafeError as e:
            raise click.ClickException(str(e))
        click.echo(f"\n{path}")
        for name, answer in response.answers.items():
            flag = " ⚠ low confidence" if answer.confidence < threshold else ""
            click.echo(f"  {name:<15} {answer.score:.2f}/4  (confidence {answer.confidence:.2f}){flag}")


if __name__ == "__main__":
    cli()
