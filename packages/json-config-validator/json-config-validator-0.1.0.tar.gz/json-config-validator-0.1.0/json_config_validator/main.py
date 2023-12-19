# -*- coding: utf-8 -*-
"""Validate a JSON configuration file using JSON schema validation."""
import logging
import os
import pathlib
import sys
from datetime import datetime

import click

from json_config_validator.json.schema.validator import Validator
from json_config_validator.terminal.color_utils import (
    print_green,
    print_red,
    print_yellow,
)

DEFAULT_OUTDIR = os.path.join(
    "/tmp/",
    os.path.basename(__file__),
    str(datetime.today().strftime("%Y-%m-%d-%H%M%S")),
)

LOGGING_FORMAT = "%(levelname)s : %(asctime)s : %(pathname)s : %(lineno)d : %(message)s"

LOG_LEVEL = logging.INFO

DEFAULT_VERBOSE = False


@click.command()
@click.option(
    "--json_file",
    help="Input JSON file to be validated against JSON schema doc",
)
@click.option(
    "--json_schema_file",
    help="JSON schema doc",
)
@click.option("--logfile", help="The log file")
@click.option(
    "--outdir",
    help=f"Output directory - default is '{DEFAULT_OUTDIR}'",
)
@click.option(
    "--verbose",
    is_flag=True,
    help=f"Will print more info to STDOUT - default is '{DEFAULT_VERBOSE}'",
)
def main(
    json_file: str,
    json_schema_file: str,
    logfile: str,
    outdir: str,
    verbose: bool,
):
    """Validate the JSON file against the JSON schema."""

    error_ctr = 0

    if json_file is None:
        print_red("--json_file was not specified")
        error_ctr += 1
    else:
        if not os.path.exists(json_file):
            print_red(f"input JSON file '{json_file}' does not exist")
            error_ctr += 1

    if json_schema_file is None:
        print_red("--json_schema_file was not specified")
        error_ctr += 1
    else:
        if not os.path.exists(json_schema_file):
            print_red(f"input JSON file '{json_schema_file}' does not exist")
            error_ctr += 1

    if error_ctr > 0:
        sys.exit(1)

    if outdir is None:
        outdir = DEFAULT_OUTDIR
        print_yellow(f"--outdir was not specified and therefore was set to '{outdir}'")

    if not os.path.exists(outdir):
        pathlib.Path(outdir).mkdir(parents=True, exist_ok=True)

        print_yellow(f"Created output directory '{outdir}'")

    if logfile is None:
        logfile = os.path.join(outdir, os.path.basename(__file__) + ".log")
        print_yellow(
            f"--logfile was not specified and therefore was set to '{logfile}'"
        )

    if verbose is None:
        verbose = DEFAULT_VERBOSE
        print_yellow(
            f"--verbose was not specified and therefore was set to '{verbose}'"
        )

    logging.basicConfig(filename=logfile, format=LOGGING_FORMAT, level=LOG_LEVEL)

    validator = Validator(
        json_schema_file=json_schema_file, logfile=logfile, outdir=outdir
    )

    if validator.is_valid(infile=json_file, json_schema_file=json_schema_file):
        logging.info(f"JSON file '{json_file}' is valid")
        print_green(f"JSON file '{json_file}' is valid")
    else:
        logging.error(f"JSON file '{json_file}' is not valid")
        print_red(f"JSON file '{json_file}' is not valid")

    print(f"The log file is '{logfile}'")
    print_green(f"Execution of {os.path.abspath(__file__)} completed")


if __name__ == "__main__":
    main()
