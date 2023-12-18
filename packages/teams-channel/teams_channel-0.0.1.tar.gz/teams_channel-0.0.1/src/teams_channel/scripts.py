################################################################
# Example scripts.py
#  - See https://click.palletsprojects.com/en/8.1.x/
################################################################
from __future__ import print_function, unicode_literals

import click

@click.group()
def teams_channel():
    pass


@teams_channel.command()
@click.option("--times", default=1)
def hello(times):
    from .example import print_hello
    
    print_hello(times=times)
