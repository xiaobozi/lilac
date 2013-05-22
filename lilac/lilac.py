# coding=utf8
# This is the application script also the cli interface.

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
from .utils import logger
from subprocess import call
from docopt import docopt

import os


# tasks

def deploy():
    lilac_dir = os.path.dirname(__file__)
    res = os.path.join(lilac_dir, "resources")
    classic = os.path.join(res, "classic")
    sample_post = os.path.join(res, "sample.md")
    sample_config = os.path.join(res, "config.toml")
    makefile_path = os.path.join(res, "Makefile")
    call(["mkdir", "-p", "src/post"])
    call(["touch", "src/about.md"])
    call(["cp", sample_post, "src/post/helloworld.md"])
    call(["cp", sample_config, "."])
    call(["cp", "-r", classic, "."])
    call(["cp", makefile_path, "."])
    logger.ok("Deployment complete")
    logger.info("Please edit config.toml")


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
    logger.info(" ".join(cmd))
    exit_code = call(cmd)
    if exit_code == 0:
        logger.ok("Clean done")


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
        task = generate
    task()
