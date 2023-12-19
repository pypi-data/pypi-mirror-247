#!/usr/bin/env python

"""Tests for `code_inspection_utils` package."""


import unittest
from click.testing import CliRunner

from code_inspection_utils import code_inspection_utils
from code_inspection_utils import cli


class TestCode_inspection_utils(unittest.TestCase):
    """Tests for `code_inspection_utils` package."""

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
        assert 'code_inspection_utils.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
