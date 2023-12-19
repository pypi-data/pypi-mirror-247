"""Console script for profile_data_directory."""
import logging
import os
import pathlib
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional

import click
import yaml
from rich.console import Console

from profile_data_directory.manager import Manager

DEFAULT_DATABASE_FILE_EXTENSION = "sqlite3"

DEFAULT_OUTDIR = os.path.join(
    "/tmp/profile_data_directory/",
    str(datetime.today().strftime("%Y-%m-%d-%H%M%S")),
)

DEFAULT_CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "conf", "config.yaml"
)


DEFAULT_LOGGING_FORMAT = (
    "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"
)

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = True


error_console = Console(stderr=True, style="bold red")

console = Console()

logger = logging.getLogger(__name__)


def check_infile_status(infile: str, extension: Optional[str] = None) -> None:
    """Check if the file exists, if it is a regular file and whether it has
    content.

    Args:
        infile (str): the file to be checked

    Raises:
        None
    """

    error_ctr = 0

    if infile is None or infile == "":
        error_console.print(f"'{infile}' is not defined")
        error_ctr += 1
    else:
        if not os.path.exists(infile):
            error_ctr += 1
            error_console.print(f"'{infile}' does not exist")
        else:
            if not os.path.isfile(infile):
                error_ctr += 1
                error_console.print(f"'{infile}' is not a regular file")
            if os.stat(infile).st_size == 0:
                error_console.print(f"'{infile}' has no content")
                error_ctr += 1
            if extension is not None and not infile.endswith(extension):
                error_console.print(
                    f"'{infile}' does not have filename extension '{extension}'"
                )
                error_ctr += 1

    if error_ctr > 0:
        error_console.print(f"Detected problems with input file '{infile}'")
        sys.exit(1)


def setup_filehandler_logger(logfile: str = None) -> None:
    # Create handlers
    # c_handler = logging.StreamHandler()
    f_handler = logging.FileHandler(filename=logfile)

    # c_handler.setLevel(DEFAULT_LOGGING_LEVEL)
    f_handler.setLevel(DEFAULT_LOGGING_LEVEL)

    # Create formatters and add it to handlers
    f_format = logging.Formatter(DEFAULT_LOGGING_FORMAT)
    # c_format = logging.Formatter("%(levelname)-7s : %(asctime)s : %(message)s")

    # c_handler.setFormatter(c_format)
    f_handler.setFormatter(f_format)

    # Add handlers to the logger
    # logger.addHandler(c_handler)
    logger.addHandler(f_handler)


@click.command()
@click.option(
    "--config_file",
    type=click.Path(exists=True),
    help=f"The configuration file for this project - default is '{DEFAULT_CONFIG_FILE}'",
)
@click.option(
    "--indir",
    help="The input directory to be profiled",
)
@click.option("--logfile", help="The log file")
@click.option(
    "--outdir",
    help=f"The default is the current working directory - default is '{DEFAULT_OUTDIR}'",
)
@click.option("--outfile", help="The output report file")
@click.option(
    "--verbose",
    is_flag=True,
    help=f"Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'",
)
def main(
    config_file: str,
    indir: str,
    logfile: str,
    outdir: str,
    outfile: str,
    verbose: bool,
):
    """Console script for profile_data_directory."""

    error_ctr = 0

    if indir is None:
        console.print("[bold red]--indir was not specified[/]")

    if error_ctr > 0:
        return -1

    if config_file is None:
        config_file = DEFAULT_CONFIG_FILE
        console.print(
            f"[yellow]--config_file was not specified and therefore was set to '{config_file}'[/]"
        )

    check_infile_status(config_file)

    if outdir is None:
        outdir = DEFAULT_OUTDIR
        console.print(
            f"[yellow]--outdir was not specified and therefore was set to '{outdir}'[/]"
        )

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)

        console.print(f"[yellow]Created output directory '{outdir}'[/]")

    if logfile is None:
        logfile = os.path.join(
            outdir, os.path.splitext(os.path.basename(__file__))[0] + ".log"
        )
        console.print(
            f"[yellow]--logfile was not specified and therefore was set to '{logfile}'[/]"
        )

    if outfile is None:
        outfile = os.path.join(
            outdir, os.path.splitext(os.path.basename(__file__))[0] + ".report.txt"
        )
        console.print(
            f"[yellow]--outfile was not specified and therefore was set to '{outfile}'[/]"
        )


    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    # Read the configuration from the JSON file and
    # load into dictionary.
    logging.info(f"Will load contents of config file '{config_file}'")
    config = yaml.safe_load(Path(config_file).read_text())

    manager = Manager(
        config=config,
        config_file=config_file,
        indir=indir,
        logfile=logfile,
        outdir=outdir,
        outfile=outfile,
    )

    manager.generate_report()

    print(f"The log file is '{logfile}'")
    console.print(
        f"[bold green]Execution of '{os.path.abspath(__file__)}' completed[/]"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())  # pragma: no cover
