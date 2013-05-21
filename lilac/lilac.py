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
  clean          remove files built by lilac
"""

from ._ import version
from .generator import generator
from .utils import _call
from .utils import log
from docopt import docopt

import os


# tasks

def deploy():
    lilac_dir = os.path.dirname(__file__)
    res = os.path.join(lilac_dir, "resources")
    classic = os.path.join(res, "classic")
    sample_post = os.path.join(res, "sample.md")
    sample_config = os.path.join(res, "config.toml")

    _call(["mkdir", "-p", "src/post"])
    _call(["touch", "src/about.md"])
    _call(["cp", sample_post, "src/post/helloworld.md"])
    _call(["cp", sample_config, "."])
    _call(["cp", "-r", classic, "."])
    log.ok("Deployment complete.")
    log.info("Please edit config.toml.")


def clean():
    paths = [
        "post",
        "page",
        "tag",
        "404.html",
        "about.html",
        "archives.html",
        "feed.atom",
        "index.html",
        "tags.html"
    ]

    cmd = ["rm", "-rf"] + paths
    exit_code = _call(cmd)
    if exit_code == 0:
        log.ok("Clean done.")


def generate():
    generator.generate()


def main():
    dct = docopt(__doc__, version='lilac version ' + version)

    task = lambda: exit(__doc__)

    if dct['deploy']:
        task = deploy
    if dct['clean']:
        task = clean
    if dct['generate']:
        task  = generate
    task()
