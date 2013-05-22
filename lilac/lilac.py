# coding=utf8
# This is the application script also the cli interface.

"""Usage:
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
from .utils import progress_logger
from subprocess import call
from docopt import docopt

import os


# tasks

def deploy():
    """deploy blog: classic/, src/post/helloworld.md, src/about.md, config.toml, Makefile"""
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


def clean():
    """rm -rf post page tag 404.html about.html archives.html feed.atom index.html tags.html"""
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
    call(cmd)


def generate():
    generator.generate()


def main():
    arguments = docopt(__doc__, version='lilac version ' + version)

    if arguments["deploy"]:
        with progress_logger.reset(deploy.__doc__):
            deploy()
    elif arguments["clean"]:
        with progress_logger.reset(clean.__doc__):
            clean()
    elif arguments["generate"]:
        generate()
    else:
        exit(__doc__)
