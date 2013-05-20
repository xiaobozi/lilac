# coding=utf8
# This is the application script also the\
# cli interface.

"""
Usage:
  lilac [-h|-v]
  lilac deploy
  lilac generate
  lilac clean

Options:
  -h --help      show this message
  -v --version   show version

Commands:
  deploy         deploy blog in current directory
  generate       generate blog from source
  clean          remove html files built by lilac

"""

from ._ import version
from docopt import docopt


def main():
    dct = docopt(__doc__, version='lilac version ' + version)
    print dct
