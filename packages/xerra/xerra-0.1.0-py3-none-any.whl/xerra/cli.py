from pathlib import Path
from typing import Optional, List

import click
from loguru import logger

from xerra.importer import run_import, ImportFilter


@click.group()
def cli():
    pass


@click.command()
@click.argument("path")
@click.option("--app", required=False, help="Filter based on ex/em")
@click.option("--roi", required=False, help="Specific ROI to convert to mhd")
@click.option("--output-path", required=False,help="Output directory for mhd")
@click.option("--times-downsampled", default=0, help="Downsampled factor")
@click.option(
    "--exposure",
    "-e",
    multiple=True,
    help="exposures to include",
    default=[],
)
def generate_mhd(
        path: str,
        app: Optional[str] = None,
        roi: Optional[str] = None,
        exposure: List[int] = [],
        output_path: Optional[str] = None,
        times_downsampled: int = 0,
):
    input_filter = ImportFilter(
        app=app,
        roi=roi,
        exposure=exposure,
        output_dir=output_path,
        downsample_factor=times_downsampled,
    )
    path = Path(path).resolve()
    if path.exists():
        run_import(path,input_filter)
    else:
        logger.error(f"Missing input path {path}")

@click.command()
@click.argument("path")
def download(path: str):
    pass



def main():
    cli.add_command(download)
    cli.add_command(generate_mhd)
    cli()


if __name__ == "__main__":
    main()
