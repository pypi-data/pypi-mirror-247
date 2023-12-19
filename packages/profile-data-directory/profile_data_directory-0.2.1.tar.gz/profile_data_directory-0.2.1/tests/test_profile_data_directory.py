#!/usr/bin/env python

"""Tests for `profile_data_directory` package."""


import unittest
from click.testing import CliRunner

from profile_data_directory import profile_data_directory
from profile_data_directory import cli


class TestProfile_data_directory(unittest.TestCase):
    """Tests for `profile_data_directory` package."""

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
        assert 'profile_data_directory.cli.main' in result.output
        help_result = runner.invoke(cli.main, ['--help'])
        assert help_result.exit_code == 0
        assert '--help  Show this message and exit.' in help_result.output
