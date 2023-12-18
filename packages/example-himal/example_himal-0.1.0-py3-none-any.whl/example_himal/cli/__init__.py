# SPDX-FileCopyrightText: 2023-present Himal Shrestha <himal.shrestha@unimelb.edu.au>
#
# SPDX-License-Identifier: MIT
import click
# import typer

from example_himal.__about__ import __version__


@click.group(context_settings={"help_option_names": ["-h", "--help"]}, invoke_without_command=True)
@click.version_option(version=__version__, prog_name="example_himal")
def example_himal():
    click.echo("Hello world!")
