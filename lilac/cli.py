# coding=utf8

"""cli interface for lilac"""


import logging
from .utils import join
from os.path import dirname
from .logger import logger
from .server import run_server
from . import version
from .generator import generator
from subprocess import call
from docopt import docopt


def task(task_func):
    def wrapper(*args, **kwargs):
        # set logger's level to info
        logger.setLevel(logging.INFO)
        if task_func.__doc__:
            logger.info(task_func.__doc__)
        return task_func()
    return wrapper


@task
def deploy():
    """deploy blog: classic/, src/post/sample.md, src/about.md, config.toml, Makefile"""
    lib_dir = dirname(__file__)  # this library's directroy
    res = join(lib_dir, "resources")
    call("rsync -aqu " + join(res, "*") + " .", shell=True)
    logger.success("deploy done")
    logger.info("Please edit config.toml to meet tour needs")
    logger.info("Run 'make build' to build blog to htmls")
    logger.info("Run 'make clean' to remove built htmls")


@task
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
    logger.success("clean done")


@task
def build():
    generator.generate()


def main():
    """Usage:
  lilac [-h|-v]
  lilac deploy
  lilac build
  lilac clean
  lilac server [<port>]

  Options:
    -h --help     show this help message
    -v --version  show version

  Commands:
    deploy        deploy blog in current directroy
    build         build blog source to html
    clean         remove files built by lilac
    server        start a simple server here"""

    arguments = docopt(main.__doc__, version='lilac version: ' + version)

    if arguments["deploy"]:
        deploy()
    elif arguments["clean"]:
        clean()
    elif arguments["build"]:
        build()
    elif arguments["server"]:
        if arguments["<port>"]:
            port = int(arguments["<port>"])
        else:
            port = 8000
        run_server(port)
    else:
        exit(main.__doc__)
