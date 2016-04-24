# -*- coding: utf-8 -*-

"""
    xweb.interactive
    ~~~~~~~~~~~~~~~~

    An interactive environment for xweb.
"""

import click
import os.path
from agen import generate_dir

from .. import invoke


def invoke_server():
    app = invoke.create_app()
    app.invoke_app()
    app.run()


@click.group()
def cli():
    pass


@cli.command()
def serve():
    """
    Run debug server.
    """
    invoke_server()


@cli.command()
@click.argument('name')
def init(name):
    """
    Initialize XWeb project
    """
    _current_dir = os.path.dirname(os.path.abspath(__file__))
    _template_dir = os.path.join(_current_dir, 'templates', 'xweb')
    generate_dir(_template_dir, name)
