# coding=utf8

"""builder for lilac"""

from .utils import join
from .models import Post, about
from .config import config
from .logger import logger
from .generator import generator

import logging
from os import listdir as ls
from os import stat
from os.path import exists
from time import sleep
from threading import Thread
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler as handler


class MultiThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Multiple threaded http server"""
    # TODO: standard the format the sever logging
    pass


class Builder(object):
    """To build source to html, optional, can watch files for
    changes to auto rebuild , or start a web server here the same time"""

    def __init__(self):
        # files_stat: filepath to file's updated time dict
        self.files_stat = {}
        # server: the server instance initialized from MultiThreadedHTTPServer
        self.server = None
        # watcher: the thread to watch files for changes
        self.watcher = Thread(target=self.watch_files)
        self.watcher.daemon = True
        # set logger level to info
        logger.setLevel(logging.INFO)

    def run_server(self, port=8888):
        """run a server binding to port(default 8888)"""
        self.server = MultiThreadedHTTPServer(('0.0.0.0', port), handler)
        logger.info("Serve at 0.0.0.0:%d(ctrl-c to stop it) ..." % port)
        try:
            self.server.serve_forever()
            # add exception catch for address already used
        except KeyboardInterrupt:
            logger.info("^C received, shutting down server")
            self.shutdown_server()

    def get_files_stat(self):
        """Get current filepath to file updated time dict"""
        # posts
        paths = Post.glob_src_files().keys()
        # about
        if exists(about.src):
            paths.append(about.src)
        # config.toml
        if exists(config.filepath):
            paths.append(config.filepath)
        # files - a <filepath to updated time> dict
        files = dict((p, stat(p).st_mtime) for p in paths)
        return files

    def watch_files(self):
        """watch files for changes, if changed, rebuild blog"""
        while 1:
            sleep(1)
            files_stat = self.get_files_stat()
            if self.files_stat != files_stat:
                logger.info("Changes detected, start rebuilding..")

                try:
                    generator.re_generate()
                except SystemExit:  # catch sys.exit, it means fatal error
                    logger.error("Error occurred, server shut down")
                    self.shutdown_server()

                logger.success("Rebuild success")
                self.files_stat = files_stat  # update files' stat

    def run(self, watch=False, server=False, port=8888):
        """start building blog, options: run a server, start watching
        changes"""
        if watch:  # if watch, start a thread to watch
            self.watcher.start()

        if server:  # if server, start server threading
            self.run_server(port)

        if not watch and not server:  # just build for once
            generator.generate()

    def shutdown_server(self):
        """shut down the web server"""
        self.server.shutdown()
        self.server.socket.close()

builder = Builder()
