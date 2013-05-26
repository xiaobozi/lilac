# coding=utf8

"""Run a server and start to watch posts for changes to auto
rebuild as a default option, we can choose to not watch"""


from .utils import join
from .models import Post, About
from .config import config
from os import listdir as ls
from os import stat
from os.path import exists
from time import sleep
from threading import Thread
from SocketServer import ThreadingMixIn
from BaseHTTPServer import HTTPServer
from SimpleHTTPServer import SimpleHTTPRequestHandler as handler
import logging
from .logger import logger
from .generator import generator


class MultiThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Multiple threaded http server"""
    pass


class Server(object):
    """Start a web server at some port(default: 8888), and watch to rebuild"""

    def __init__(self):
        self.files_stat = {}   # init a empty filepath to stat dic
        self.server = None
        logger.setLevel(logging.INFO)  # set logger level to info

    def run_server(self, port=8888):
        """run a server binding to port(default 8888)"""
        self.server = MultiThreadedHTTPServer(('0.0.0.0', port), handler)
        logger.info("Serve at 0.0.0.0:%d(ctrl-c to stop it) ..." % port)
        try:
            self.server.serve_forever()
        except KeyboardInterrupt:
            logger.info("^C received, shutting down server")
            self.shutdown()

    def get_files_stat(self):
        paths = Post.glob_src_files().keys()  # posts'path
        # about
        if exists(generator.about.src):
            paths.append(generator.about.src)
        # config.toml
        if exists(config.filepath):
            paths.append(config.filepath)
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
                except SystemExit:
                    logger.error("Error occurred, server shut down")
                    self.shutdown()
                logger.success("Rebuild success")
                self.files_stat = files_stat  # update files' stat

    def run(self, port=8888, watch=True):
        """run a server here, as a defalut option, start watching changes
        to rebuild"""
        if watch:
            watcher_thread = Thread(target=self.watch_files)
            watcher_thread.daemon = True
            watcher_thread.start()
        self.run_server(port)

    def shutdown(self):
        """shut down the server"""
        self.server.shutdown()
        self.server.socket.close()


server = Server()
