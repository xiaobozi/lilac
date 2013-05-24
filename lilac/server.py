# coding=utf8

"""a really simple HTTP server for lilac to preview blog
locally"""

import SimpleHTTPServer
from BaseHTTPServer import HTTPServer
from .logger import logger
import logging


def run_server(port=8000):
    Handler = SimpleHTTPServer.SimpleHTTPRequestHandler
    server = HTTPServer(('0.0.0.0', port), Handler)
    logger.setLevel(logging.INFO)
    logger.info("Serve at 0.0.0.0:%d (Ctrl-c to stop).." % port)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        logger.info("^C received, shutting down server")
        server.socket.close()


if __name__ == '__main__':
    run_server()
