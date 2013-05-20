# coding=utf8

"""
  Utils for lilac: colored output, log etc.

  colored("red", "this is text")
  log.error(text), log.info(text), log.warn(text), log.ok(text)
  call(['ls', '-a'])   # call `ls -a` in a subprocess, return exit_code
"""

import sys
from termcolor import colored
from subprocess import call


class Log(object):
    """logging message to screen"""

    def error(self, message):
        """Error message in red, kill the sys"""
        print colored("red", "[error]" + message)
        sys.exit(1)

    def info(self, message):
        """Print message"""
        print '[info] ' + message

    def ok(self, message):
        """Tell the user the success message"""
        print colored("[ok]\t" + message, "green")

    def warn(self, message):
        """Warning message"""
        print colored("[warn]\t" + message, "yellow")


log = Log()
