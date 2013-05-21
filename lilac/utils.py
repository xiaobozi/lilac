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
        print colored(message, "red")
        sys.exit(1)

    def info(self, message):
        """Print message"""
        print message

    def ok(self, message):
        """Tell the user the success message"""
        print colored(message, "green")

    def warn(self, message):
        """Warning message"""
        print colored(message, "yellow")


log = Log()


def chunks(lst, number):
    """
      A generator to split list `lst` into `number` equal size parts.

      ::

          lst = range(1, 9)
          chunks(lst, 3)  # return a list each time
                          # [1, 2, 3]
                          # [4, 5, 6]
                          # [7, 8]
    """
    l = len(lst)
    for i in xrange(0, l, number):
        yield lst[i:i + number]


def update_nested_dict(a, b):
    """
      Update nested dict recursivly
    """

    for k, v in b.iteritems():
        if isinstance(v, dict):
            d = a.setdefault(k, {})
            update_nested_dict(d, v)
        else:
            a[k] = v
    return a


def _call(cmds):
    log.info(" ".join(cmds))
    return call(cmds)
