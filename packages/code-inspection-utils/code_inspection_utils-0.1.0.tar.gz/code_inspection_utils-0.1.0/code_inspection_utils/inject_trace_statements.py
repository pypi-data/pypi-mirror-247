"""Copy the data files in the specified directory to a destination and preserve the directory structure."""
import os
import sys
import click
import pathlib
import logging
import yaml

from pathlib import Path
from datetime import datetime
from rich.console import Console

from code_inspection_utils.manager import Manager


DEFAULT_TRACE_PREFIX = "TRACE::"

DEFAULT_OUTDIR = os.path.join(
    '/tmp/',
    os.path.splitext(os.path.basename(__file__))[0],
    str(datetime.today().strftime('%Y-%m-%d-%H%M%S'))
)

DEFAULT_CONFIG_FILE = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    'conf',
    'config.yaml'
)


DEFAULT_LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

DEFAULT_LOGGING_LEVEL = logging.INFO

DEFAULT_VERBOSE = True

error_console = Console(stderr=True, style="bold red")

console = Console()


def check_infile_status(infile: str = None, extension: str = None) -> bool:
    """Check if the file exists, if it is a regular file and whether it has content.

    Args:
        infile (str): the file to be checked

    Raises:
        None
    """

    error_ctr = 0

    if infile is None or infile == '':
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
                error_console.print(f"'{infile}' does not have filename extension '{extension}'")
                error_ctr += 1

    if error_ctr > 0:
        error_console.print(f"Detected problems with input file '{infile}'")
        sys.exit(1)




@click.command()
@click.option('--config_file', type=click.Path(exists=True), help=f"The configuration file for this project - default is '{DEFAULT_CONFIG_FILE}'")
@click.option('--infile', help="Required: the file into which trace statements should be inserted")
@click.option('--logfile', help="The log file")
@click.option('--outdir', help="The default is the current working directory - default is '{DEFAULT_OUTDIR}'")
@click.option('--outfile', help="Optional: The output file that should contain the inserted trace statements")
@click.option('--trace_prefix', help=f"Optional: The trace prefix to insert in the trace statements - default is '{DEFAULT_TRACE_PREFIX}'")
@click.option('--verbose', is_flag=True, help=f"Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'")
def main(config_file: str, infile: str, logfile: str, outdir: str, outfile: str, trace_prefix: str, verbose: bool):
    """Insert trace print statements inside all code blocks."""
    error_ctr = 0

    if infile is None:
        error_console.print("--infile was not specified")
        error_ctr += 1

    if error_ctr > 0:
        sys.exit(1)

    if config_file is None:
        config_file = DEFAULT_CONFIG_FILE
        console.print(f"[yellow]--config_file was not specified and therefore was set to '{config_file}'[/]")

    if outdir is None:
        outdir = DEFAULT_OUTDIR
        console.print(f"[yellow]--outdir was not specified and therefore was set to '{outdir}'[/]")

    if trace_prefix is None:
        trace_prefix = DEFAULT_TRACE_PREFIX
        console.print(f"[yellow]--trace_prefix was not specified and therefore was set to '{trace_prefix}'[/]")

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)

        console.print(f"[yellow]Created output directory '{outdir}'[/]")

    if logfile is None:
        logfile = os.path.join(
            outdir,
            os.path.splitext(os.path.basename(__file__))[0] + '.log'
        )
        console.print(f"[yellow]--logfile was not specified and therefore was set to '{logfile}'[/]")


    logging.basicConfig(
        filename=logfile,
        format=DEFAULT_LOGGING_FORMAT,
        level=DEFAULT_LOGGING_LEVEL,
    )

    check_infile_status(config_file, "yaml")
    check_infile_status(infile)

    logging.info(f"Will load contents of config file '{config_file}'")
    config = yaml.safe_load(Path(config_file).read_text())

    manager = Manager(
        config=config,
        config_file=config_file,
        logfile=logfile,
        outdir=outdir,
        trace_prefix=trace_prefix,
        verbose=verbose,
    )

    manager.insert_trace_statements(infile, outfile)

    print(f"The log file is '{logfile}'")
    console.print(f"[bold green]Execution of '{os.path.abspath(__file__)}' completed[/]")


if __name__ == "__main__":
    main()
