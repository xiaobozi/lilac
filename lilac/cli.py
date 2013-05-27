# coding=utf8

"""cli interface for lilac"""


import logging
import sys
from .utils import join
from os.path import dirname
from .logger import logger
from .builder import builder
from watcher import watcher
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
        return task_func(*args, **kwargs)
    return wrapper


@task
def deploy():
    """deploy blog: classic/, src/post/, config.toml, Makefile"""
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
def build(watch, server, port):
    builder.run(watch, server, port)


def main():
    """Usage:
  lilac [-h|-v]
  lilac build [--watch] [--server] [<port>]
  lilac deploy
  lilac clean

Options:
  -h --help     show this help message
  -v --version  show version
  --watch       watch source files for changes
  --server      start a server here
  <port>        which port for server to use(default: 8888)

Commands:
  deploy        deploy blog in current directroy
  build         build source files to htmls
  clean         remove files built by lilac"""

    arguments = docopt(main.__doc__, version='lilac version: ' + version)

    if arguments["deploy"]:
        deploy()
    elif arguments["clean"]:
        clean()
    elif arguments["build"]:
        watch = arguments["--watch"]
        server = arguments["--server"]
        port_s = arguments["<port>"]

        if not port_s:
            port = 8888
        else:  # check if port is an integer
            try:
                port = int(port_s)
            except ValueError:
                logger.error("Error format of argument 'port': '%s'" % port_s)
                sys.exit(1)

        build(watch, server, port)
    else:
        exit(main.__doc__)
