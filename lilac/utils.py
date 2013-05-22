# coding=utf8

"""
  Utils for lilac: colored output, log etc.
"""

import sys
from termcolor import colored


class Logger(object):
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

logger = Logger()


class ProgressLogger(object):

    def __init__(self, description=''):
        self.reset(description)

    def reset(self, description):
        self.description = description
        self.done = False
        return self

    @property
    def text(self):
        if self.done:
            state = "[done]"
            color = "green"
        else:
            state = "[....]"
            color = "yellow"
        return colored(state, color) + "  " + self.description

    def __enter__(self):
        sys.stdout.write(self.text)
        sys.stdout.flush()

    def __exit__(self, type, value, traceback):
        # clean this line
        sys.stdout.write("\r%s" % ' '* len(self.text))
        # back to left
        sys.stdout.write("\r")
        self.done = True
        sys.stdout.write(self.text)
        sys.stdout.write("\n")
        sys.stdout.flush()


progress_logger = ProgressLogger()


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
