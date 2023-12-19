# -*- coding: utf-8 -*-
"""Class for performing JSON schema validation on any JSON file."""
import json
import logging
import os
from datetime import datetime

from jsonschema import validate
from jsonschema.exceptions import ValidationError

DEFAULT_TIMESTAMP = str(datetime.today().strftime("%Y-%m-%d-%H%M%S"))

DEFAULT_OUTDIR = os.path.join("/tmp", os.path.basename(__file__), DEFAULT_TIMESTAMP)

DEFAULT_VERBOSE = False


class Validator:
    """Class for performing JSON schema validation on any JSON file."""

    def __init__(self, **kwargs):
        """Class constructor."""
        self.config_file = kwargs.get("config_file", None)
        self.config = kwargs.get("config", None)
        self.logfile = kwargs.get("logfile", None)
        self.outdir = kwargs.get("outdir", None)
        self.outfile = kwargs.get("outfile", None)
        self.json_schema_file = kwargs.get("json_schema_file", None)
        if self.json_schema_file is None:
            self.json_schema_file = self.config["json_schema_file"]
        self.verbose = kwargs.get("verbose", DEFAULT_VERBOSE)
        self._is_valid = None

        logging.info(
            f"Instantiated the Validator class in '{os.path.abspath(__file__)}'"
        )

    def is_valid(self, infile: str = None, json_schema_file: str = None) -> bool:
        """Determine whether the input JSON file is valid when validated
        against JSON schema doc.

        Args:
            infile (str): the input cohort metadata JSON file
            json_schema_file (str): the JSON schema doc file
        Returns:
            bool
        """
        if self._is_valid is None:
            if json_schema_file is None:
                json_schema_file = self.json_schema_file
            self.validate_file(infile=infile, json_schema_file=json_schema_file)
        return self._is_valid

    def validate_file(self, infile: str = None, json_schema_file: str = None) -> bool:
        """Execute JSON schema validation on the cohort metadata JSON file.

        Args:
            infile (str): the input cohort metadata JSON file
            json_schema_file (str): the JSON schema doc file
        Returns:
            bool: True if valid, False if not valid
        """
        if not os.path.exists(infile):
            raise Exception(f"json file '{infile}' does not exist")

        with open(infile, "r") as json_file:
            text = json_file.read()
            json_data = json.loads(text)

        schema = None

        with open(json_schema_file, "r") as file:
            schema = json.load(file)
        try:
            validate(instance=json_data, schema=schema)
            self._is_valid = True
        except ValidationError as err:
            logging.error(err)
            logging.exception(
                f"JSON schema validation failed for cohort metadata JSON file '{infile}' using schema doc '{json_schema_file}'"
            )
            self._is_valid = False
