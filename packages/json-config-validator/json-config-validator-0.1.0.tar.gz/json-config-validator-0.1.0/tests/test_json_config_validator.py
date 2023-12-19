#!/usr/bin/env python

"""Tests for `json_config_validator` package."""


import unittest
from click.testing import CliRunner

from json_config_validator import json_config_validator
from json_config_validator import cli


class TestJson_config_validator(unittest.TestCase):
    """Tests for `json_config_validator` package."""

    def setUp(self):
        """Set up test fixtures, if any."""

    def tearDown(self):
        """Tear down test fixtures, if any."""

    def test_000_something(self):
        """Test something."""

    def test_command_line_interface(self):
        """Test the CLI."""
        runner = CliRunner()
        result = runner.invoke(cli.main)
        assert result.exit_code == 0
        assert 'json_config_validator.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
